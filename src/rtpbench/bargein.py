"""Barge-in: the shared script, and stop time from the caller's capture.

Each turn the caller speaks a prompt, waits for the agent's reply to start, then cuts in at a
scripted point with an interruption, a backchannel or a cough. The reference agent knows the
same script (same seed): it stops for every interruption and, playing an over-eager agent, for
half of the backchannels and coughs, a known delay after it detects the caller.

Measured, per detector and timing method, from the caller pcap alone: the agent's speech in
progress when the caller's interjection starts (its labelled onset), or paused for less than
1 s, ends at the last detected sample before a silence of at least 1 s. The agent stopped if
that end comes within 2 s of the interjection; stop time is that end minus the interjection
onset, negative when the agent fell silent in a pause the caller cut into. Truth: the last
labelled sample of the agent's reply before its cut that reached the caller.
"""

import json
import random
from pathlib import Path
from typing import Any

from rtpbench import analyze, detect, speechcal
from rtpbench.rtp import FRAME

KINDS = ("interrupt", "backchannel", "cough")
GAP_NS = 1_000_000_000  # silence that ends the agent's speech
STOP_WINDOW_NS = 2_000_000_000
METHOD_DETECTOR = "webrtcvad"  # the detector the per-method table uses


def plan(seed: int, n: int = 1000) -> list[dict[str, Any]]:
    """Per turn: what the caller says, when (s after it hears the agent start), and whether
    and how long after detecting the caller the reference agent stops."""
    rng = random.Random(seed + 2)
    steps = []
    for _ in range(n):
        kind = rng.choices(KINDS, weights=(2, 1, 1))[0]
        steps.append(
            {
                "kind": kind,
                "at_s": rng.uniform(0.5, 2.5),
                "stop": kind == "interrupt" or rng.random() < 0.5,
                "stop_delay_s": rng.uniform(0.1, 1.0),
            }
        )
    return steps


def _segments(st: analyze.Stream, found: list[speechcal.Span], packet: bool) -> list[list[int]]:
    """Detected spans as times, merged across gaps shorter than GAP_NS."""
    segs: list[list[int]] = []
    for a, b in found:
        if packet:
            on, end = st.times[a // FRAME], st.times[(b - 1) // FRAME]
        else:
            on, end = st.time(a, True), st.time(b - 1, False)
        if on is None or end is None:
            continue
        if segs and on - segs[-1][1] < GAP_NS:
            segs[-1][1] = max(segs[-1][1], end)
        else:
            segs.append([on, end])
    return segs


def stop(segs: list[list[int]], t: int) -> int | None:
    """End of the agent speech in progress at t (or paused under GAP_NS), minus t; None if the
    agent had not spoken for GAP_NS."""
    seg = next((s for s in segs if s[0] <= t < s[1] + GAP_NS), None)
    return None if seg is None else seg[1] - t


def turns(run: Path) -> list[dict[str, Any]]:
    caller_log = json.loads((run / "caller.json").read_text())
    agent_path = run / "agent.json"
    agent_log = json.loads(agent_path.read_text()) if agent_path.exists() else None
    cap = analyze.load(run / "caller.pcap")
    pt, seq0 = caller_log["pt"], caller_log["seq0"]
    segs: dict[str, tuple[analyze.Stream, list[list[int]]]] = {}
    for m in analyze.METHODS:
        mode = "wire" if m == "packet" else m
        up, down = analyze.stream(cap.up, pt, mode), analyze.stream(cap.down, pt, mode)
        for d in detect.DETECTORS if m == "wire" else (METHOD_DETECTOR,):
            segs[f"{m}/{d}"] = up, _segments(down, detect.DETECT[d](down.pcm), m == "packet")
    up, down = analyze.stream(cap.up, pt), analyze.stream(cap.down, pt)
    out = []
    for i, c in enumerate(caller_log["turns"]):
        if not c.get("speech"):
            continue  # the agent never replied, so there was nothing to cut into
        rec: dict[str, Any] = {"turn": i, "kind": c["kind"], "clip": c["clip"], "measured_ms": {}}
        for key, (st, s) in segs.items():
            t = st.time(st.index(seq0, c["speech"][0][0]), True)
            gap = None if t is None else stop(s, t)
            rec["measured_ms"][key] = None if gap is None else gap / 1e6
        if agent_log:
            reply = agent_log["turns"][i]
            barge = reply.get("barge", {})
            rec |= {"stopped": "cut" in barge, "stop_delay_ms": barge.get("stop_delay_ns", 0) / 1e6}
            if "cut" in barge:
                a0 = agent_log["seq0"]
                kept = [(a, min(b, barge["cut"])) for a, b in reply["speech"] if a < barge["cut"]]
                said = speechcal._truth(
                    up, [(up.index(seq0, a), up.index(seq0, b)) for a, b in c["speech"]]
                )
                heard = speechcal._truth(
                    down, [(down.index(a0, a), down.index(a0, b)) for a, b in kept]
                )
                if said and heard:
                    rec["truth_ms"] = (heard[1] - said[0]) / 1e6
        out.append(rec)
    return out


def summarize(runs: dict[str, Path]) -> str:
    """Measured stop rate and stop time per interjection kind; with a reference agent's log
    also the error against truth and the stopped-or-not confusion."""
    stat = ["mean", "p5", "p50", "p95", "max abs"]
    measured, errors, confusion = [], [], []
    key = f"wire/{METHOD_DETECTOR}"
    for name, run in runs.items():
        recs = turns(run)
        (run / "turns.jsonl").write_text("".join(json.dumps(r) + "\n" for r in recs))
        for d in detect.DETECTORS:
            for kind in KINDS:
                sel = [r for r in recs if r["kind"] == kind]
                v = [r["measured_ms"][f"wire/{d}"] for r in sel if _stopped(r, f"wire/{d}")]
                cells = [f"{analyze._pct(v, q):.0f}" for q in (0.05, 0.5, 0.95)] if v else ["-"] * 3
                measured.append([name, kind, d, str(len(sel)), str(len(v)), *cells])
        truth = [r for r in recs if "truth_ms" in r]
        if not truth:
            continue
        for k in recs[0]["measured_ms"]:
            got = [r["measured_ms"][k] - r["truth_ms"] for r in truth if _stopped(r, k)]
            errors.append(
                [name, *k.split("/"), f"{len(got)}/{len(truth)}", *speechcal._signed(got)]
            )
        for kind in KINDS:
            for stopped in (True, False):
                sel = [r for r in recs if r["kind"] == kind and r.get("stopped") == stopped]
                said = sum(_stopped(r, key) for r in sel)
                agent = "stopped" if stopped else "continued"
                confusion.append([name, kind, agent, str(len(sel)), str(said)])
    out = "Measured: turns, stopped, stop time p5 / p50 / p95 (ms) of those stopped, wire\n\n"
    out += analyze._table(
        ["run", "interjection", "detector", "turns", "stopped", "p5", "p50", "p95"], measured
    )
    if errors:
        out += (
            "\nBarge-in stop time: measured - truth, ms (agent stopped, rtpbench agrees)\n\n"
            + analyze._table(["run", "method", "detector", "n", *stat], errors)
            + f"\nStopped or not: what the agent did vs what rtpbench measured ({key})\n\n"
            + analyze._table(
                ["run", "interjection", "agent", "turns", "measured stopped"], confusion
            )
        )
    return out


def _stopped(rec: dict[str, Any], key: str) -> bool:
    v = rec["measured_ms"][key]
    return v is not None and v < STOP_WINDOW_NS / 1e6


def pooled(runs: dict[str, list[Path]]) -> str:
    """Barge-in per profile and interjection against a real agent, over every turn of every
    run: how often the agent stopped (and the range of that rate over runs), and its stop time
    by the gate on the wire, with the gate's error bar for the profile and codec."""
    from rtpbench import cases

    key = "wire/gate"
    rows = []
    for profile, dirs in runs.items():
        per_run, bars = [], set()
        for run in dirs:
            recs = turns(run)
            (run / "turns.jsonl").write_text("".join(json.dumps(r) + "\n" for r in recs))
            per_run.append(recs)
            pt = json.loads((run / "caller.json").read_text())["pt"]
            bars.add(cases.bar(cases.STOP, profile, pt))
        error = "; ".join(f"[{b.lo:+.1f}, {b.hi:+.1f}] {b.source}" for b in bars if b) or "-"
        for kind in KINDS:
            sel = [[r for r in recs if r["kind"] == kind] for recs in per_run]
            stopped = [[r for r in s if _stopped(r, key)] for s in sel]
            n, k = sum(map(len, sel)), sum(map(len, stopped))
            rates = [len(t) / len(s) for s, t in zip(sel, stopped, strict=True) if s]
            spread = f"{min(rates):.0%} .. {max(rates):.0%}" if rates else "-"
            v = [r["measured_ms"][key] for t in stopped for r in t]
            cells = [f"{analyze._pct(v, q):.0f}" for q in (0.05, 0.5, 0.95)] if v else ["-"] * 3
            rows.append([profile, kind, str(len(dirs)), f"{k}/{n}", spread, *cells, error])
    head = ["profile", "interjection", "runs", "stopped", "run rates", "p5", "p50", "p95"]
    return (
        "Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop "
        "time (ms, gate, wire) when it did, every turn of every run. True value = measured - "
        "error, error within the bar (calibrated on hard cuts).\n\n"
        + analyze._table([*head, "stop error bar"], rows)
    )
