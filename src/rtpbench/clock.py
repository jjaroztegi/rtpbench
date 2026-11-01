"""Time for schedules, and the wall-clock steps that captures cannot see.

Captures stamp CLOCK_REALTIME, which time sync may step. Schedules run on a `Clock`:
CLOCK_REALTIME as it read at the start, carried on by CLOCK_MONOTONIC (NTP slews both alike;
only a step moves one and not the other). Until a step the two read the same to the nanosecond,
so logged times line up with captures; across one, schedules keep their real spacing and the
capture times jump. `Watch` logs the steps, so that what was measured across one is flagged.
A clock stepped back again and again runs fast in between, which no step marks: `Clock.rate`
measures it.
"""

import json
import statistics
import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from itertools import pairwise
from pathlib import Path
from typing import Any

STEP_NS = 100_000  # an offset change this large is a step, not reading noise
RATE_PPM = 100  # a wall clock this far off between steps adds to "late" (5 ms over 50 s)
WATCH_S = 0.1
# a step under this share of a timing's error bar (p5..p95 of a calibration) moves the timing
# less than the bar's own spread: no step for that timing
STEP_SHARE = 0.1


class Clock:
    def __init__(
        self,
        realtime: Callable[[], int] = time.time_ns,
        monotonic: Callable[[], int] = time.monotonic_ns,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.realtime, self.monotonic, self.sleep = realtime, monotonic, sleep
        self.base = self.offset()
        self.started = self.monotonic()

    def rate(self) -> float:
        """How fast CLOCK_REALTIME has run between its steps since this clock started, in ppm
        (positive: fast), against the time the steps set: their net change, per second. NTP
        slewing moves CLOCK_MONOTONIC alike, so only steps (of any size) count."""
        stepped = self.offset() - self.base
        return -stepped / max(self.monotonic() - self.started + stepped, 1) * 1e6

    def offset(self) -> int:
        """CLOCK_REALTIME - CLOCK_MONOTONIC, from the tightest of three readings (a thread
        preempted between the two would read them apart)."""
        best = (0, 0)
        for i in range(3):
            m0, r, m1 = self.monotonic(), self.realtime(), self.monotonic()
            if i == 0 or m1 - m0 < best[0]:
                best = (m1 - m0, r - (m0 + m1) // 2)
        return best[1]

    def now(self) -> int:
        return self.monotonic() + self.base

    def steady(self, wall_ns: int) -> int:
        """A CLOCK_REALTIME time just past (a kernel receive stamp) on this clock."""
        return wall_ns - (self.offset() - self.base)

    def sleep_until(self, t_ns: int) -> None:
        """Sleep to `t_ns` on this clock; spin the last millisecond for precision."""
        while (left := t_ns - self.now()) > 1_000_000:
            self.sleep((left - 1_000_000) / 1e9)
        while self.now() < t_ns:
            pass


CLOCK = Clock()


@contextmanager
def watch(clock: Clock = CLOCK, every_s: float = WATCH_S) -> Iterator[list[dict[str, Any]]]:
    """Meanwhile, log each step of CLOCK_REALTIME: its size and the window of capture times it
    may lie in (between two readings; what was stamped there, before or after it, is
    ambiguous)."""
    steps: list[dict[str, Any]] = []
    stop = threading.Event()

    def run() -> None:
        m0, o0 = clock.monotonic(), clock.offset()
        while not stop.wait(every_s):
            m1, o1 = clock.monotonic(), clock.offset()
            if abs(o1 - o0) >= STEP_NS:
                window = [m0 + min(o0, o1), m1 + max(o0, o1)]
                steps.append({"wall_ns": window, "step_ms": (o1 - o0) / 1e6})
            m0, o0 = m1, o1

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    try:
        yield steps
    finally:
        stop.set()
        thread.join()


def spans(a: int, b: int, steps: list[dict[str, Any]], bar_ms: float = 0.0) -> bool:
    """Whether the capture-time interval [a, b] may hold one of `steps` that matters to a
    timing whose error bar is `bar_ms` wide (STEP_SHARE)."""
    lo, hi = min(a, b), max(a, b)
    return any(
        lo <= s["wall_ns"][1] and hi >= s["wall_ns"][0] and abs(s["step_ms"]) >= STEP_SHARE * bar_ms
        for s in steps
    )


def steps(out: Path) -> list[dict[str, Any]] | None:
    """The steps a results directory's run logged; None if it predates the log."""
    conds = out / "conditions.json"
    return json.loads(conds.read_text()).get("clock_steps") if conds.exists() else None


def note(steps: list[dict[str, Any]] | None) -> str:
    """One line on the wall-clock steps a run saw."""
    if steps is None:
        return "Wall-clock steps during the run: not recorded (the run predates the log).\n"
    if not steps:
        return "Wall-clock steps during the run: none.\n"
    sizes = [s["step_ms"] for s in steps]
    return (
        f"Wall-clock steps during the run: {len(steps)} (median {statistics.median(sizes):+.1f} "
        f"ms, largest {max(sizes, key=abs):+.1f} ms); what was timed across one of at least "
        f"{STEP_SHARE:.0%} of its error bar's width is marked [across a clock step].\n"
    )


def rate_note(out: Path) -> str:
    """A warning when the run's wall clock ran more than RATE_PPM off between its steps (its
    `clock_rate_ppm`); a single step is no rate."""
    path = out / "conditions.json"
    conds = json.loads(path.read_text()) if path.exists() else {}
    ppm, steps = conds.get("clock_rate_ppm"), conds.get("clock_steps") or []
    if ppm is None or abs(ppm) <= RATE_PPM or len(steps) == 1:
        return ""
    text = f"Wall clock: {abs(ppm):,.0f} ppm {'fast' if ppm > 0 else 'slow'} between its steps"
    if len(steps) > 1:
        apart = statistics.median(b["wall_ns"][0] - a["wall_ns"][0] for a, b in pairwise(steps))
        off = abs(ppm) * apart / 1e12
        text += f", {apart / 1e9:.0f} s apart: late reads up to {off:.0f} ms off from that alone"
    return text + " (docs/calibration.md, clock steps and rate).\n"
