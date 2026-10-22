import os
import signal

import pytest

from rtpbench import progress
from rtpbench.progress import Progress, eta, hms


def test_eta_from_the_rate_so_far() -> None:
    assert eta(10.0, 0.0, 4) is None
    assert eta(10.0, 1.0, 4) == 30.0
    assert eta(10.0, 0.5, 2) == 30.0  # half a unit (its turns) counts
    assert eta(10.0, 4.0, 4) == 0.0
    assert hms(3725.4) == "1:02:05"


def _run(monkeypatch: pytest.MonkeyPatch) -> None:
    with Progress() as p:  # pytest's stdout is not a terminal
        p.plan(2)
        p.phase("building images")
        p.unit("clean greeting/good")
        p.turn("turn 1/3")  # too soon after the last line: no line
        monkeypatch.setattr(progress, "QUIET_S", 0.0)
        p.turn("a line that is not a turn")
        p.turn("turn 2/3")
        p.done("pass as expected", True)
        p.unit("clean greeting/stale")
        p.done("pass, expected fail", False)
        p.phase("starting the stack")
        raise RuntimeError("the stack did not start")


def test_without_a_terminal_a_plain_line_per_event(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    with pytest.raises(RuntimeError):
        _run(monkeypatch)
    lines = [line.split(" ", 1)[1] for line in capsys.readouterr().out.splitlines()]
    assert lines[:2] == [
        "building images",
        "[1/2] clean greeting/good: calling",
    ]
    assert lines[2].startswith("[1/2] clean greeting/good: turn 2 of 3 (about 0:00:0")
    assert lines[3].startswith("[1/2] clean greeting/good: pass as expected (about 0:00:0")
    assert lines[5].startswith("FAILED [2/2] clean greeting/stale: pass, expected fail")
    assert lines[6:] == ["starting the stack", "failed while starting the stack after 0:00:00"]
    assert not any(c in "".join(lines) for c in "\r\x1b")


def _terminated(torn_down: list[bool]) -> None:
    with Progress() as p:
        p.phase("calling")
        try:
            os.kill(os.getpid(), signal.SIGTERM)
        finally:
            os.kill(os.getpid(), signal.SIGINT)  # while tearing down
            torn_down.append(True)


def test_sigterm_unwinds_the_run_and_a_second_signal_waits_for_the_teardown(
    capsys: pytest.CaptureFixture[str],
) -> None:
    before = signal.getsignal(signal.SIGTERM)
    torn_down: list[bool] = []
    with pytest.raises(SystemExit) as e:
        _terminated(torn_down)
    assert e.value.code == 128 + signal.SIGTERM
    assert torn_down
    assert "interrupted while calling" in capsys.readouterr().out
    assert signal.getsignal(signal.SIGTERM) == before
