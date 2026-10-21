import json
from pathlib import Path
from typing import Any

import pytest

from rtpbench import check, cli

PCMU = 0


def _run(
    d: Path,
    verdicts: dict[str, str],
    latency: list[list[float | None]] | None = None,
    stops: list[list[tuple[str, float | None]]] | None = None,
    steps: list[dict[str, Any]] | None = None,
    pt: int = PCMU,
) -> Path:
    """A judged target run: clean only, one repeat per latency or barge-in call."""
    d.mkdir(parents=True)
    conds = {"target": "sip:agent@host", "image": "rtpbench:abc", "clock_steps": steps or []}
    (d / "conditions.json").write_text(json.dumps(conds))
    recs = [
        {"profile": "clean", "repeat": 1, "case": c, "behaviour": None, "verdict": v}
        for c, v in verdicts.items()
    ]
    (d / "results.json").write_text(json.dumps(recs))
    lat: list[list[dict[str, Any]]] = [
        [{"end_ns": i * 10**10, "webrtcvad_ms": t} for i, t in enumerate(c, 1)]
        for c in latency or []
    ]
    barge: list[list[dict[str, Any]]] = [
        [
            {"onset_ns": i * 10**10, "kind": k, "measured_ms": {"wire/gate": t}}
            for i, (k, t) in enumerate(c, 1)
        ]
        for c in stops or []
    ]
    for sub, calls in (("latency", lat), ("barge-in", barge)):
        for k, lines in enumerate(calls, 1):
            run = d / f"clean/{k:02}/{sub}"
            run.mkdir(parents=True)
            (run / "caller.json").write_text(json.dumps({"pt": pt}))
            (run / "turns.jsonl").write_text("".join(json.dumps(x) + "\n" for x in lines))
    return d


def _policy(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "policy.toml"
    path.write_text(text)
    return path


@pytest.mark.parametrize(
    ("text", "error"),
    [
        ("[latncy.clean]\np50 = 1\n", "latncy unknown"),
        ("[cases]\nholdd = 'fail'\n", "holdd unknown"),
        ("[cases]\nhold = 'flaky'\n", "pass or fail"),
        ("[latency.wifi]\np50 = 1\n", "wifi unknown"),
        ("[latency.clean]\np90 = 1\n", "p90 unknown"),
        ("[latency.clean]\np50 = '1'\n", "a finite number"),
        ("[barge-in.clean.interrupt]\nstopped = 2\n", "a share"),
        ("[barge-in.clean.sneeze]\np50 = 1\n", "sneeze unknown"),
        ("[regression]\nlatency = -1\n", "a finite number"),
        ("[regression]\nlatency = inf\n", "a finite number"),
        ("[latency.clean]\np95 = nan\n", "a finite number"),
        ("cases = 'fail'\n", r"\[cases\]: a table"),
        ("latency = 2000\n", r"\[latency\]: a table"),
    ],
)
def test_a_policy_with_an_unknown_name_or_value_is_refused(
    tmp_path: Path, text: str, error: str
) -> None:
    with pytest.raises(check.InputError, match=error):
        check.load(_policy(tmp_path, text))


def test_verdicts_against_the_policy(tmp_path: Path) -> None:
    now = check.measure(_run(tmp_path / "now", {"greeting": "pass", "hold": "fail"}))
    rows, ok = check.evaluate(now, {})
    assert not ok
    assert rows[1][1:3] == ["hold", "FAIL"]
    rows, ok = check.evaluate(now, {"cases": {"hold": "fail"}})
    assert ok
    fixed = check.measure(_run(tmp_path / "fixed", {"greeting": "pass", "hold": "pass"}))
    rows, ok = check.evaluate(fixed, {"cases": {"hold": "fail"}})
    assert ok
    assert rows[1][2] == "note"
    # allowed to fail, but it passed before: a regression all the same
    rows, ok = check.evaluate(now, {"cases": {"hold": "fail"}}, fixed)
    assert not ok
    assert "previous run" in rows[1][3]


def test_a_limit_reads_the_error_bar_in_the_agents_favour(tmp_path: Path) -> None:
    # clean PCMU onset bar: true = measured - error, error up to +44.6 ms
    def latency(ms: float) -> list[list[str]]:
        d = _run(tmp_path / str(ms), {}, latency=[[ms] * 12])
        return check.evaluate(check.measure(d), {"latency": {"clean": {"p50": 2000}}})[0]

    assert latency(2040)[0][2] == "pass"
    assert latency(2050)[0][2] == "FAIL"


def test_unanswered_turns_are_later_than_any_limit(tmp_path: Path) -> None:
    d = _run(tmp_path / "d", {}, latency=[[1000] * 11 + [None]])
    rows, _ = check.evaluate(check.measure(d), {"latency": {"clean": {"p50": 2000, "p95": 2000}}})
    assert [r[2] for r in rows] == ["pass", "FAIL"]


def test_a_limit_on_a_call_not_requested_is_noted_and_on_a_broken_call_fails(
    tmp_path: Path,
) -> None:
    policy = {"latency": {"clean": {"p50": 2000}}, "barge-in": {"clean": {"interrupt": {"p50": 1}}}}
    rows, ok = check.evaluate(check.measure(_run(tmp_path / "none", {"greeting": "pass"})), policy)
    assert ok  # a cases-only run (--only <cases>): one policy serves split runs
    assert [r[1:] for r in rows[1:]] == [
        ["latency", "note", "not requested in this run"],
        ["barge-in", "note", "not requested in this run"],
    ]
    d = _run(tmp_path / "empty", {}, latency=[[]])  # requested, answered no turn
    rows, ok = check.evaluate(check.measure(d), {"latency": {"clean": {"p50": 2000}}})
    assert not ok
    assert rows[0][3] == "p50: no measurement"
    d = _run(tmp_path / "broken", {}, latency=[[1000] * 12])
    (d / "clean/02/latency").mkdir(parents=True)
    (d / "clean/02/latency/error.txt").write_text("refused")
    rows, ok = check.evaluate(check.measure(d), {"latency": {"clean": {"p50": 2000}}})
    assert not ok
    assert rows[0][3] == "1 call(s) did not complete"


def test_barge_in_share_stopped_and_stop_time(tmp_path: Path) -> None:
    stops = [[("interrupt", 200.0)] * 9 + [("interrupt", None), ("cough", 50.0)]]
    d = check.measure(_run(tmp_path / "d", {}, stops=stops))
    limits = {"interrupt": {"stopped": 0.9, "p95": 199}}
    rows, _ = check.evaluate(d, {"barge-in": {"clean": limits}})
    # the stop bar is all below zero: a stop time is read as it was measured
    assert [r[2] for r in rows] == ["pass", "FAIL"]
    assert "stopped 9/10" in rows[0][3]


def test_turns_across_a_clock_step_are_left_out(tmp_path: Path) -> None:
    step = {"wall_ns": [2 * 10**10, 2 * 10**10 + 1], "step_ms": 5.0}  # in turn 2's latency
    d = check.measure(_run(tmp_path / "d", {}, latency=[[1000, 1000, 1000]], steps=[step]))
    assert d["latency"]["clean"]["calls"] == [[1000, 1000]]
    assert d["latency"]["clean"]["stepped"] == 1


def test_regression_beyond_noise_and_tolerance(tmp_path: Path) -> None:
    def calls(base: float) -> list[list[float | None]]:
        return [[base + (7 * i + 3 * k) % 40 for i in range(12)] for k in range(3)]

    before = check.measure(_run(tmp_path / "before", {}, latency=calls(1500)))
    tolerance = {"regression": {"latency": 50}}
    same = check.measure(_run(tmp_path / "same", {}, latency=calls(1500)))
    assert check.evaluate(same, tolerance, before)[1]
    within = check.measure(_run(tmp_path / "within", {}, latency=calls(1530)))
    assert check.evaluate(within, tolerance, before)[1]
    slower = check.measure(_run(tmp_path / "slower", {}, latency=calls(1600)))
    rows, ok = check.evaluate(slower, tolerance, before)
    assert not ok
    assert rows[0][1] == "latency regression"
    # another codec has another error bar: not compared
    pcma = check.measure(_run(tmp_path / "pcma", {}, latency=calls(1600), pt=8))
    rows, ok = check.evaluate(pcma, tolerance, before)
    assert ok
    assert "codec differs" in rows[0][3]


def test_cli_exit_codes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    d = _run(tmp_path / "d", {"greeting": "pass", "hold": "fail"})
    with pytest.raises(SystemExit) as e:
        cli.main(["check", str(d)])
    assert e.value.code == 1
    assert "FAILED: 1 of 2" in capsys.readouterr().out
    cli.main(["check", str(d), "--policy", str(_policy(tmp_path, "[cases]\nhold = 'fail'\n"))])
    assert (d / "check.md").read_text().endswith("Passed.\n")
    assert json.loads((d / "check.json").read_text())["verdicts"]["clean"]["hold"] == ["fail"]
    with pytest.raises(SystemExit) as e:
        cli.main(["check", str(d), "--policy", str(_policy(tmp_path, "[cases]\nx = 'fail'\n"))])
    assert e.value.code == 2
    no_codecs = json.loads((d / "check.json").read_text()) | {"latency": {"clean": {"calls": []}}}
    nan = json.loads((d / "check.json").read_text())
    nan["latency"] = {"clean": {"codecs": [0], "calls": [[float("nan")]]}}
    codecs = nan | {"latency": {"clean": {"codecs": [[0]], "calls": []}}}
    bad = ["[]", "null", json.dumps(no_codecs), json.dumps(nan), json.dumps(codecs)]
    for i, text in enumerate(bad):  # not one; null; no codecs; NaN; codecs not numbers
        (tmp_path / f"previous{i}.json").write_text(text)
    for previous in [*(f"previous{i}.json" for i in range(len(bad))), "missing.json"]:
        with pytest.raises(SystemExit) as e:
            cli.main(["check", str(d), "--previous", str(tmp_path / previous)])
        assert e.value.code == 2
    (tmp_path / "null").mkdir()
    (tmp_path / "null/conditions.json").write_text("{}")
    (tmp_path / "null/results.json").write_text("null")
    for run in ("no-run", "null"):
        with pytest.raises(SystemExit) as e:
            cli.main(["check", str(tmp_path / run)])
        assert e.value.code == 2


def test_too_few_turns_are_not_compared(tmp_path: Path) -> None:
    before = check.measure(_run(tmp_path / "before", {}, latency=[[1500.0] * 5]))
    now = check.measure(_run(tmp_path / "now", {}, latency=[[1900.0] * 5]))
    rows, ok = check.evaluate(now, {"regression": {"latency": 50}}, before)
    assert ok
    assert "5 and 5 turns" in rows[0][3]
