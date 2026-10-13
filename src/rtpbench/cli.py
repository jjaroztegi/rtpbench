"""rtpbench: wire-level latency tests for voice agents over SIP/RTP."""

import argparse
import json
from datetime import datetime
from pathlib import Path

from rtpbench import analyze
from rtpbench.caller import GAP_SECONDS, LEAD_SECONDS

CODECS = {"pcmu": 0, "pcma": 8}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="rtpbench", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("calibrate", help="measure the error against a reference agent (Docker)")
    p.add_argument("--out", type=Path, help="default: results/<timestamp>")
    kind = p.add_mutually_exclusive_group()
    kind.add_argument("--speech", action="store_true", help="speech detection on real speech")
    kind.add_argument("--barge-in", action="store_true", help="barge-in stop time")
    p.add_argument("--profiles", help="default: all five; --speech, --barge-in: clean,mobile")
    p.add_argument("--codecs", help="default pcmu; --speech: pcmu,pcma; --barge-in: pcma")
    p.add_argument("--replies", type=Path, help="with --speech: agent replies from these WAVs")
    p.add_argument("--turns", type=int, help="default 20; --speech: one per reply; --barge-in: 60")
    p.add_argument("--seed", type=int, default=1)

    p = sub.add_parser("analyze", help="summarise run directories already captured")
    p.add_argument("runs", type=Path, nargs="+")

    for name in ("agent", "call"):
        p = sub.add_parser(name, help=f"run the {name} side (inside a container)")
        p.add_argument("--speech", action="store_true", help="speak corpus clips")
        p.add_argument("--barge-in", action="store_true", help="follow the barge-in script")
        if name == "agent":
            p.add_argument("--replies", type=Path, help="with --speech: reply with these WAVs")
        else:
            p.add_argument("uri")
            p.add_argument("--turns", type=int, default=20)
            p.add_argument("--wav", type=Path, nargs="+", help="utterances, 8 kHz mono 16-bit")
            p.add_argument("--interrupt", type=Path, nargs="+", help="with --barge-in: WAVs")
            p.add_argument("--codec", choices=CODECS, help="offer only this codec")
            p.add_argument(
                "--lead", type=float, default=LEAD_SECONDS, help="silence before turn 1, s"
            )
            p.add_argument(
                "--gap", type=float, default=GAP_SECONDS, help="silence after each turn, s"
            )
        p.add_argument("--out", type=Path, required=True)
        p.add_argument("--seed", type=int, default=1)
        p.add_argument("--iface", default="eth0")

    args = parser.parse_args(argv)
    if args.cmd == "calibrate":
        from rtpbench.bench import PROFILES, calibrate

        out = args.out or Path("results") / datetime.now().strftime("%Y%m%d-%H%M%S")
        special = args.speech or args.barge_in
        profiles = args.profiles or ("clean,mobile" if special else ",".join(PROFILES))
        codecs = args.codecs or ("pcmu,pcma" if args.speech else "pcma" if args.barge_in else "")
        print(
            calibrate(
                out,
                profiles.split(","),
                args.turns,
                args.seed,
                codecs.split(",") if codecs else None,
                args.speech,
                args.replies,
                args.barge_in,
            )
        )
        print(f"results in {out}")
    elif args.cmd == "analyze":
        from rtpbench import bargein, speechcal

        first = json.loads((args.runs[0] / "caller.json").read_text())["turns"][:1] or [{}]
        summarize = speechcal.summarize if "speech" in first[0] else analyze.summarize
        if "prompt" in first[0]:
            summarize = bargein.summarize
        print(summarize({run.name: run for run in args.runs}))
    else:
        from rtpbench.capture import capture

        args.out.mkdir(parents=True, exist_ok=True)
        with capture(args.out / f"{'agent' if args.cmd == 'agent' else 'caller'}.pcap", args.iface):
            if args.cmd == "agent":
                from rtpbench.agent import serve

                log = serve(
                    args.out / "ready",
                    seed=args.seed,
                    real=args.speech,
                    replies=args.replies,
                    barge=args.barge_in,
                )
            else:
                from rtpbench import speech
                from rtpbench.caller import call, converse, speech_utterances

                utterances: list[tuple[str, list[int]]] | None = None
                if args.wav:
                    utterances = [(w.stem, speech.read_wav(w)) for w in args.wav]
                elif args.speech:
                    utterances = speech_utterances(args.seed)
                codecs = (CODECS[args.codec],) if args.codec else tuple(CODECS.values())
                if args.barge_in:
                    cut_in = [(w.stem, speech.read_wav(w)) for w in args.interrupt or []]
                    log = converse(
                        args.uri, args.turns, args.seed, utterances, args.lead, codecs, cut_in
                    )
                else:
                    log = call(
                        args.uri, args.turns, args.seed, utterances, args.lead, args.gap, codecs
                    )
        name = "agent.json" if args.cmd == "agent" else "caller.json"
        (args.out / name).write_text(json.dumps(log, indent=1))
