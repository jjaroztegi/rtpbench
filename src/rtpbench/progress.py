"""What a long run is doing and how far along it is: a live status bar on a terminal, a line per
event anywhere else (CI logs, redirects, pipes). Host side only: the captures that time the calls
are taken in the containers, and the bar redraws twice a second at most, from its own thread."""

import re
import signal
import sys
import time
from types import TracebackType

from rich import progress as rp
from rich.console import Console
from rich.markup import escape
from rich.text import Text

QUIET_S = 30.0  # without a terminal, a turn gets a line only after this long without one
_TURN = re.compile(r"turn (\d+)/(\d+)")  # what the caller prints as each turn starts


def eta(elapsed: float, done: float, total: int) -> float | None:
    """Seconds left for `total` units at the rate of the `done` (fractional) done in `elapsed`
    seconds; None before any is done."""
    return elapsed * (total - done) / done if done > 0 else None


def hms(seconds: float) -> str:
    s = round(seconds)
    return f"{s // 3600}:{s // 60 % 60:02d}:{s % 60:02d}"


def _stop(signum: int, _frame: object) -> None:
    """SIGINT and SIGTERM (systemd stop, a cancelled CI job, kill) unwind the run the same way,
    so its `finally` blocks tear the stack down and hand the results back. A second signal
    meanwhile would cut that short and leave containers and root-owned files behind."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    raise SystemExit(128 + signum)


class Progress:
    """Units of work (calls) out of `plan`'s total: `unit` starts one, `turn` takes the caller's
    output while it runs, `done` ends it; `phase` names what happens outside units. As a context
    manager it draws the bar (on a terminal), says where a run failed, and turns SIGINT and
    SIGTERM into a clean exit that runs the run's teardown."""

    def __init__(self) -> None:
        self.t0 = time.monotonic()
        self.total = self.k = 0  # units planned, started
        self.done_units = 0.0  # with the current one's turns as a fraction
        self.label = ""  # the current unit or phase
        self.turns: tuple[int, int] | None = None  # the current unit's turn, of how many
        self.unit_t = self.first_t = self.said_t = 0.0
        self.end_t: float | None = None  # when the run should end, at the rate so far
        console = Console(highlight=False)
        # rich's own test honours TERM=dumb and TTY_INTERACTIVE; FORCE_COLOR into a file must
        # still not redraw
        self.bar = None
        if console.is_interactive and sys.stdout.isatty():
            self.bar = rp.Progress(
                rp.SpinnerColumn(),
                rp.TextColumn("{task.description}"),
                rp.BarColumn(),
                rp.MofNCompleteColumn(),
                rp.TimeElapsedColumn(),
                _Left(self),
                console=console,
                transient=True,
                refresh_per_second=2,
            )
            self.task = self.bar.add_task("", total=None)

    def __enter__(self) -> Progress:
        self.was = [signal.signal(s, _stop) for s in (signal.SIGINT, signal.SIGTERM)]
        if self.bar:
            self.bar.start()
        return self

    def __exit__(
        self, exc: type[BaseException] | None, _v: BaseException | None, _t: TracebackType | None
    ) -> None:
        took = hms(time.monotonic() - self.t0)
        if exc:
            how = "interrupted" if issubclass(exc, KeyboardInterrupt | SystemExit) else "failed"
            self._event(False, f"{how} while {self.label or 'starting'}", f"after {took}")
        else:
            self._event(True, "finished", f"in {took}")
        if self.bar:
            self.bar.stop()
        for s, handler in zip((signal.SIGINT, signal.SIGTERM), self.was, strict=True):
            signal.signal(s, handler)

    def plan(self, total: int) -> None:
        self.total = total
        if self.bar:
            self.bar.update(self.task, total=total)

    def phase(self, text: str) -> None:
        self.label, self.turns = text, None
        self._say(text)
        self._draw()

    def unit(self, label: str) -> None:
        self.k += 1
        self.label, self.turns = label, None
        self.unit_t = time.monotonic()
        self.first_t = self.first_t or self.unit_t  # the rate leaves out building and starting
        self._say(f"{self._of()} {label}: calling")
        self._draw()

    def turn(self, line: str) -> None:
        """A line of the caller's output; those that say a turn started move the bar."""
        if not (m := _TURN.fullmatch(line.strip())):
            return
        k, n = self.turns = int(m[1]), int(m[2])
        self._estimate(self.k - 1 + (k - 1) / n)
        if time.monotonic() - self.said_t >= QUIET_S:
            left = self.left()
            self._say(
                f"{self._of()} {self.label}: turn {k} of {n}" + (f" ({left})" if left else "")
            )
        self._draw()

    def done(self, text: str = "", ok: bool | None = None) -> None:
        """The unit ended with `text`; `ok`: whether that is what it should be (None: no
        judgement)."""
        text = text or (f"{self.turns[1]} turns" if self.turns else "done")
        self._estimate(self.k)
        if self.bar:
            self._event(ok, f"{self.label}  {text}", hms(time.monotonic() - self.unit_t))
        else:
            left = self.left()
            line = f"{self._of()} {self.label}: {text}" + (f" ({left})" if left else "")
            self._say(line if ok is not False else f"FAILED {line}")
        self._draw()

    def left(self) -> str:
        if self.end_t is None or self.done_units >= self.total:
            return ""
        return f"about {hms(max(0.0, self.end_t - time.monotonic()))} left"

    def _of(self) -> str:
        return f"[{self.k}/{self.total}]"

    def _estimate(self, done: float) -> None:
        now = time.monotonic()
        self.done_units = done
        left = eta(now - self.first_t, done, self.total)
        self.end_t = None if left is None else now + left  # counts down between estimates

    def _say(self, line: str) -> None:
        """A line of the log, without a terminal (on one the bar shows the same)."""
        if not self.bar:
            print(f"{hms(time.monotonic() - self.t0)} {line}", flush=True)
            self.said_t = time.monotonic()

    def _event(self, ok: bool | None, text: str, note: str) -> None:
        """A line that stays: above the bar on a terminal, else in the log."""
        if not self.bar:
            self._say(f"{text} {note}")
            return
        mark = {True: "[green]✓[/]", False: "[red]✗[/]", None: "[dim]·[/]"}[ok]
        self.bar.console.print(f"{mark} {escape(text)}  [dim]{escape(note)}[/]")

    def _draw(self) -> None:
        if self.bar:
            turn = f" · turn {self.turns[0]} of {self.turns[1]}" if self.turns else ""
            self.bar.update(self.task, description=self.label + turn, completed=self.done_units)


class _Left(rp.ProgressColumn):
    """Time left, counting down between the estimates units and turns make."""

    def __init__(self, progress: Progress) -> None:
        super().__init__()
        self.progress = progress

    def render(self, task: rp.Task) -> Text:
        return Text(self.progress.left(), style="progress.remaining")
