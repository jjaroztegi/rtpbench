import itertools
import json
import time
from pathlib import Path
from typing import Any

import pytest

from rtpbench import cases, clock, g711, rtp
from rtpbench.agent import Responder
from rtpbench.rtp import FRAME, PTIME_NS, SAMPLE_NS, Packet
from rtpbench.voice import GATE, voice

STEP_NS = -50_000_000  # the wall clock jumps back 50 ms, as WSL2's did every ~30 s
AT_NS = 1_000_000_000  # real time of the step


class Host:
    """A fake host: time moves only when someone sleeps or reads a clock (1 µs a read), and the
    wall clock steps back once at AT_NS."""

    def __init__(self) -> None:
        self.mono = 0

    def monotonic(self) -> int:
        self.mono += 1_000
        return self.mono

    def realtime(self) -> int:
        self.mono += 1_000
        return self.mono + 7_000_000_000 + (STEP_NS if self.mono >= AT_NS else 0)

    def sleep(self, s: float) -> None:
        self.mono += round(s * 1e9)


class Wire:
    """A socket that notes the real (monotonic) time of each packet it sends."""

    def __init__(self, host: Host) -> None:
        self.host, self.sent = host, []  # type: ignore[var-annotated]

    def sendto(self, data: bytes, addr: tuple[str, int]) -> None:
        self.sent.append(self.host.mono)


def send(c: clock.Clock, host: Host, packets: int) -> list[int]:
    """Real send times of a sender ticking on `c`."""
    wire = Wire(host)
    sender: rtp.Sender

    def source(n: int, _tick: int) -> bytes:
        if n == packets - 1:
            sender.stop.set()
        return bytes(160)

    sender = rtp.Sender(wire, ("x", 1), 0, source, c.now() + PTIME_NS, 0, 1, c)  # type: ignore[arg-type]
    sender.run()
    return wire.sent


def test_sender_keeps_real_spacing_across_a_wall_clock_step() -> None:
    host = Host()
    sent = send(clock.Clock(host.realtime, host.monotonic, host.sleep), host, 100)
    gaps = [b - a for a, b in itertools.pairwise(sent)]
    assert sent[0] < AT_NS < sent[-1]
    assert max(abs(g - PTIME_NS) for g in gaps) < 50_000  # spin granularity, no step


def test_sender_on_the_wall_clock_would_gap_by_the_step() -> None:
    """What the senders did before: scheduled on CLOCK_REALTIME, a step back of 50 ms holds the
    next packet back 50 ms (a real gap in the audio, invisible in a capture)."""
    host = Host()
    on_wall = clock.Clock(host.realtime, host.realtime, host.sleep)
    gaps = [b - a for a, b in itertools.pairwise(send(on_wall, host, 100))]
    assert max(gaps) - PTIME_NS > -STEP_NS - 50_000


def test_kernel_stamps_land_on_the_clock_across_a_step() -> None:
    """A receive stamp (CLOCK_REALTIME) maps to the real time it was taken, before and after the
    step; until the step the clock reads what the wall clock (and a capture) reads."""
    host = Host()
    c = clock.Clock(host.realtime, host.monotonic, host.sleep)
    host.mono = AT_NS - 10_000_000
    wall = host.realtime()
    assert c.steady(wall) == wall
    assert abs(c.now() - host.realtime()) < 10_000
    host.mono = AT_NS + 10_000_000
    wall = host.realtime()
    assert abs(c.steady(wall) - (wall - STEP_NS)) < 10_000
    assert abs(c.now() - (host.realtime() - STEP_NS)) < 10_000


def test_reference_reply_keeps_its_delay_in_real_time_across_a_step() -> None:
    """The reference agent hears the caller stop (kernel stamps), the wall clock steps back,
    then it replies: in real time the reply still comes the injected delay after the end. Its
    truth stays positional (which packet and sample), so a capture reads both ends on the same
    clock and wire-vs-truth error is unaffected; only an interval spanning the step reads short."""
    host = Host()
    c = clock.Clock(host.realtime, host.monotonic, host.sleep)
    pt, delay = g711.PCMU, 0.6
    r = Responder(pt, seq0=0, delays=[delay])
    sil = bytes([g711.SILENCE[pt]]) * FRAME
    audio = g711.encode(pt, voice(0.5, 140))
    pkts = [audio[i : i + FRAME].ljust(FRAME, sil[:1]) for i in range(0, len(audio), FRAME)]
    start = AT_NS - 700_000_000  # the caller's utterance ends ~200 ms before the step
    for i, payload in enumerate(pkts + [sil] * 15):
        host.mono = start + i * PTIME_NS
        kernel = host.realtime() - 5_000  # stamped 5 µs before the receiver reads it
        r.on_packet(c.steady(kernel), Packet(pt, i, i * FRAME, 9, False, payload))
    assert r.pending is not None
    end_real = r.pending["end_ns"] - c.base  # the clock's time back to real (monotonic) time
    tick0 = c.now()
    sent = b"".join(_bytes(r.source(n, tick0 + n * PTIME_NS)) for n in range(120))
    m = g711.gate(pt, GATE).search(sent)
    assert m is not None
    onset_real = tick0 - c.base + m.start() * SAMPLE_NS
    assert end_real < AT_NS < onset_real
    assert abs(onset_real - end_real - round(delay * 1e9)) <= SAMPLE_NS


def _bytes(out: object) -> bytes:
    assert isinstance(out, bytes)
    return out


def test_watch_logs_a_step_and_flags_what_spans_it() -> None:
    offset = [0]

    def realtime() -> int:
        return time.monotonic_ns() + offset[0]

    c = clock.Clock(realtime, time.monotonic_ns, time.sleep)
    with clock.watch(c, every_s=0.005) as steps:
        time.sleep(0.03)
        offset[0] = STEP_NS
        time.sleep(0.03)
    assert len(steps) == 1
    (step,) = steps
    assert abs(step["step_ms"] - STEP_NS / 1e6) < 0.01  # readings ns apart
    lo, hi = step["wall_ns"]
    assert hi - lo < 100_000_000  # the window: two readings and the step
    assert clock.spans(lo - 1_000_000_000, hi + 1, steps)
    assert not clock.spans(lo - 1_000_000_000, lo - 1, steps)
    assert not clock.spans(hi + 1, hi + 1_000_000_000, steps)


def test_summaries_mark_what_ran_across_a_step() -> None:
    bar = list(cases.WIRE)
    timing = {"name": "BYE to its response", "ms": 2.0, "bar": bar, "truth_ms": 2.0}
    check = {"name": "agent RTP stops within 500 ms", "ok": False, "detail": ""}
    recs: list[dict[str, Any]] = [
        {"timings": [timing], "checks": [check], "stepped": [timing["name"], check["name"]]},
        {"timings": [timing], "checks": [check], "stepped": []},
    ]
    assert cases.timings(recs)[0][1].endswith("[1 across a clock step]")
    assert cases.failures(recs)[0].endswith("[1 across a clock step]")
    assert cases.errors(recs)[0].endswith("[1 across a clock step]")
    assert "none" in clock.note([])
    assert "not recorded" in clock.note(None)
    assert "1 (-50.0 ms)" in clock.note([{"wall_ns": [0, 1], "step_ms": -50.0}])


def test_rate_reads_a_clock_that_runs_fast_and_is_stepped_back() -> None:
    """A guest whose clocks run 1,700 ppm fast, the wall clock stepped back by what it gained
    every 30 s: between steps, "late" gains up to 51 ms, which no step marks."""
    true = [0]
    ppm, every = 1_700, 30_000_000_000

    def monotonic() -> int:
        return true[0] + true[0] * ppm // 1_000_000

    def realtime() -> int:
        return monotonic() - true[0] // every * every * ppm // 1_000_000

    c = clock.Clock(realtime, monotonic, time.sleep)
    true[0] = 10 * every  # ten steps later, just after one
    assert abs(c.rate() - ppm) < 1


def test_rate_note_bounds_the_drift_between_steps(tmp_path: Path) -> None:
    every = 30_000_000_000
    steps = [{"wall_ns": [k * every, k * every + 1], "step_ms": -51.0} for k in range(1, 11)]
    conds = tmp_path / "conditions.json"
    conds.write_text(json.dumps({"clock_rate_ppm": 1_700.0, "clock_steps": steps}))
    assert clock.rate_note(tmp_path).startswith(
        "Wall clock: 1,700 ppm fast between its steps, 30 s apart: late reads up to 51 ms off"
    )


@pytest.mark.parametrize(
    ("ppm", "steps"),
    [
        (1_700.0, [{"wall_ns": [0, 1], "step_ms": -51.0}]),  # one step is no rate
        (-20.0, []),  # within RATE_PPM
    ],
)
def test_rate_note_stays_quiet(ppm: float, steps: list[dict[str, Any]], tmp_path: Path) -> None:
    (tmp_path / "conditions.json").write_text(
        json.dumps({"clock_rate_ppm": ppm, "clock_steps": steps})
    )
    assert clock.rate_note(tmp_path) == ""
