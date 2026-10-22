"""How late each sender's RTP packets left against its own 20 ms grid, from the capture taken at
the sender: the caller's stream from caller.pcap, the agent's from agent.pcap, in every run under
the directories given. Packet n of a stream should leave at t0 + n * 20 ms (n from its RTP
timestamp); lateness is the capture time less that, with t0 the earliest such origin, so the most
punctual packet is 0.

    uv run python results/baseline/lateness.py DIR...
"""

import sys
from pathlib import Path

from rtpbench import analyze, rtp


def lateness(packets: analyze.Timed) -> list[float]:
    """Per packet, ms."""
    if not packets:
        return []
    ts0 = packets[0][1].ts
    origins = [t - analyze.signed(p.ts - ts0, 32) * rtp.SAMPLE_NS for t, p in packets]
    t0 = min(origins)
    return [(o - t0) / 1e6 for o in origins]


def main() -> None:
    late: dict[str, list[float]] = {"caller": [], "agent": []}
    for arg in sys.argv[1:]:
        for caller in sorted(Path(arg).glob("**/caller.json")):
            run = caller.parent
            late["caller"] += lateness(analyze.load(run / "caller.pcap").up)
            late["agent"] += lateness(analyze.load(run / "agent.pcap").down)
    for name, v in {**late, "both": late["caller"] + late["agent"]}.items():
        p50, p99 = analyze._pct(v, 0.5), analyze._pct(v, 0.99)
        print(f"{name}: {len(v)} packets, p50 {p50:.3f}, p99 {p99:.3f}, max {max(v):.2f} ms")


if __name__ == "__main__":
    main()
