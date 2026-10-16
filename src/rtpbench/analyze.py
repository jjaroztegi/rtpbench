"""Turn latency from a caller-side capture, by several methods, against ground truth.

Convention: sample k of a packet captured at time t sits at t + k/8000 s. Both ends use it, so
packetisation cancels and only network delay and method artefacts remain.

Methods (caller pcap only):
  wire    packets in RTP sequence order, each at its capture time, sample-accurate: the onset is
          the first voiced sample by sequence, when its packet arrived (the earliest an in-order
          player could play it)
  packet  as wire, but at packet granularity (first/last voiced packet)
  rtp     RTP timestamps anchored at the first packet to arrive, as a jitter-buffered recorder
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
CALLER_GAP_NS = 1_000_000_000  # pauses inside one caller turn are shorter than this
AGENT_GAP_NS = 250_000_000
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
        if g.tcp or 5060 in (g.sport, g.dport) or (p := rtp.parse(g.payload)) is None:
            continue
        if p.pt in g711.NAMES:
            (up if g.src == invite.src else down).append((g.t_ns, p))
    return Capture(up, down)


def signed(diff: int, bits: int) -> int:
    """A difference of wrapping counters (RTP seq, timestamp) as a signed number."""
    half = 1 << (bits - 1)
    return ((diff + half) & ((1 << bits) - 1)) - half


def unwrap(packets: Timed) -> list[int]:
    """Each packet's seq relative to the first to arrive, unwrapped in arrival order (negative
    for packets the first one overtook)."""
    ext, last, out = 0, packets[0][1].seq if packets else 0, []
    for _, p in packets:
        ext += signed(p.seq - last, 16)
        last = p.seq
        out.append(ext)
    return out


def by_seq(packets: Timed) -> Timed:
    """Sequence order (first copy of duplicates)."""
    seen: dict[int, tuple[int, rtp.Packet]] = {}
    for k, tp in zip(unwrap(packets), packets, strict=True):
        seen.setdefault(k, tp)
    return [seen[k] for k in sorted(seen)]


@dataclass
class Stream:
    """Decoded audio as a method reads it, 160 samples per packet slot."""

    seq: int  # RTP seq of slot 0
    pcm: list[int]
    times: list[int | None]  # time of each slot's sample 0; None for a lost packet

    def index(self, seq0: int, k: int) -> int:
        """Slot sample of sample k of a sender whose first packet had seq `seq0`."""
        return k + rtp.FRAME * (((seq0 - self.seq + 0x8000) & 0xFFFF) - 0x8000)

    def time(self, i: int, later: bool) -> int | None:
        """Time of sample i. In a lost packet: the next arrived sample if `later`, else the
        previous one (what a listener hears first / last)."""
        k, off = divmod(i, rtp.FRAME)
        if 0 <= k < len(self.times) and (t := self.times[k]) is not None:
            return t + off * S
        step = 1 if later else -1
        while 0 <= (k := k + step) < len(self.times):
            if (t := self.times[k]) is not None:
                return t + (0 if later else rtp.FRAME - 1) * S
        return None


def stream(packets: Timed, pt: int, method: str = "wire") -> Stream:
    """In sequence order (lost packets as silence) or, for concat, in arrival order."""
    if any(len(p.payload) != rtp.FRAME for _, p in packets):
        raise ValueError("only 20 ms G.711 packets are supported")
    t0, ts0 = packets[0][0], packets[0][1].ts
    if method == "concat":
        payloads = [p.payload for _, p in packets]
        times: list[int | None] = [t0 + k * rtp.PTIME_NS for k in range(len(packets))]
        seq = packets[0][1].seq
    else:
        seen: dict[int, tuple[int, rtp.Packet]] = {}
        for k, tp in zip(unwrap(packets), packets, strict=True):
            seen.setdefault(k, tp)
        lo, hi = min(seen), max(seen)
        silence = bytes([g711.SILENCE[pt]]) * rtp.FRAME
        slots = [seen.get(k) for k in range(lo, hi + 1)]
        payloads = [s[1].payload if s else silence for s in slots]
        times = [
            None if s is None else t0 + signed(s[1].ts - ts0, 32) * S if method == "rtp" else s[0]
            for s in slots
        ]
        seq = (packets[0][1].seq + lo) & 0xFFFF
    return Stream(seq, g711.decode(pt, b"".join(payloads)), times)


def view(packets: Timed, method: str) -> Iterable[tuple[int, bytes]]:
    """(time of sample 0, payload) per packet, in the order the method reads them."""
    if not packets:
        return
    t0, ts0 = packets[0][0], packets[0][1].ts
    if method == "concat":
        total = 0
        for _, p in packets:
            yield t0 + total * S, p.payload
            total += len(p.payload)
        return
    for t, p in by_seq(packets):
        yield (t0 + signed(p.ts - ts0, 32) * S if method == "rtp" else t), p.payload


def segments(
    timed: Iterable[tuple[int, bytes]], gate: re.Pattern[bytes], samples: bool, gap_ns: int
) -> list[list[int]]:
    """[onset, end] of each burst of activity: onset of its first voiced packet, latest end."""
    segs: list[list[int]] = []
    for t, payload in timed:
        if not (first := gate.search(payload)):
            continue
        on = end = t
        if samples:
            last = gate.search(payload[::-1])
            assert last is not None
            on, end = t + first.start() * S, t + (len(payload) - 1 - last.start()) * S
        if segs and on - segs[-1][1] <= gap_ns:
            segs[-1][1] = max(segs[-1][1], end)
        else:
            segs.append([on, end])
    return segs


def latencies(cap: Capture, pt: int, method: str) -> list[int | None]:
    """Per caller turn: first agent onset after the caller's end, minus that end (ns)."""
    gate, samples = g711.gate(pt, GATE), method != "packet"
    mode = "wire" if method == "packet" else method
    ends = [s[1] for s in segments(view(cap.up, mode), gate, samples, CALLER_GAP_NS)]
    onsets = [s[0] for s in segments(view(cap.down, mode), gate, samples, AGENT_GAP_NS)]
    out: list[int | None] = []
    for i, end in enumerate(ends):
        nxt = ends[i + 1] if i + 1 < len(ends) else None
        on = next((o for o in onsets if o > end and (nxt is None or o < nxt)), None)
        out.append(None if on is None else on - end)
    return out


def _at(packets: Timed, seq: int, off: int, later: bool = False) -> tuple[int, bool] | None:
    """Capture time of sample `off` of packet `seq`; if lost and `later`, of the next one by seq."""
    times = [t for t, p in packets if p.seq == seq]
    if times:
        return min(times) + off * S, False
    if later:
        after = [((p.seq - seq) & 0xFFFF, t) for t, p in packets if 0 < (p.seq - seq) & 0xFFFF < 50]
        if after:
            return min(after)[1], True
    return None


def turns(run: Path) -> list[dict[str, Any]]:
    """One record per caller turn: latency per method (ms) and, with an agent log, the truth."""
    caller_log = json.loads((run / "caller.json").read_text())
    caller = load(run / "caller.pcap")
    pt = caller_log["pt"]
    measured = {m: latencies(caller, pt, m) for m in METHODS}
    agent_turns: list[dict[str, Any]] = []
    if (run / "agent.json").exists():
        agent_turns = json.loads((run / "agent.json").read_text())["turns"]
        agent = load(run / "agent.pcap")
        if len(agent_turns) != len(caller_log["turns"]):
            raise ValueError(
                f"{run}: agent answered {len(agent_turns)} turns, "
                f"caller spoke {len(caller_log['turns'])}"
            )
    out = []
    for i, c in enumerate(caller_log["turns"]):
        rec: dict[str, Any] = {"turn": i}
        for m in METHODS:
            v = measured[m][i] if i < len(measured[m]) else None
            rec[m + "_ms"] = None if v is None else v / 1e6
        if agent_turns:
            a = agent_turns[i]
            rec["delay_ms"] = a["delay_ns"] / 1e6
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
        out.append(rec)
    return out


def stream_stats(packets: Timed) -> dict[str, int]:
    """Distinct packets received, packets the sender sent over that span, and late arrivals."""
    if not packets:
        return {"received": 0, "expected": 0, "reordered": 0}
    ext = unwrap(packets)
    lo = min(ext)
    rel = [k - lo for k in ext]
    reordered, top = 0, -1
    for r in rel:
        reordered += r < top
        top = max(top, r)
    return {"received": len(set(rel)), "expected": max(rel) + 1, "reordered": reordered}


def _pct(values: list[float], q: float) -> float:
    """Nearest-rank percentile."""
    s = sorted(values)
    return s[max(0, math.ceil(q * len(s)) - 1)]


def _stats(values: list[float]) -> list[str]:
    """Mean, p95 of magnitude, max magnitude."""
    if not values:
        return ["-"] * 3
    mags = [abs(v) for v in values]
    return [f"{sum(values) / len(values):+.2f}", f"{_pct(mags, 0.95):.2f}", f"{max(mags):.2f}"]


def _table(header: list[str], rows: list[list[str]]) -> str:
    lines = [header, ["---"] * len(header), *rows]
    return "\n".join("| " + " | ".join(cells) + " |" for cells in lines) + "\n"


def transit(path: Path) -> dict[str, list[float]]:
    """RTP through a relay, from a capture of both its legs on one interface: each packet's time
    from arriving to leaving (ms), for the caller's stream ("up") and the agent's ("down")."""
    grams = pcap.read(path)
    caller = next(g.src for g in grams if g.payload.startswith(b"INVITE "))
    seen: dict[tuple[int, int, int], tuple[int, str]] = {}
    out: dict[str, list[float]] = {"up": [], "down": []}
    for g in grams:
        if g.tcp or 5060 in (g.sport, g.dport) or (p := rtp.parse(g.payload)) is None:
            continue
        if (key := (p.ssrc, p.seq, p.ts)) in seen:
            t, src = seen.pop(key)
            out["up" if src == caller else "down"].append((g.t_ns - t) / 1e6)
        else:
            seen[key] = g.t_ns, g.src
    return out


def summarize(runs: dict[str, Path]) -> str:
    """Latency per method; with an agent log, error per method and what truth - delay is made of;
    with a carrier capture, the carrier's own transit time."""
    latency, errors, budget, relay = [], [], [], []
    for name, run in runs.items():
        if (run / "carrier.pcap").exists():
            for way, ms in transit(run / "carrier.pcap").items():
                cells = (
                    [f"{_pct(ms, q):.3f}" for q in (0.5, 0.95)] + [f"{max(ms):.3f}"]
                    if ms
                    else ["-"] * 3
                )
                relay.append([name, way, str(len(ms)), *cells])
        recs = turns(run)
        (run / "turns.jsonl").write_text("".join(json.dumps(r) + "\n" for r in recs))
        for m in METHODS:
            v = [r[m + "_ms"] for r in recs if r[m + "_ms"] is not None]
            cells = (
                [f"{_pct(v, 0.5):.1f}", f"{_pct(v, 0.95):.1f}", f"{max(v):.1f}"] if v else ["-"] * 3
            )
            latency.append([name, m, f"{len(v)}/{len(recs)}", *cells])
        ok = [r for r in recs if "truth_ms" in r]
        if not ok:
            continue
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
                f"{max(abs(r['stamp_ms']) for r in ok):.3f}",
                f"{up['expected'] - up['received']}/{up['expected']}, {up['reordered']}",
                f"{down['expected'] - down['received']}/{down['expected']}, {down['reordered']}",
                str(sum(r["onset_lost"] for r in ok)),
            ]
        )
    out = "Turn latency, ms\n\n" + _table(["run", "method", "n", "p50", "p95", "max"], latency)
    if relay:
        out += "\nCarrier transit (in to out on its interface), ms\n\n"
        out += _table(["run", "stream", "packets", "p50", "p95", "max"], relay)
    if not errors:
        return out
    stat = ["mean", "p95 abs", "max abs"]
    return (
        out
        + "\nError, ms: measured - injected delay | measured - truth\n\n"
        + _table(["run", "method", "n", *stat, *stat], errors)
        + "\nTruth - delay = agent scheduling error + network (up + down), ms\n\n"
        + _table(
            [
                "run",
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
