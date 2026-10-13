import math

from rtpbench import g711
from rtpbench.agent import Responder
from rtpbench.analyze import stream
from rtpbench.rtp import FRAME, PTIME_NS, SAMPLE_NS, Packet
from rtpbench.speechcal import _truth

PT = g711.PCMA


def pay(out: object) -> bytes:
    """A source's payload (these sources never pause or set their own header fields)."""
    assert isinstance(out, bytes)
    return out


def tone(n: int, amp: float = 8000) -> list[int]:
    return [round(amp * math.cos(2 * math.pi * i / 8)) for i in range(n)]


def packets(pcm: list[int], seq0: int, t0: int = 0) -> list[tuple[int, Packet]]:
    audio = g711.encode(PT, pcm)
    return [
        (
            t0 + n * PTIME_NS,
            Packet(PT, (seq0 + n) & 0xFFFF, n * FRAME, 1, False, audio[i : i + FRAME]),
        )
        for n, i in enumerate(range(0, len(audio), FRAME))
    ]


def test_stream_fills_losses_and_maps_sender_positions_across_wrap() -> None:
    pkts = packets([0] * 1600 + tone(1600), seq0=65530)
    del pkts[12]  # seq 6, sample 1920 onwards of the sender's stream
    st = stream(pkts, PT)
    assert st.seq == 65530
    assert st.times[12] is None
    assert st.pcm[12 * FRAME : 13 * FRAME] == g711.decode(PT, bytes([g711.SILENCE[PT]]) * FRAME)
    i = st.index(65530, 1920 + 5)
    assert st.time(i, later=True) == 13 * PTIME_NS  # what a listener hears first: next packet
    assert st.time(i, later=False) == 11 * PTIME_NS + (FRAME - 1) * SAMPLE_NS
    assert _truth(st, [(1600, 3200)]) == (10 * PTIME_NS, 19 * PTIME_NS + (FRAME - 1) * SAMPLE_NS)
    assert _truth(st, [(1920, 2080)]) is None  # all of it lost


def test_agent_places_a_clips_labelled_onset_at_the_delay() -> None:
    clip = [0] * 777 + tone(2000) + [0] * 2000
    r = Responder(PT, seq0=100, delays=[1.0], replies=[("c", clip, [(777, 2777)])])
    r.pending = {"turn": 0, "target_ns": 1_000_000_000 + 1_234_567}
    sent = b"".join(pay(r.source(n, n * PTIME_NS)) for n in range(80))
    onset = g711.gate(PT, 1000).search(sent)
    assert onset is not None
    assert abs(onset.start() * SAMPLE_NS - 1_001_234_567) <= SAMPLE_NS // 2
    turn = r.turns[0]
    assert turn["clip"] == "c"
    assert turn["speech"] == [[turn["start"] + 777, turn["start"] + 2777]]
    assert turn["start"] + 777 == onset.start()
    assert (turn["onset_seq"] - 100) * FRAME + turn["onset_off"] == onset.start()
