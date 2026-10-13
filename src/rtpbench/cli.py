"""rtpbench: wire-level latency tests for voice agents over SIP/RTP."""

import argparse
import json
from datetime import datetime
from pathlib import Path

from rtpbench import analyze


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="rtpbench", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("calibrate", help="measure the error against a reference agent (Docker)")
    p.add_argument("--out", type=Path, help="default: results/<timestamp>")
    p.add_argument("--profiles", default=",".join(["clean", "delay", "jitter", "loss", "mobile"]))
    p.add_argument("--turns", type=int, default=20)
    p.add_argument("--seed", type=int, default=1)

    p = sub.add_parser("analyze", help="summarise run directories already captured")
    p.add_argument("runs", type=Path, nargs="+")

    for name in ("agent", "call"):
        p = sub.add_parser(name, help=f"run the {name} side (inside a container)")
        if name == "call":
            p.add_argument("uri")
            p.add_argument("--turns", type=int, default=20)
        p.add_argument("--out", type=Path, required=True)
        p.add_argument("--seed", type=int, default=1)
        p.add_argument("--iface", default="eth0")

    args = parser.parse_args(argv)
    if args.cmd == "calibrate":
        from rtpbench.bench import calibrate

        out = args.out or Path("results") / datetime.now().strftime("%Y%m%d-%H%M%S")
        print(calibrate(out, args.profiles.split(","), args.turns, args.seed))
        print(f"results in {out}")
    elif args.cmd == "analyze":
        print(analyze.summarize({run.name: run for run in args.runs}))
    else:
        from rtpbench.capture import capture

        args.out.mkdir(parents=True, exist_ok=True)
        with capture(args.out / f"{'agent' if args.cmd == 'agent' else 'caller'}.pcap", args.iface):
            if args.cmd == "agent":
                from rtpbench.agent import serve

                log = serve(args.out / "ready", seed=args.seed)
            else:
                from rtpbench.caller import call

                log = call(args.uri, args.turns, args.seed)
        name = "agent.json" if args.cmd == "agent" else "caller.json"
        (args.out / name).write_text(json.dumps(log, indent=1))
