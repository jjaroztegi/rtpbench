"""Turn latency from a caller-side capture, by several methods, against ground truth.

Convention: sample k of a packet captured at time t sits at t + k/8000 s. Both ends use it, so
packetisation cancels and only network delay and method artefacts remain.

Methods (caller pcap only):
  wire    capture order and time, sample-accurate onset and end
  packet  capture time of the first/last packet holding speech
  rtp     RTP timestamps anchored at each stream's first packet
  concat  payloads appended in arrival order, as a naive two-channel recorder does

Truth uses event positions from the agent and caller logs (which packet and sample), times from
the caller pcap. The agent pcap splits truth - delay into agent scheduling error and network.
"""

import json
import math
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rtpbench import g711, pcap, rtp
from rtpbench.voice import GATE

METHODS = ("wire", "packet", "rtp", "concat")
SEGMENT_GAP_NS = 250_000_000
S = rtp.SAMPLE_NS

Timed = list[tuple[int, rtp.Packet]]


@dataclass
class Capture:
    up: Timed  # caller -> agent
    down: Timed  # agent -> caller


def load(path: Path) -> Capture:
    grams = pcap.read(path)
    invite = next(g for g in grams if g.payload.startswith(b"INVITE "))
    up: Timed = []
    down: Timed = []
    for g in grams:
        if 5060 in (g.sport, g.dport) or (p := rtp.parse(g.payload)) is None:
            continue
        if p.pt in g711.NAMES:
            (up if g.src == invite.src else down).append((g.t_ns, p))
    return Capture(up, down)


def view(packets: Timed, method: str) -> Iterable[tuple[int, bytes]]:
    """(time of sample 0, payload) per packet, in capture order."""
    if not packets:
        return
    t0, ts0 = packets[0][0], packets[0][1].ts
    total = 0
    for t, p in packets:
        if method == "rtp":
            t = t0 + ((p.ts - ts0) & 0xFFFFFFFF) * S
        elif method == "concat":
            t, total = t0 + total * S, total + len(p.payload)
        yield t, p.payload


def segments(
    timed: Iterable[tuple[int, bytes]], gate: re.Pattern[bytes], samples: bool
) -> list[list[int]]:
    """[onset, end] of each burst of activity, bursts split by SEGMENT_GAP_NS of silence."""
    segs: list[list[int]] = []
    for t, payload in timed:
        if not (first := gate.search(payload)):
            continue
        on = end = t
        if samples:
            last = gate.search(payload[::-1])
            assert last is not None
            on, end = t + first.start() * S, t + (len(payload) - 1 - last.start()) * S
        if segs and on - segs[-1][1] <= SEGMENT_GAP_NS:
            segs[-1] = [min(segs[-1][0], on), max(segs[-1][1], end)]
        else:
            segs.append([on, end])
    return sorted(segs)


def latencies(cap: Capture, pt: int, method: str) -> list[int | None]:
    """Per caller turn: first agent onset after the caller's end, minus that end (ns)."""
    gate, samples = g711.gate(pt, GATE), method != "packet"
    mode = "wire" if method == "packet" else method
    ends = [s[1] for s in segments(view(cap.up, mode), gate, samples)]
    onsets = [s[0] for s in segments(view(cap.down, mode), gate, samples)]
    out: list[int | None] = []
    for i, end in enumerate(ends):
        nxt = ends[i + 1] if i + 1 < len(ends) else None
        on = next((o for o in onsets if o > end and (nxt is None or o < nxt)), None)
        out.append(None if on is None else on - end)
    return out


def _at(packets: Timed, seq: int, off: int, later: bool = False) -> tuple[int, bool] | None:
    """Capture time of sample `off` of packet `seq`; if lost and `later`, the next one received."""
    times = [t for t, p in packets if p.seq == seq]
    if times:
        return min(times) + off * S, False
    if later:
        after = [t for t, p in packets if 0 < (p.seq - seq) & 0xFFFF < 50]
        if after:
            return min(after), True
    return None


def turns(run: Path) -> list[dict[str, Any]]:
    """One record per turn of one call: delay, truth, decomposition, latency per method (ms)."""
    agent_log = json.loads((run / "agent.json").read_text())
    caller_log = json.loads((run / "caller.json").read_text())
    caller, agent = load(run / "caller.pcap"), load(run / "agent.pcap")
    pt = caller_log["pt"]
    measured = {m: latencies(caller, pt, m) for m in METHODS}
    if len(agent_log["turns"]) != len(caller_log["turns"]):
        raise ValueError(
            f"{run}: agent answered {len(agent_log['turns'])} turns, "
            f"caller spoke {len(caller_log['turns'])}"
        )
    out = []
    for i, (a, c) in enumerate(zip(agent_log["turns"], caller_log["turns"], strict=True)):
        rec: dict[str, Any] = {"turn": i, "delay_ms": a["delay_ns"] / 1e6}
        end = _at(caller.up, c["end_seq"], c["end_off"])
        onset = _at(caller.down, a["onset_seq"], a["onset_off"], later=True)
        agent_end = _at(agent.up, a["end_seq"], a["end_off"])
        agent_on = _at(agent.down, a["onset_seq"], a["onset_off"])
        if end and onset and agent_end and agent_on:
            rec |= {
                "truth_ms": (onset[0] - end[0]) / 1e6,
                "onset_lost": onset[1],
                "sched_err_ms": (agent_on[0] - agent_end[0] - a["delay_ns"]) / 1e6,
                "up_ms": (agent_end[0] - end[0]) / 1e6,
                "down_ms": (onset[0] - agent_on[0]) / 1e6,
                "stamp_ms": (agent_end[0] - a["end_ns"]) / 1e6,  # tcpdump vs SO_TIMESTAMPNS
            }
        for m in METHODS:
            v = measured[m][i] if i < len(measured[m]) else None
            rec[m + "_ms"] = None if v is None else v / 1e6
        out.append(rec)
    return out


def stream_stats(packets: Timed) -> dict[str, int]:
    """Distinct packets received, packets the sender sent over that span, and late arrivals."""
    if not packets:
        return {"received": 0, "expected": 0, "reordered": 0}
    rel = [(p.seq - packets[0][1].seq) & 0xFFFF for _, p in packets]
    reordered, top = 0, -1
    for r in rel:
        reordered += r < top
        top = max(top, r)
    return {"received": len(set(rel)), "expected": max(rel) + 1, "reordered": reordered}


def _p95(values: list[float]) -> float:
    """Nearest-rank 95th percentile."""
    s = sorted(values)
    return s[max(0, math.ceil(0.95 * len(s)) - 1)]


def _stats(values: list[float]) -> list[str]:
    """Mean, p95 of magnitude, max magnitude."""
    if not values:
        return ["-"] * 3
    mags = [abs(v) for v in values]
    return [f"{sum(values) / len(values):+.2f}", f"{_p95(mags):.2f}", f"{max(mags):.2f}"]


def _table(header: list[str], rows: list[list[str]]) -> str:
    lines = [header, ["---"] * len(header), *rows]
    return "\n".join("| " + " | ".join(cells) + " |" for cells in lines) + "\n"


def summarize(runs: dict[str, Path]) -> str:
    """Error per method (vs injected delay and vs truth), then what truth - delay is made of."""
    errors, budget = [], []
    for name, run in runs.items():
        recs = turns(run)
        (run / "turns.jsonl").write_text("".join(json.dumps(r) + "\n" for r in recs))
        ok = [r for r in recs if "truth_ms" in r]
        for m in METHODS:
            got = [r for r in ok if r[m + "_ms"] is not None]
            vs_delay = _stats([r[m + "_ms"] - r["delay_ms"] for r in got])
            vs_truth = _stats([r[m + "_ms"] - r["truth_ms"] for r in got])
            errors.append([name, m, f"{len(got)}/{len(recs)}", *vs_delay, *vs_truth])
        up = stream_stats(load(run / "agent.pcap").up)
        down = stream_stats(load(run / "caller.pcap").down)
        budget.append(
            [
                name,
                *_stats([r["sched_err_ms"] for r in ok]),
                *_stats([r["up_ms"] + r["down_ms"] for r in ok]),
                f"{max((abs(r['stamp_ms']) for r in ok), default=0):.3f}",
                f"{up['expected'] - up['received']}/{up['expected']}, {up['reordered']}",
                f"{down['expected'] - down['received']}/{down['expected']}, {down['reordered']}",
                str(sum(r["onset_lost"] for r in ok)),
            ]
        )
    stat = ["mean", "p95 abs", "max abs"]
    return (
        "Error, ms: measured - injected delay | measured - truth\n\n"
        + _table(["profile", "method", "n", *stat, *stat], errors)
        + "\nTruth - delay = agent scheduling error + network (up + down), ms\n\n"
        + _table(
            [
                "profile",
                *(f"agent {s}" for s in stat),
                *(f"network {s}" for s in stat),
                "max pcap vs SO_TIMESTAMPNS",
                "uplink lost/sent, late",
                "downlink lost/sent, late",
                "onset pkt lost",
            ],
            budget,
        )
    )
