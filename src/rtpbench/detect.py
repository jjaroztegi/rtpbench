"""Speech detectors for received audio: [start, end) sample spans of detected speech.

  gate       |sample| >= 1000 on the 16-bit scale; gaps under 20 ms merged
  webrtcvad  WebRTC VAD, aggressiveness 3, 10 ms frames
  silero     Silero VAD 6.2.3 (ONNX), 32 ms windows; speech from p >= 0.5 until p < 0.35

The window detectors run raw: no minimum durations and no padding, so their bias shows. They
need the `vad` extra (webrtcvad-wheels, onnxruntime); the Silero model is fetched once from
its PyPI wheel, checked against a pinned hash and cached.
"""

import hashlib
import io
import os
import urllib.request
import zipfile
from array import array
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

from rtpbench.voice import GATE, RATE

DETECTORS = ("gate", "webrtcvad", "silero")
GATE_GAP = 160
WEBRTC_MODE = 3
WEBRTC_FRAME = 80
SILERO_WINDOW = 256
SILERO_ON, SILERO_OFF = 0.5, 0.35
SILERO_WHEEL = (
    "https://files.pythonhosted.org/packages/84/ef/"
    "9099037ed6f180ea33220178df4107112c0ce2bf5fb4d6f6ab19db2844ed/"
    "silero_vad-6.2.3-py3-none-any.whl",
    "7b7f5436cfcb02fae583a05b512ea96467fd449fe54cb49a5e4f06c51a1e43b8",
)


def _spans(flags: Iterable[bool], size: int, gap: int = 0) -> list[tuple[int, int]]:
    """Runs of True in per-unit flags as sample spans, merging gaps of at most `gap` samples."""
    out: list[tuple[int, int]] = []
    for i, on in enumerate(flags):
        if not on:
            continue
        start, end = i * size, (i + 1) * size
        if out and start - out[-1][1] <= gap:
            out[-1] = (out[-1][0], end)
        else:
            out.append((start, end))
    return out


def gate(pcm: list[int]) -> list[tuple[int, int]]:
    return _spans((abs(s) >= GATE for s in pcm), 1, GATE_GAP)


def webrtc(pcm: list[int]) -> list[tuple[int, int]]:
    import webrtcvad

    vad = webrtcvad.Vad(WEBRTC_MODE)
    n = len(pcm) // WEBRTC_FRAME
    raw = array("h", pcm).tobytes()  # native order; webrtcvad wants little-endian (x86-64, arm64)
    step = 2 * WEBRTC_FRAME
    return _spans(
        (vad.is_speech(raw[i * step : (i + 1) * step], RATE) for i in range(n)), WEBRTC_FRAME
    )


def _silero_model() -> bytes:
    url, sha = SILERO_WHEEL
    cache = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "rtpbench"
    path = cache / f"silero_vad-{sha[:12]}.onnx"
    if not path.exists():
        with urllib.request.urlopen(url, timeout=60) as r:
            wheel = r.read()
        if hashlib.sha256(wheel).hexdigest() != sha:
            raise RuntimeError(f"{url}: unexpected sha256")
        with zipfile.ZipFile(io.BytesIO(wheel)) as z:
            model = z.read("silero_vad/data/silero_vad.onnx")
        cache.mkdir(parents=True, exist_ok=True)
        path.write_bytes(model)
    return path.read_bytes()


_session: Any = None


def silero(pcm: list[int]) -> list[tuple[int, int]]:
    """As silero_vad.OnnxWrapper at 8 kHz: 256-sample windows, each with 32 samples of context."""
    import numpy as np
    import onnxruntime

    global _session
    if _session is None:
        opts = onnxruntime.SessionOptions()
        opts.inter_op_num_threads = opts.intra_op_num_threads = 1
        _session = onnxruntime.InferenceSession(_silero_model(), sess_options=opts)
    x = np.asarray(pcm, dtype=np.float32) / 32768
    state = np.zeros((2, 1, 128), dtype=np.float32)
    context = np.zeros((1, 32), dtype=np.float32)
    sr = np.array(RATE, dtype=np.int64)
    flags, speaking = [], False
    for i in range(len(x) // SILERO_WINDOW):
        chunk = np.concatenate([context, x[None, i * SILERO_WINDOW : (i + 1) * SILERO_WINDOW]], 1)
        out, state = _session.run(None, {"input": chunk, "state": state, "sr": sr})
        context = chunk[:, -32:]
        p = float(out[0, 0])
        speaking = p >= SILERO_ON or (speaking and p >= SILERO_OFF)
        flags.append(speaking)
    return _spans(flags, SILERO_WINDOW)


DETECT: dict[str, Callable[[list[int]], list[tuple[int, int]]]] = {
    "gate": gate,
    "webrtcvad": webrtc,
    "silero": silero,
}
