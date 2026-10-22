"""The capacity table from the unpacked capacity archive: per N, one directory nNN of N reference
stacks (sK, with its log sK.log) run at once, and the load average sampled in load.log.

    uv run python results/baseline/capacity.py capacity-DIR
"""

import json
import re
import sys
from pathlib import Path

from lateness import lateness

from rtpbench import analyze


def pct(v: list[float], q: float) -> str:
    return f"{analyze._pct(v, q):.2f}" if v else "-"


def main() -> None:
    head = [
        "N",
        "stacks ok",
        "turns",
        "wire-truth p99 / max",
        "agent sched p99 / max",
        "stamp max",
        "late caller p99 / max",
        "late agent p99 / max",
        "> 10 ms late",
        "drops",
        "steps",
        "load mean / max",
    ]
    print("| " + " | ".join(head) + " |")
    print("|" + " --- |" * len(head))
    for d in sorted(Path(sys.argv[1]).glob("n[0-9][0-9]")):
        logs = sorted(d.glob("s*.log"))
        ok = drops = steps = 0
        wire, sched, stamp, caller, agent = [], [], [], [], []
        for log in logs:
            drops += len(re.findall(r"dropped packets", log.read_text()))
            run = d / log.stem
            if (conditions := run / "conditions.json").exists():
                steps += len(json.loads(conditions.read_text()).get("clock_steps", []))
            if not (turns := run / "clean" / "turns.jsonl").exists():
                continue
            ok += 1
            for r in map(json.loads, turns.read_text().splitlines()):
                if "truth_ms" in r and r["wire_ms"] is not None:
                    wire.append(abs(r["wire_ms"] - r["truth_ms"]))
                    sched.append(abs(r["sched_err_ms"]))
                    stamp.append(abs(r["stamp_ms"]))
            caller += lateness(analyze.load(run / "clean" / "caller.pcap").up)
            agent += lateness(analyze.load(run / "clean" / "agent.pcap").down)
        loads = [float(x.split()[1]) for x in (d / "load.log").read_text().splitlines()]
        print(
            f"| {int(d.name[1:])} | {ok}/{len(logs)} | {len(wire)} "
            f"| {pct(wire, 0.99)} / {max(wire, default=0):.2f} "
            f"| {pct(sched, 0.99)} / {max(sched, default=0):.2f} | {max(stamp, default=0):.3f} "
            f"| {pct(caller, 0.99)} / {max(caller, default=0):.2f} "
            f"| {pct(agent, 0.99)} / {max(agent, default=0):.2f} "
            f"| {sum(x > 10 for x in caller + agent)} | {drops} | {steps} "
            f"| {sum(loads) / len(loads):.1f} / {max(loads):.1f} |"
        )


if __name__ == "__main__":
    main()
