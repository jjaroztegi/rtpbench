"""`rtpbench check`: pass or fail a target run against a policy, for CI.

A policy (TOML) sets which cases may fail, limits on turn latency and barge-in per profile, and
how far they may grow from an earlier run's check.json. Limits read the error bar in the
agent's favour: a percentile fails only when even the lowest true value its bar allows is over.
A regression fails only when the change in median is over the tolerance across its whole 95%
interval, resampling calls and then turns within them: turn-to-turn and call-to-call noise
stays inside it, and the bars, the same for both runs of a profile and codec, cancel.
"""

import json
import math
import random
import statistics
import tomllib
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

from rtpbench import analyze, bargein, cases, clock

PROFILE_KEYS = {"p50": 0.5, "p95": 0.95}
RESAMPLES = 2000
# fewer turns a side and the interval is too narrow to hold the noise: on the baseline, single
# barge-in calls (2-5 of each interjection) failed up to 7% of unchanged comparisons
MIN_TURNS = 10


class PolicyError(ValueError):
    pass


def load(path: Path) -> dict[str, Any]:
    """The policy at `path`, refused whole on any unknown name: a typo must not turn a limit
    off."""
    from rtpbench.bench import PROFILES

    try:
        policy = tomllib.loads(path.read_text())
    except tomllib.TOMLDecodeError as e:
        raise PolicyError(f"{path}: {e}") from e
    _known(policy, {"cases", "latency", "barge-in", "regression"}, "")
    for case, want in policy.get("cases", {}).items():
        if case not in cases.CASES:
            raise PolicyError(f"[cases] {case}: not a case ({', '.join(cases.CASES)})")
        if want not in ("pass", "fail"):
            raise PolicyError(f"[cases] {case} = {want!r}: pass or fail")
    for profile, limits in policy.get("latency", {}).items():
        _profile(profile, PROFILES)
        _limits(limits, PROFILE_KEYS, f"[latency.{profile}]")
    for profile, kinds in policy.get("barge-in", {}).items():
        _profile(profile, PROFILES)
        _known(kinds, set(bargein.KINDS), f"[barge-in.{profile}]")
        for kind, limits in kinds.items():
            _limits(limits, {**PROFILE_KEYS, "stopped": 1}, f"[barge-in.{profile}.{kind}]")
            if not 0 <= limits.get("stopped", 0) <= 1:
                raise PolicyError(f"[barge-in.{profile}.{kind}] stopped: a share, 0 to 1")
    _limits(policy.get("regression", {}), {"latency": 1, "barge-in": 1}, "[regression]")
    return policy


def _known(table: Any, names: set[str], where: str) -> None:
    if not isinstance(table, dict):
        raise PolicyError(f"{where or 'policy'}: a table")
    if unknown := sorted(set(table) - names):
        known = ", ".join(sorted(names))
        raise PolicyError(f"{where or 'policy'}: {', '.join(unknown)} unknown (known: {known})")


def _profile(profile: str, profiles: dict[str, str]) -> None:
    if profile not in profiles:
        raise PolicyError(f"{profile}: not a profile ({', '.join(profiles)})")


def _limits(limits: Any, keys: dict[str, float], where: str) -> None:
    _known(limits, set(keys), where)
    for key, v in limits.items():
        if isinstance(v, bool) or not isinstance(v, int | float) or v < 0:
            raise PolicyError(f"{where} {key} = {v!r}: a number, 0 or more")


def _lines(path: Path) -> Iterator[dict[str, Any]]:
    return (json.loads(line) for line in path.read_text().splitlines() if line)


def measure(out: Path) -> dict[str, Any]:
    """What a judged target run directory holds that a policy reads: verdicts per profile and
    case over the repeats, and per profile each latency and barge-in call's turns (ms; None
    unanswered or not stopped), leaving out turns timed across a clock step; check.json."""
    conds = json.loads((out / "conditions.json").read_text())
    records = json.loads((out / "results.json").read_text())
    if any(r["behaviour"] for r in records):
        raise PolicyError(f"{out}: a cases run (the reference agent); check judges a target run")
    steps = clock.steps(out) or []
    verdicts: dict[str, dict[str, list[str]]] = {}
    for r in sorted(records, key=lambda r: r["repeat"]):
        verdicts.setdefault(r["profile"], {}).setdefault(r["case"], []).append(r["verdict"])
    latency: dict[str, dict[str, Any]] = {}
    barge: dict[str, dict[str, Any]] = {}
    for sub, into in (("latency", latency), ("barge-in", barge)):
        for run in sorted(out.glob(f"*/*/{sub}")):
            entry = into.setdefault(run.parts[-3], {"codecs": [], "stepped": 0, "broken": 0})
            if not (run / "turns.jsonl").exists():  # the call did not complete (error.txt)
                entry["broken"] += 1
                continue
            entry["codecs"].append(json.loads((run / "caller.json").read_text())["pt"])
            if sub == "latency":
                turns = []
                for t in _lines(run / "turns.jsonl"):
                    ms = t["webrtcvad_ms"]
                    if ms is not None and clock.spans(t["end_ns"], t["end_ns"] + ms * 1e6, steps):
                        entry["stepped"] += 1
                    else:
                        turns.append(ms)
                entry.setdefault("calls", []).append(turns)
                continue
            kinds: dict[str, list[float | None]] = {k: [] for k in bargein.KINDS}
            for t in _lines(run / "turns.jsonl"):
                ms = t["measured_ms"]["wire/gate"] if bargein._stopped(t, "wire/gate") else None
                if ms is not None and clock.spans(t["onset_ns"], t["onset_ns"] + ms * 1e6, steps):
                    entry["stepped"] += 1
                else:
                    kinds[t["kind"]].append(ms)
            for kind, stops in kinds.items():
                entry.setdefault("kinds", {}).setdefault(kind, []).append(stops)
    return {
        "target": conds.get("target"),
        "image": conds.get("image"),
        "lines": conds.get("lines"),
        "verdicts": verdicts,
        "latency": latency,
        "barge-in": barge,
    }


def _hi(table: dict[tuple[str, int], cases.Bar], profile: str, codecs: list[int]) -> float:
    """The error bar's upper end for the profile, the widest over the calls' codecs."""
    return max((b.hi for pt in set(codecs) if (b := cases.bar(table, profile, pt))), default=0.0)


def _flat(calls: list[list[float | None]], missing: float | None) -> list[float]:
    """Every turn's value; None as `missing`, or left out when `missing` is None."""
    out = [missing if v is None else v for c in calls for v in c]
    return [v for v in out if v is not None]


def _over(values: list[float], limits: dict[str, float], hi: float) -> Iterator[tuple[bool, str]]:
    """Each percentile limit: whether it holds, with the measurement as the detail."""
    for key, limit in limits.items():
        if key not in PROFILE_KEYS:
            continue
        if not values:
            yield False, f"{key}: no measurement"
            continue
        v = analyze._pct(values, PROFILE_KEYS[key])
        least = v - hi  # the lowest true value the error bar allows
        yield least <= limit, f"{key} {v:.0f} ms (at least {least:.0f}), limit {limit:g}"


def _shift(
    before: list[list[float]], now: list[list[float]], rng: random.Random
) -> tuple[float, float, float]:
    """The change in median turn from `before` to `now` (lists of calls' turns), and its 95%
    interval: each resample draws calls with replacement, then turns within each drawn call."""

    def draw(calls: list[list[float]]) -> float:
        picked = [rng.choice(calls) for _ in calls]
        return statistics.median(rng.choice(c) for c in picked for _ in c)

    d = statistics.median(x for c in now for x in c) - statistics.median(
        x for c in before for x in c
    )
    shifts = sorted(draw(now) - draw(before) for _ in range(RESAMPLES))
    return d, analyze._pct(shifts, 0.025), analyze._pct(shifts, 0.975)


def _series(entry: dict[str, Any], sub: str) -> dict[str, list[list[float | None]]]:
    """A latency entry's calls, or a barge-in entry's per interjection."""
    return {"": entry.get("calls", [])} if sub == "latency" else entry.get("kinds", {})


def _calls(calls: list[list[float | None]], missing: float | None) -> list[list[float]]:
    return [t for c in calls if (t := _flat([c], missing))]


def _stepped(
    row: Callable[[str, str, bool | None, str], None], profile: str, sub: str, entry: dict[str, Any]
) -> None:
    if entry["stepped"]:
        row(profile, sub, None, f"{entry['stepped']} turn(s) across a clock step, left out")


def evaluate(
    now: dict[str, Any], policy: dict[str, Any], before: dict[str, Any] | None = None
) -> tuple[list[list[str]], bool]:
    """Rows (profile, check, result, detail) and whether the run passes the policy."""
    rows: list[list[str]] = []

    def row(profile: str, what: str, ok: bool | None, detail: str) -> None:
        rows.append([profile, what, {True: "pass", False: "FAIL", None: "note"}[ok], detail])

    expect = policy.get("cases", {})
    was = (before or {}).get("verdicts", {})
    for profile, by_case in now["verdicts"].items():
        for case, got in by_case.items():
            mix = cases.verdicts([{"verdict": v} for v in got])
            passed = all(v == "pass" for v in got)
            if expect.get(case, "pass") == "pass":
                row(profile, case, passed, mix + ("" if passed else ", expected to pass"))
            elif passed:
                row(profile, case, None, f"{mix}, allowed to fail: the policy can expect a pass")
            elif (prev := was.get(profile, {}).get(case)) and all(v == "pass" for v in prev):
                row(profile, case, False, f"{mix}, allowed to fail, but passed in the previous run")
            else:
                row(profile, case, True, f"{mix}, allowed to fail")

    for profile, limits in policy.get("latency", {}).items():
        entry = now["latency"].get(profile)
        if not entry:
            row(profile, "latency", False, "not measured")
            continue
        if entry["broken"]:
            row(profile, "latency", False, f"{entry['broken']} call(s) did not complete")
        _stepped(row, profile, "latency", entry)
        values = _flat(entry.get("calls", []), math.inf)  # unanswered: later than any limit
        hi = _hi(cases.ONSET, profile, entry["codecs"])
        for ok, detail in _over(values, limits, hi):
            row(profile, "latency", ok, detail)

    for profile, kinds in policy.get("barge-in", {}).items():
        entry = now["barge-in"].get(profile)
        if not entry:
            row(profile, "barge-in", False, "not measured")
            continue
        if entry["broken"]:
            row(profile, "barge-in", False, f"{entry['broken']} call(s) did not complete")
        _stepped(row, profile, "barge-in", entry)
        hi = _hi(cases.STOP, profile, entry["codecs"])
        for kind, limits in kinds.items():
            turns = entry.get("kinds", {}).get(kind, [])
            said, stops = _flat(turns, math.inf), _flat(turns, None)
            if "stopped" in limits:
                share = len(stops) / len(said) if said else 0.0
                detail = f"stopped {len(stops)}/{len(said)}, at least {limits['stopped']:.0%}"
                row(profile, f"barge-in {kind}", bool(said) and share >= limits["stopped"], detail)
            for ok, detail in _over(stops, limits, hi):
                row(profile, f"barge-in {kind}", ok, f"stop time {detail}")

    tolerance = policy.get("regression", {})
    if tolerance and before is None:
        row("", "regression", None, "no --previous to compare with")
    if before is not None and tolerance:
        rng = random.Random(1)
        differ = [k for k in ("image", "lines") if now.get(k) != before.get(k)]
        for sub in ("latency", "barge-in"):
            if sub not in tolerance:
                continue
            for profile, entry in now[sub].items():
                prev = before[sub].get(profile)
                if not prev:
                    row(profile, f"{sub} regression", None, "not in the previous run")
                    continue
                if differ or set(entry["codecs"]) != set(prev["codecs"]):
                    diff = ", ".join(differ) or "codec"
                    row(profile, f"{sub} regression", None, f"not compared: {diff} differs")
                    continue
                missing = math.inf if sub == "latency" else None
                old = _series(prev, sub)
                for kind, calls in _series(entry, sub).items():
                    a, b = _calls(old.get(kind, []), missing), _calls(calls, missing)
                    what = " ".join(filter(None, (sub, kind, "regression")))
                    n = [sum(map(len, a)), sum(map(len, b))]
                    if min(n) < MIN_TURNS:
                        detail = f"not compared: {n[0]} and {n[1]} turns, under {MIN_TURNS} a side"
                        row(profile, what, None, detail)
                        continue
                    d, lo, hi = _shift(a, b, rng)
                    ok = not lo > tolerance[sub]
                    detail = (
                        f"p50 {d:+.0f} ms (95% interval {lo:+.0f} .. {hi:+.0f}), "
                        f"tolerance +{tolerance[sub]:g}"
                    )
                    row(profile, what, ok, detail)
    return rows, all(r[2] != "FAIL" for r in rows)


def check(out: Path, policy: Path | None, previous: Path | None) -> tuple[str, bool]:
    """Judge the target run in `out` against `policy` (default: every case passes) and the
    check.json `previous`: writes check.md and check.json in `out`; returns check.md and
    whether it passed."""
    rules = load(policy) if policy else {}
    now = measure(out)
    before = json.loads(previous.read_text()) if previous else None
    rows, ok = evaluate(now, rules, before)
    failed = sum(r[2] == "FAIL" for r in rows)
    text = "## Check\n\n" + f"Policy: {policy.name if policy else 'every case passes'}"
    text += f"; previous run: {previous.name}.\n\n" if previous else ".\n\n"
    text += analyze._table(["profile", "check", "result", "detail"], rows)
    text += "\nPassed.\n" if ok else f"\nFAILED: {failed} of {len(rows)}.\n"
    (out / "check.md").write_text(text)
    (out / "check.json").write_text(json.dumps(now, indent=1))
    return text, ok
