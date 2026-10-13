import math
import random

import pytest

from rtpbench import detect, speech

RATE = 8000


def tone(n: int, amp: float, hz: float = 1000) -> list[int]:
    return [round(amp * math.cos(2 * math.pi * hz * i / RATE)) for i in range(n)]


def noise(n: int, amp: float, seed: int = 1) -> list[int]:
    rng = random.Random(seed)
    return [round(rng.gauss(0, amp)) for _ in range(n)]


def test_label_is_sample_accurate_on_abrupt_edges() -> None:
    pcm = [0] * 2000 + tone(4000, 8000) + [0] * 2000
    assert speech.label(pcm) == [(2000, 6000)]


def test_label_keeps_a_weak_fricative_and_drops_a_click() -> None:
    # /s/-like noise 30 dB under the vowel, then the vowel; a 3 ms click far after it
    fricative = noise(400, 8000 / math.sqrt(2) * 10 ** (-30 / 20))
    click = tone(24, 3000)
    pcm = [0] * 2000 + fricative + tone(4000, 8000) + [0] * 2000 + click + [0] * 2000
    ((start, end),) = speech.label(pcm)
    assert 2000 <= start < 2000 + 16
    assert end == 6400


def test_label_splits_on_pauses_over_20_ms() -> None:
    pcm = [0] * 2000 + tone(1600, 8000) + [0] * 120 + tone(1600, 8000) + [0] * 400
    pcm += tone(1600, 8000) + [0] * 2000
    assert speech.label(pcm) == [(2000, 5320), (5720, 7320)]


def test_label_refuses_a_noisy_source() -> None:
    pcm = noise(16000, 300)
    pcm[4000:8000] = tone(4000, 8000)
    with pytest.raises(ValueError, match="noisy"):
        speech.label(pcm)


def test_gate_merges_gaps_up_to_20_ms() -> None:
    pcm = [0] * 800 + tone(800, 4000) + [0] * 160 + tone(800, 4000) + [0] * 161 + tone(80, 4000)
    spans = detect.gate(pcm)
    assert [s for s, _ in spans] == [800, 2721]
    assert spans[0][1] == 2560


@pytest.mark.parametrize("name", ["webrtcvad", "silero", "silero16"])
def test_window_detectors_ignore_silence(name: str) -> None:
    pytest.importorskip("webrtcvad" if name == "webrtcvad" else "onnxruntime")
    assert detect.DETECT[name]([0] * 16000) == []


def test_every_corpus_clip_labels_with_silence_around_it() -> None:
    clips = speech.clips("tts-", "human-", "cough-")
    assert len(clips) == 60
    lines = sorted((speech.CORPUS / "lines" / "en").glob("*.wav"))
    assert len(lines) == 28
    clips |= {p.stem: speech.read_wav(p) for p in lines}
    for name, pcm in clips.items():
        spans = speech.label(pcm)
        assert spans[0][0] >= 400, name  # at least 50 ms of non-speech before
        assert spans[-1][1] <= len(pcm) - 400, name
