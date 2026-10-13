import pytest

from rtpbench import g711
from rtpbench.agent import HANGOVER_NS, Responder
from rtpbench.analyze import Capture, Timed, latencies
from rtpbench.rtp import FRAME, PTIME_NS, SAMPLE_NS, Packet
from rtpbench.voice import GATE, voice

PT = g711.PCMU
SIL = bytes([g711.SILENCE[PT]]) * FRAME


def pay(out: object) -> bytes:
    """A source's payload (these sources never pause or set their own header fields)."""
    assert isinstance(out, bytes)
    return out


def stream(pcm: list[int], t0: int, ptime: int = PTIME_NS) -> Timed:
    audio = g711.encode(PT, pcm)
    frames = [audio[i : i + FRAME].ljust(FRAME, SIL[:1]) for i in range(0, len(audio), FRAME)]
    return [(t0 + n * ptime, Packet(PT, n, n * FRAME, 1, False, f)) for n, f in enumerate(frames)]


def call(caller_end: int, onset: int, net_ns: int) -> Capture:
    """Caller speaks samples [800, caller_end); agent speaks from sample `onset` of its stream.

    Both streams start at t=0; the agent's packets reach the caller `net_ns` late.
    """
    up = stream([0] * 800 + voice((caller_end - 800) / 8000, 140) + [0] * 30000, 0)
    down = stream([0] * onset + voice(0.5, 210) + [0] * 8000, net_ns)
    return Capture(up, down)


def last_active(pcm: list[int]) -> int:
    return max(i for i, s in enumerate(g711.encode(PT, pcm)) if abs(g711.ulaw_decode(s)) >= GATE)


def test_wire_is_sample_accurate() -> None:
    cap = call(caller_end=9_003, onset=17_777, net_ns=3_000_000)
    end = 800 + last_active(voice((9_003 - 800) / 8000, 140))
    want = (17_777 - end) * SAMPLE_NS + 3_000_000
    assert latencies(cap, PT, "wire") == [want]
    assert latencies(cap, PT, "rtp") == [want]
    assert latencies(cap, PT, "concat") == [want]
    # packet granularity: off by the onset/end offsets within their packets
    (got,) = latencies(cap, PT, "packet")
    assert got is not None
    assert abs(got - want) < PTIME_NS


def test_lost_packet_shifts_concat_but_not_wire() -> None:
    cap = call(caller_end=9_003, onset=17_777, net_ns=0)
    want = latencies(cap, PT, "wire")
    del cap.down[50]  # a silent packet before the onset (packet 111)
    assert latencies(cap, PT, "wire") == want
    assert latencies(cap, PT, "rtp") == want
    (got,), (ref,) = latencies(cap, PT, "concat"), want
    assert got is not None
    assert ref is not None
    assert got == ref - PTIME_NS


def test_late_first_packet_skews_rtp_timeline() -> None:
    cap = call(caller_end=9_003, onset=17_777, net_ns=0)
    want = latencies(cap, PT, "wire")
    t, p = cap.down[0]
    cap.down[0] = (t + 7_000_000, p)  # anchor packet delayed by jitter
    assert latencies(cap, PT, "wire") == want
    (got,), (ref,) = latencies(cap, PT, "rtp"), want
    assert got is not None
    assert ref is not None
    assert got == ref + 7_000_000


@pytest.mark.parametrize("delay", [0.3, 0.4567891, 1.29])
def test_agent_places_onset_at_the_injected_delay(delay: float) -> None:
    r = Responder(PT, seq0=65530, delays=[delay])
    utterance = g711.encode(PT, voice(0.5, 140))
    pkts = [utterance[i : i + FRAME] for i in range(0, len(utterance), FRAME)]
    arrival = 1_000_000_000
    for i, payload in enumerate(pkts + [SIL] * 20):
        r.on_packet(arrival + i * PTIME_NS + 37_000, Packet(PT, i, i * FRAME, 9, False, payload))
    assert r.pending is not None
    end = r.pending["end_ns"]
    assert (
        end - arrival - 37_000
        == (len(pkts) - 1) * PTIME_NS + (last_active(voice(0.5, 140)) % FRAME) * SAMPLE_NS
    )
    assert r.pending["target_ns"] - end == round(delay * 1e9) > HANGOVER_NS

    tick0 = arrival + 3_123_456  # sender clock unrelated to arrivals
    sent = b"".join(pay(r.source(n, tick0 + n * PTIME_NS)) for n in range(100))
    gate = g711.gate(PT, GATE)
    m = gate.search(sent)
    assert m is not None
    onset = tick0 + m.start() * SAMPLE_NS
    assert abs(onset - end - round(delay * 1e9)) <= SAMPLE_NS // 2
    turn = r.turns[0]
    assert turn["onset_seq"] == (65530 + m.start() // FRAME) & 0xFFFF
    assert turn["onset_off"] == m.start() % FRAME


def test_reordered_onset_counts_from_the_onset_packet() -> None:
    cap = call(caller_end=9_003, onset=17_777, net_ns=0)
    want = latencies(cap, PT, "wire")
    i = 17_777 // FRAME  # packet carrying the onset; the next one overtakes it by 5 ms
    (t1, p1), (t2, p2) = cap.down[i], cap.down[i + 1]
    cap.down[i], cap.down[i + 1] = (t2 - 25_000_000, p2), (t1, p1)
    assert latencies(cap, PT, "wire") == want


def test_onset_in_the_last_half_sample_goes_to_the_next_packet() -> None:
    r = Responder(PT, seq0=10, delays=[0.5])
    r.pending = {"turn": 0, "target_ns": 5 * PTIME_NS + FRAME * SAMPLE_NS - 30_000}
    sent = b"".join(pay(r.source(n, n * PTIME_NS)) for n in range(8))
    m = g711.gate(PT, GATE).search(sent)
    assert m is not None
    assert m.start() == 6 * FRAME
    assert (r.turns[0]["onset_seq"], r.turns[0]["onset_off"]) == (16, 0)
