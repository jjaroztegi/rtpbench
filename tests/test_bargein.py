import json
import math
from pathlib import Path
from typing import Any

import pytest

from rtpbench import bargein, g711, speech
from rtpbench.agent import SPEECH_HANGOVER_NS, Responder
from rtpbench.bargein import stop
from rtpbench.caller import Conversation
from rtpbench.rtp import FRAME, PTIME_NS, SAMPLE_NS, Packet

PT = g711.PCMA
SIL = bytes([g711.SILENCE[PT]]) * FRAME
S = 1_000_000_000


def pay(out: object) -> bytes:
    """A source's payload (these sources never pause or set their own header fields)."""
    assert isinstance(out, bytes)
    return out


def tone(n: int, amp: float = 8000) -> list[int]:
    return [round(amp * math.cos(2 * math.pi * i / 8)) for i in range(n)]


def active(payload: bytes) -> bool:
    return g711.gate(PT, 1000).search(payload) is not None


@pytest.mark.parametrize("stops", [True, False])
def test_agent_cuts_the_planned_delay_after_the_interjection(stops: bool) -> None:
    plan = [{"kind": "interrupt", "at_s": 1.0, "stop": stops, "stop_delay_s": 0.3456789}]
    clip = tone(40000)  # a 5 s reply
    r = Responder(PT, 7, [1.0], [("long", clip, [(0, 40000)])], SPEECH_HANGOVER_NS, plan)
    r.pending = {"turn": 0, "target_ns": 0}
    sent = [pay(r.source(n, n * PTIME_NS)) for n in range(10)]  # reply under way
    burst = g711.encode(PT, [0] * 37 + tone(123))
    arrival = 10 * PTIME_NS + 1_234_567
    r.on_packet(arrival, Packet(PT, 1, 0, 9, False, burst))  # caller cuts in at sample 37
    sent += [pay(r.source(n, n * PTIME_NS)) for n in range(10, 300)]
    audio = b"".join(sent)
    barge = r.turns[0]["barge"]
    assert barge["trigger_ns"] == arrival + 37 * SAMPLE_NS
    last = max(i for i in range(len(audio)) if audio[i] != SIL[0])
    if stops:
        want = (arrival + 37 * SAMPLE_NS + 345_678_900) / SAMPLE_NS
        assert abs(barge["cut"] - want) <= 0.5
        assert last == barge["cut"] - 1
    else:
        assert "cut" not in barge
        assert last == 40000 - 1
    for k in range(1, 70):  # the interjection ends; it must not become a turn
        r.on_packet(arrival + k * PTIME_NS, Packet(PT, 1 + k, 0, 9, False, SIL))
    assert r.pending is None


def test_stop_is_the_end_of_the_speech_in_progress() -> None:
    segs = [[0, 3 * S], [5 * S, 6 * S]]
    assert stop(segs, 2 * S) == 1 * S
    assert stop(segs, 3 * S + S // 2) == -S // 2  # agent fell silent in the pause cut into
    assert stop(segs, 4 * S) is None  # silent for a full second: nothing to stop


def test_caller_cuts_in_the_planned_time_after_the_reply_starts() -> None:
    prompt = ("p", tone(800), [(0, 800)])
    said = ("j", [0] * 100 + tone(800), [(100, 900)])
    conv = Conversation(PT, [(prompt, said, {"kind": "cough", "at_s": 0.5})], lead_ns=0)
    out = [pay(conv.source(n, n * PTIME_NS)) for n in range(30)]  # prompt: packets 0-4
    assert [active(p) for p in out[:6]] == [True] * 5 + [False]
    onset = 30 * PTIME_NS + 7 * SAMPLE_NS
    conv.on_packet(30 * PTIME_NS, Packet(PT, 1, 0, 9, False, g711.encode(PT, [0] * 7 + tone(153))))
    out = [pay(conv.source(n, n * PTIME_NS)) for n in range(30, 70)]
    first = next(n for n, p in enumerate(out, 30) if active(p))
    assert first == math.ceil((onset + 0.5 * S) / PTIME_NS)
    assert conv.turns[0]["speech"] == [[first * FRAME + 100, first * FRAME + 900]]
    assert conv.turns[0]["kind"] == "cough"
    for n in range(70, 400):  # 3 s of quiet ends the script; the sender keeps ticking after
        pay(conv.source(n, n * PTIME_NS))
    assert conv.done


def test_every_backchannel_clip_has_its_words() -> None:
    assert set(bargein.WORDS) == {p.stem for p in speech.CORPUS.glob("*-bc.wav")}


def test_pooled_counts_stops_per_clip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def turn(kind: str, clip: str, ms: float | None) -> dict[str, Any]:
        return {"kind": kind, "clip": clip, "measured_ms": {"wire/gate": ms}}

    by_run = {
        "a": [
            turn("backchannel", "tts-cori-bc", 300.0),
            turn("backchannel", "tts-cori-bc", -500.0),  # ended long before: left out
            turn("backchannel", "tts-ald-bc", None),
        ],
        "b": [turn("backchannel", "tts-cori-bc", 2500.0), turn("cough", "cough-c1-0", None)],
    }
    for name in by_run:
        (tmp_path / name).mkdir()
        (tmp_path / name / "caller.json").write_text(json.dumps({"pt": g711.PCMA}))
    monkeypatch.setattr(bargein, "turns", lambda run: by_run[run.name])
    text = bargein.pooled({"clean": [tmp_path / "a"], "lte": [tmp_path / "b"]})
    per_clip = text[text.index("Per clip") :]
    # a stop over 2 s after the onset is no stop; a clip a profile never played is "-"
    assert "| backchannel | tts-ald-bc | Ajá | 0/1 | - |" in per_clip
    assert "| backchannel | tts-cori-bc | Yeah | 1/1, 1 ended before | 0/1 |" in per_clip
    assert "| clean | backchannel | 1 | 1/2 |" in text  # the stop rate leaves it out too
    assert "| cough | cough-c1-0 |  | - | 0/1 |" in per_clip
