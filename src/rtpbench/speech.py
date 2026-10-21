"""Reference speech boundaries on a clean source, the labels detectors are measured against.

Measured in the telephone band (zero-phase high-pass at 200 Hz, which removes the sub-100 Hz
wobble TTS engines and bridges leave after speech). Speech is where the 4 ms RMS, one value per
ms, is within 35 dB of the source's active speech level for at least 10 ms; gaps shorter than
20 ms do not split it. Each edge is then moved to the first/last sample in its window whose
unfiltered magnitude reaches the threshold (the filter rings around abrupt edges). At 8 kHz a
word-edge /s/ sits 25-35 dB below the active level, so a higher threshold cuts fricatives off.
"""

import math
import wave
from array import array
from pathlib import Path

CORPUS = Path(__file__).resolve().parents[2] / "corpus"
WINDOW = 32  # samples, 4 ms
STEP = 8  # samples, 1 ms
BELOW_ACTIVE_DB = 35.0
MIN_SPEECH = 10  # steps
MIN_GAP = 20  # steps
FLOOR_MARGIN_DB = 6  # the quietest 200 ms must sit this far under the threshold
HIGHPASS_HZ = 200


def highpass(pcm: list[int], rate: int = 8000) -> list[float]:
    """2nd-order Butterworth high-pass, run forwards then backwards (no phase shift)."""
    w = 2 * math.pi * HIGHPASS_HZ / rate
    alpha = math.sin(w) / math.sqrt(2)
    a0 = 1 + alpha
    b0, b1 = (1 + math.cos(w)) / 2 / a0, -(1 + math.cos(w)) / a0
    a1, a2 = -2 * math.cos(w) / a0, (1 - alpha) / a0

    def run(x: list[float]) -> list[float]:
        y, x1, x2, y1, y2 = [], 0.0, 0.0, 0.0, 0.0
        for s in x:
            v = b0 * (s + x2) + b1 * x1 - a1 * y1 - a2 * y2
            x2, x1, y2, y1 = x1, s, y1, v
            y.append(v)
        return y

    return run(run([float(s) for s in pcm])[::-1])[::-1]


def active_power(x: list[float]) -> float:
    """Mean power of the 20 ms frames within 30 dB of the loudest one."""
    frames = [sum(s * s for s in x[i : i + 160]) / 160 for i in range(0, len(x) - 159, 160)]
    loud = [p for p in frames if p > max(frames, default=0) / 1000]
    if not loud:
        raise ValueError("no speech")
    return sum(loud) / len(loud)


def label(pcm: list[int], below_db: float = BELOW_ACTIVE_DB) -> list[tuple[int, int]]:
    """[start, end) sample spans of speech. Raises if the source is too noisy to label."""
    x = highpass(pcm)
    thr = active_power(x) * 10 ** (-below_db / 10)
    quiet = sorted(sum(s * s for s in x[i : i + 80]) / 80 for i in range(0, len(x) - 79, 80))
    if quiet[min(19, len(quiet) - 1)] > thr * 10 ** (-FLOOR_MARGIN_DB / 10):
        raise ValueError("source too noisy, or without silence, to label speech")
    acc = [0.0]
    for s in x:
        acc.append(acc[-1] + s * s)
    runs: list[list[int]] = []
    for k, c in enumerate(range(0, len(x), STEP)):
        lo, hi = max(0, c - WINDOW // 2), min(len(x), c + WINDOW // 2)
        if acc[hi] - acc[lo] < thr * (hi - lo):
            continue
        if runs and k - runs[-1][1] <= MIN_GAP:
            runs[-1][1] = k
        else:
            runs.append([k, k])
    amp = math.sqrt(thr)
    spans = []
    for a, b in runs:
        if b - a + 1 < MIN_SPEECH:
            continue
        lo, hi = max(0, a * STEP - WINDOW // 2), min(len(x), b * STEP + WINDOW // 2)
        start = next((i for i in range(lo, hi) if abs(pcm[i]) >= amp), a * STEP)
        end = next((i for i in range(hi - 1, start - 1, -1) if abs(pcm[i]) >= amp), b * STEP) + 1
        spans.append((start, end))
    return spans


def read_wav(path: Path) -> list[int]:
    try:
        with wave.open(str(path)) as w:
            if (w.getnchannels(), w.getsampwidth(), w.getframerate()) != (1, 2, 8000):
                raise ValueError(f"{path}: need 8 kHz mono 16-bit PCM")
            return list(array("h", w.readframes(w.getnframes())))
    except wave.Error, EOFError:  # not a WAV file, or a truncated one
        raise ValueError(f"{path}: need 8 kHz mono 16-bit PCM") from None


def clips(*prefixes: str) -> dict[str, list[int]]:
    """Corpus clips whose name starts with one of `prefixes`, in name order."""
    paths = sorted(p for p in CORPUS.glob("*.wav") if p.stem.startswith(prefixes))
    return {p.stem: read_wav(p) for p in paths}
