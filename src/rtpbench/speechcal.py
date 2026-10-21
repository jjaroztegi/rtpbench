"""Speech-detection error against labelled speech, from the caller's capture alone.

The reference agent replies with labelled clips and logs where each sits in its stream; the
caller logs where its own utterances sit. All times come from the caller pcap (wire method).
Truth is the first / last labelled sample that arrived. Per detector:

  latency  turn latency measured blind (the caller's labelled end to the first detected agent
           speech after it) minus the truth (to the agent's first labelled sample)
  offset   last detected sample of the speech around a labelled clip minus its last labelled
           sample; likewise onset and offset of the caller's own utterances (uplink)
  rec      turn latency as a two-channel recording at the caller reads it: the caller's end and
           the agent's onset both detected, the agent's channel timed as the wire, a jitter
           buffer (rtp) or a recorder appending payloads as they arrive (concat) places it
  agent    the truth measured on the agent's capture instead, as an agent-side log sees a turn

A detected span belongs to a clip if it overlaps the clip's labelled speech widened by 300 ms.
"""

import json
import statistics
from pathlib import Path
from typing import Any

from rtpbench import analyze, detect, speech

WIDEN = 2400  # samples
ALIGN = 1280  # samples, a whole number of every detector's frames: they keep the stream's grid
Span = tuple[int, int]


def _truth(st: analyze.Stream, spans: list[Span]) -> tuple[int, int] | None:
    """Times of the first and last labelled samples whose packets arrived."""
    on = off = None
    slots = [(a, b, k) for a, b in spans for k in range(a // 160, (b - 1) // 160 + 1)]
    for a, _b, k in slots:
        if 0 <= k < len(st.times) and st.times[k] is not None:
            on = st.time(max(a, k * 160), True)
            break
    for _a, b, k in reversed(slots):
        if 0 <= k < len(st.times) and st.times[k] is not None:
            off = st.time(min(b, (k + 1) * 160) - 1, False)
            break
    return (on, off) if on is not None and off is not None else None


def _edges(
    st: analyze.Stream, found: list[Span], spans: list[Span]
) -> tuple[int | None, int | None]:
    """Times of the first and last detected samples around labelled `spans`."""
    lo, hi = spans[0][0] - WIDEN, spans[-1][1] + WIDEN
    near = [s for s in found if s[1] > lo and s[0] < hi]
    if not near:
        return None, None
    return st.time(near[0][0], True), st.time(near[-1][1] - 1, False)


def _first(
    down: analyze.Stream, detector: str, agent_log: dict[str, Any], i: int, reply: list[Span]
) -> int | None:
    """Time of the first speech `detector` finds in reply `i` when it starts listening in the
    agent's silence just before it: as on a stream's first speech, with nothing heard before."""
    k0 = down.index(agent_log["seq0"], agent_log["turns"][i]["start"]) // ALIGN * ALIGN
    starts = (
        down.time(k0 + a, True) for a, _ in detect.DETECT[detector](down.pcm[k0 : reply[-1][1]])
    )
    return next((t for t in starts if t), None)


def _after(st: analyze.Stream, found: list[Span], t: int | None, until: int | None) -> int | None:
    """Time of the first detected onset after `t` and before `until`."""
    starts = (st.time(a, True) for a, _ in found)
    return next((x for x in starts if t and x and x > t and (until is None or x < until)), None)


def _ms(a: int | None, b: int | None) -> float | None:
    return None if a is None or b is None else (a - b) / 1e6


def turns(run: Path, detectors: tuple[str, ...] = detect.DETECTORS) -> list[dict[str, Any]]:
    """Per caller turn and detector: blind latency, and caller onset/offset error; with a
    reference agent's log also the truth and the agent offset error."""
    caller_log = json.loads((run / "caller.json").read_text())
    agent_path = run / "agent.json"
    agent_log = json.loads(agent_path.read_text()) if agent_path.exists() else None
    cap = analyze.load(run / "caller.pcap")
    pt = caller_log["pt"]
    up, down = analyze.stream(cap.up, pt), analyze.stream(cap.down, pt)
    found = {d: (up.detect(detect.DETECT[d]), down.detect(detect.DETECT[d])) for d in detectors}
    rtp, concat = analyze.stream(cap.down, pt, "rtp"), analyze.stream(cap.down, pt, "concat")
    heard = {  # the agent's channel per recording; rtp has the wire's audio on its own clock
        d: {
            "wire": (down, fd),
            "rtp": (rtp, rtp.detect(detect.DETECT[d])),  # its pauses where the clock has them
            "concat": (concat, detect.DETECT[d](concat.pcm)),
        }
        for d, (_, fd) in found.items()
    }

    def place(st: analyze.Stream, seq0: int, spans: list[list[int]]) -> list[Span]:
        return [(st.index(seq0, a), st.index(seq0, b)) for a, b in spans]

    said = [place(up, caller_log["seq0"], t["speech"]) for t in caller_log["turns"]]
    replies = (
        [place(down, agent_log["seq0"], t["speech"]) for t in agent_log["turns"]]
        if agent_log
        else []
    )
    if agent_log and len(replies) != len(said):
        raise ValueError(f"{run}: agent answered {len(replies)} turns, caller spoke {len(said)}")
    said_t = [_truth(up, s) for s in said]
    if agent_log and (run / "agent.pcap").exists():
        mine = analyze.load(run / "agent.pcap")
        a_up, a_down = analyze.stream(mine.up, pt), analyze.stream(mine.down, pt)
        ends = [
            _truth(a_up, place(a_up, caller_log["seq0"], t["speech"])) for t in caller_log["turns"]
        ]
        onsets = [
            _truth(a_down, place(a_down, agent_log["seq0"], t["speech"]))
            for t in agent_log["turns"]
        ]
    else:
        ends = onsets = []
    out = []
    for i, c in enumerate(said):
        ct = said_t[i]
        at = _truth(down, replies[i]) if replies else None
        if ct is None or (replies and at is None):
            continue
        later = said_t[i + 1] if i + 1 < len(said) else None
        nxt = later[0] if later else None
        rec: dict[str, Any] = {
            "turn": i,
            "caller_clip": caller_log["turns"][i].get("clip"),
            "end_ns": ct[1],  # capture time of the caller's labelled end, the latency's start
        }
        if agent_log and at:
            rec |= {"agent_clip": agent_log["turns"][i]["clip"], "truth_ms": (at[0] - ct[1]) / 1e6}
        if ends and (e := ends[i]) and (o := onsets[i]):
            rec["agent_ms"] = (o[0] - e[1]) / 1e6
        for d, (fu, fd) in found.items():
            on = _after(down, fd, ct[1], nxt)
            c_on, c_off = _edges(up, fu, c)
            c_next = _edges(up, fu, said[i + 1])[0] if i + 1 < len(said) else None
            for m, (st, spans) in heard[d].items():
                rec[f"{d}_rec_{m}_ms"] = _ms(_after(st, spans, c_off, c_next), c_off)
            rec |= {
                f"{d}_ms": _ms(on, ct[1]),
                f"{d}_caller_onset_ms": _ms(c_on, ct[0]),
                f"{d}_caller_offset_ms": _ms(c_off, ct[1]),
            }
            if at and agent_log:
                rec[f"{d}_offset_ms"] = _ms(_edges(down, fd, replies[i])[1], at[1])
                rec[f"{d}_first_ms"] = _ms(_first(down, d, agent_log, i, replies[i]), ct[1])
        out.append(rec)
    return out


def _signed(v: list[float]) -> list[str]:
    """Mean, 5th, 50th and 95th percentile, max magnitude."""
    if not v:
        return ["-"] * 5
    pct = [f"{analyze._pct(v, q):+.1f}" for q in (0.05, 0.5, 0.95)]
    return [f"{sum(v) / len(v):+.1f}", *pct, f"{max(abs(x) for x in v):.1f}"]


def sensitivity(clips: dict[str, list[int]]) -> str:
    """How far the labels move when the threshold moves 5 dB either way (clips too noisy to
    label at the lower threshold are left out)."""
    rows = []
    base = {n: speech.label(pcm) for n, pcm in clips.items()}
    for db in (speech.BELOW_ACTIVE_DB - 5, speech.BELOW_ACTIVE_DB + 5):
        on, off = [], []
        for n, pcm in clips.items():
            try:
                alt = speech.label(pcm, db)
            except ValueError:
                continue
            on.append(abs(alt[0][0] - base[n][0][0]) / 8)
            off.append(abs(alt[-1][1] - base[n][-1][1]) / 8)
        stats = [f"{analyze._pct(v, q):.1f}" for v in (on, off) for q in (0.5, 0.9)]
        rows.append([f"{db:.0f} dB", str(len(on)), *stats, f"{max(on):.1f}", f"{max(off):.1f}"])
    head = ["threshold", "clips", "onset p50", "onset p90", "offset p50", "offset p90"]
    return analyze._table([*head, "onset max", "offset max"], rows)


def summarize(runs: dict[str, list[Path]], clips: dict[str, list[int]] | None = None) -> str:
    """With a reference agent: detection error per detector. Against a real agent: turn
    latency per detector, whose error the calibration gives. The runs under one name (one per
    seed) pool into one row."""
    stat = ["mean", "p5", "p50", "p95", "max abs"]
    tables: dict[str, list[list[str]]] = {
        k: [] for k in ("latency", "first", "offset", "caller", "raw")
    }

    def values(recs: list[dict[str, Any]], key: str) -> list[float]:
        return [r[key] for r in recs if r.get(key) is not None]

    for name, dirs in runs.items():
        recs = []
        for run in dirs:
            part = turns(run)
            (run / "turns.jsonl").write_text("".join(json.dumps(r) + "\n" for r in part))
            recs += part
        for d in detect.DETECTORS:
            if any("truth_ms" in r for r in recs):
                err = [r[f"{d}_ms"] - r["truth_ms"] for r in recs if r[f"{d}_ms"] is not None]
                first = [
                    r[f"{d}_first_ms"] - r["truth_ms"]
                    for r in recs
                    if r.get(f"{d}_first_ms") is not None
                ]
                off = values(recs, f"{d}_offset_ms")
                tables["latency"].append([name, d, f"{len(err)}/{len(recs)}", *_signed(err)])
                tables["first"].append([name, d, f"{len(first)}/{len(recs)}", *_signed(first)])
                tables["offset"].append([name, d, f"{len(off)}/{len(recs)}", *_signed(off)])
            raw = values(recs, f"{d}_ms")
            cells = [f"{analyze._pct(raw, q):.1f}" for q in (0.05, 0.5, 0.95)] if raw else ["-"] * 3
            tables["raw"].append([name, d, f"{len(raw)}/{len(recs)}", *cells])
            c_on, c_off = (
                values(recs, f"{d}_caller_onset_ms"),
                values(recs, f"{d}_caller_offset_ms"),
            )
            tables["caller"].append(
                [name, d, f"{len(c_on)}/{len(recs)}", *_signed(c_on)[:4], *_signed(c_off)[:4]]
            )
    out = (
        "Turn latency, ms: caller's labelled end to the first agent speech detected after it\n\n"
        + analyze._table(["run", "detector", "n", "p5", "p50", "p95"], tables["raw"])
    )
    if tables["latency"]:
        out += (
            "\nAgent reply onset: blind turn latency - truth, ms\n\n"
            + analyze._table(["run", "detector", "n", *stat], tables["latency"])
            + "\nAgent reply onset as a stream's first speech (detector started on the reply):"
            + " blind turn latency - truth, ms\n\n"
            + analyze._table(["run", "detector", "n", *stat], tables["first"])
            + "\nAgent reply offset: detected - labelled, ms\n\n"
            + analyze._table(["run", "detector", "n", *stat], tables["offset"])
        )
    out += "\nCaller utterance onset | offset: detected - labelled, ms\n\n" + analyze._table(
        ["run", "detector", "n", *stat[:4], *stat[:4]], tables["caller"]
    )
    if clips:
        out += "\nLabel definition: |label at threshold - label at 35 dB|, ms\n\n" + sensitivity(
            clips
        )
    return out


def pooled(
    runs: dict[str, list[Path]],
    steps: list[dict[str, Any]] | None = None,
    detector: str = "webrtcvad",
) -> str:
    """Turn latency per profile against a real agent, over every turn of every run: the
    caller's labelled end to the agent's first onset by `detector`, the spread of the per-run
    medians, the detector's error bar for the profile and codec, and how many turns ran across
    one of the wall-clock `steps`."""
    from rtpbench import cases, clock

    rows = []
    for profile, dirs in runs.items():
        per_run, said, bars, stepped = [], 0, set(), 0
        for run in dirs:
            recs = turns(run, (detector,))
            (run / "turns.jsonl").write_text("".join(json.dumps(r) + "\n" for r in recs))
            said += len(recs)
            got = [r for r in recs if r[f"{detector}_ms"] is not None]
            per_run.append([r[f"{detector}_ms"] for r in got])
            pt = json.loads((run / "caller.json").read_text())["pt"]
            b = cases.bar(cases.ONSET, profile, pt)
            bars.add(b)
            width = b.hi - b.lo if b else 0
            stepped += sum(
                clock.spans(
                    r["end_ns"], r["end_ns"] + round(r[f"{detector}_ms"] * 1e6), steps or [], width
                )
                for r in got
            )
        v = [x for xs in per_run for x in xs]
        meds = [statistics.median(xs) for xs in per_run if xs]
        cells = [f"{analyze._pct(v, q):.0f}" for q in (0.05, 0.5, 0.95)] if v else ["-"] * 3
        spread = f"{min(meds):.0f} .. {max(meds):.0f}" if meds else "-"
        error = "; ".join(f"[{b.lo:+.1f}, {b.hi:+.1f}] {b.source}" for b in bars if b)
        rows.append(
            [profile, str(len(dirs)), f"{len(v)}/{said}", *cells, spread, str(stepped), error]
        )
    head = ["profile", "runs", "answered", "p5", "p50", "p95", "run medians"]
    head += ["across a clock step", "onset error bar"]
    return (
        f"Turn latency, ms: caller's labelled end to the agent's first speech ({detector}), every "
        "turn of every run. True value = measured - error, error within the onset bar; where the "
        "caller's speech ends is defined to ±17 ms (label threshold ±5 dB).\n\n"
        + analyze._table(head, rows)
    )


METHODS = (  # how a turn's latency is measured, and the per-turn key it lands in
    ("rtpbench: wire, labelled end, webrtcvad onset", "webrtcvad_ms"),
    ("the agent's capture, labelled: an agent-side log", "agent_ms"),
    *((f"recording, {d} at both edges", f"{d}_rec_rtp_ms") for d in detect.DETECTORS[1:]),
    ("recording appending payloads as they arrive, webrtcvad", "webrtcvad_rec_concat_ms"),
)
GAP_MS = 500  # Coval's Latency counts only silences at least this long


def methods(runs: dict[str, list[Path]]) -> str:
    """Turn latency by common measurement methods against the truth, on calls with a reference
    agent: each method's error per turn, where a recording's error comes from, and the error of
    the mean of gaps over GAP_MS per call. The runs under one name (one per seed) pool."""
    calls: dict[str, list[list[dict[str, Any]]]] = {}
    for name, dirs in runs.items():
        for run in dirs:
            recs = turns(run)
            (run / "turns.jsonl").write_text("".join(json.dumps(r) + "\n" for r in recs))
            calls.setdefault(name, []).append([r for r in recs if "truth_ms" in r])
    pooled = {n: [r for c in cs for r in c] for n, cs in calls.items()}

    def cell(key: str, minus: str | None = "truth_ms") -> list[str]:
        out = []
        for recs in pooled.values():
            v = [r[key] - (r[minus] if minus else 0) for r in recs if r.get(key) is not None]
            p = [f"{analyze._pct(v, q):+.0f}" for q in (0.05, 0.5, 0.95)] if v else ["-"] * 3
            miss = f" ({len(v)}/{len(recs)})" if len(v) < len(recs) else ""
            out.append(f"{p[1]} [{p[0]}, {p[2]}]{miss}")
        return out

    def gaps(d: str) -> list[str]:
        out = []
        for cs in calls.values():
            errs, kept, total = [], 0, 0
            for c in cs:
                v = [r[f"{d}_rec_rtp_ms"] for r in c if (r[f"{d}_rec_rtp_ms"] or 0) >= GAP_MS]
                kept, total = kept + len(v), total + len(c)
                if v:
                    errs.append(statistics.mean(v) - statistics.mean(r["truth_ms"] for r in c))
            p = (statistics.median(errs), min(errs), max(errs)) if errs else None
            out.append(f"{p[0]:+.0f} [{p[1]:+.0f}, {p[2]:+.0f}] ({kept}/{total})" if p else "-")
        return out

    names = list(pooled)
    detectors = detect.DETECTORS[1:]
    latency = [["truth itself", *cell("truth_ms", None)], *([m, *cell(k)] for m, k in METHODS)]
    edges = [
        row
        for d in detectors
        for row in (
            [f"{d}: caller's end", *cell(f"{d}_caller_offset_ms", None)],
            [f"{d}: agent's onset", *cell(f"{d}_ms")],
        )
    ]
    return (
        "Turn latency, measured - truth, ms: p50 [p5, p95] over every turn (turns measured / "
        "turns where some were missed). Truth: from the caller's last labelled sample to the "
        "agent's first, as they crossed the caller's wire. A recording is two channels at the "
        "caller, the agent's placed by a jitter buffer, unless said; both edges detected.\n\n"
        + analyze._table(["method", *names], latency)
        + "\nWhere a recording's error comes from: detected - labelled, ms, p50 [p5, p95]. "
        "A recording's error is about the agent's onset error - the caller's end error.\n\n"
        + analyze._table(["edge", *names], edges)
        + f"\nPer call, the mean of the recording's gaps of at least {GAP_MS} ms (Coval's "
        "Latency) - the mean of the call's true latencies, ms: median [min, max] over calls "
        "(gaps counted / turns)\n\n"
        + analyze._table(["detector", *names], [[d, *gaps(d)] for d in detectors])
    )
