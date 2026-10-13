"""Speech-detection error against labelled speech, from the caller's capture alone.

The reference agent replies with labelled clips and logs where each sits in its stream; the
caller logs where its own utterances sit. All times come from the caller pcap (wire method).
Truth is the first / last labelled sample that arrived. Per detector:

  latency  turn latency measured blind (the caller's labelled end to the first detected agent
           speech after it) minus the truth (to the agent's first labelled sample)
  offset   last detected sample of the speech around a labelled clip minus its last labelled
           sample; likewise onset and offset of the caller's own utterances (uplink)

A detected span belongs to a clip if it overlaps the clip's labelled speech widened by 300 ms.
"""

import json
from pathlib import Path
from typing import Any

from rtpbench import analyze, detect, speech

WIDEN = 2400  # samples
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


def _ms(a: int | None, b: int | None) -> float | None:
    return None if a is None or b is None else (a - b) / 1e6


def turns(run: Path, detectors: tuple[str, ...] = detect.DETECTORS) -> list[dict[str, Any]]:
    caller_log = json.loads((run / "caller.json").read_text())
    agent_log = json.loads((run / "agent.json").read_text())
    cap = analyze.load(run / "caller.pcap")
    pt = caller_log["pt"]
    up, down = analyze.stream(cap.up, pt), analyze.stream(cap.down, pt)
    found = {d: (detect.DETECT[d](up.pcm), detect.DETECT[d](down.pcm)) for d in detectors}

    def place(st: analyze.Stream, seq0: int, spans: list[list[int]]) -> list[Span]:
        return [(st.index(seq0, a), st.index(seq0, b)) for a, b in spans]

    said = [place(up, caller_log["seq0"], t["speech"]) for t in caller_log["turns"]]
    replies = [place(down, agent_log["seq0"], t["speech"]) for t in agent_log["turns"]]
    if len(replies) != len(said):
        raise ValueError(f"{run}: agent answered {len(replies)} turns, caller spoke {len(said)}")
    said_t = [_truth(up, s) for s in said]
    out = []
    for i, (c, a) in enumerate(zip(said, replies, strict=True)):
        ct, at = said_t[i], _truth(down, a)
        if ct is None or at is None:
            continue
        later = said_t[i + 1] if i + 1 < len(said) else None
        nxt = later[0] if later else None
        rec: dict[str, Any] = {
            "turn": i,
            "caller_clip": caller_log["turns"][i].get("clip"),
            "agent_clip": agent_log["turns"][i]["clip"],
            "truth_ms": (at[0] - ct[1]) / 1e6,
        }
        for d, (fu, fd) in found.items():
            starts = (down.time(s, True) for s, _ in fd)
            on = next((t for t in starts if t and t > ct[1] and (nxt is None or t < nxt)), None)
            c_on, c_off = _edges(up, fu, c)
            rec |= {
                f"{d}_latency_ms": _ms(on, at[0]),
                f"{d}_offset_ms": _ms(_edges(down, fd, a)[1], at[1]),
                f"{d}_caller_onset_ms": _ms(c_on, ct[0]),
                f"{d}_caller_offset_ms": _ms(c_off, ct[1]),
            }
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


def summarize(runs: dict[str, Path], clips: dict[str, list[int]] | None = None) -> str:
    stat = ["mean", "p5", "p50", "p95", "max abs"]
    tables: dict[str, list[list[str]]] = {k: [] for k in ("latency", "offset", "caller")}
    for name, run in runs.items():
        recs = turns(run)
        (run / "turns.jsonl").write_text("".join(json.dumps(r) + "\n" for r in recs))
        for d in detect.DETECTORS:
            for key in ("latency", "offset"):
                v = [r[f"{d}_{key}_ms"] for r in recs if r[f"{d}_{key}_ms"] is not None]
                tables[key].append([name, d, f"{len(v)}/{len(recs)}", *_signed(v)])
            c_on = [
                r[f"{d}_caller_onset_ms"] for r in recs if r[f"{d}_caller_onset_ms"] is not None
            ]
            c_off = [
                r[f"{d}_caller_offset_ms"] for r in recs if r[f"{d}_caller_offset_ms"] is not None
            ]
            tables["caller"].append(
                [name, d, f"{len(c_on)}/{len(recs)}", *_signed(c_on)[:4], *_signed(c_off)[:4]]
            )
    out = (
        "Agent reply onset: blind turn latency - truth, ms\n\n"
        + analyze._table(["run", "detector", "n", *stat], tables["latency"])
        + "\nAgent reply offset: detected - labelled, ms\n\n"
        + analyze._table(["run", "detector", "n", *stat], tables["offset"])
        + "\nCaller utterance onset | offset: detected - labelled, ms\n\n"
        + analyze._table(["run", "detector", "n", *stat[:4], *stat[:4]], tables["caller"])
    )
    if clips:
        out += "\nLabel definition: |label at threshold - label at 35 dB|, ms\n\n" + sensitivity(
            clips
        )
    return out
