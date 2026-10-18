"""rtpbench: wire-level latency tests for voice agents over SIP/RTP."""

import argparse
import json
import textwrap
from datetime import datetime
from pathlib import Path

from rtpbench import analyze, cases
from rtpbench.bench import PROFILES, TARGETS
from rtpbench.caller import GAP_SECONDS, LEAD_SECONDS

CODECS = {"pcmu": 0, "pcma": 8}
QUICK_START = """\
quick start, from a clone (Linux, Docker 28 or later, uv):
  uv run rtpbench calibrate --profiles clean --turns 5   # how exactly this host times the wire
  uv run --extra vad rtpbench cases                      # prove every case on the reference agent
  uv run --extra vad rtpbench target livekit --mock      # a bundled target, no AI account needed
  sudo .venv/bin/rtpbench cases sip:agent@host           # your agent (after uv sync --extra vad)

Each run writes results/<timestamp>/. rtpbench COMMAND --help shows its options and valid
values; docs/ in the repository explains the measurements, error bars and cases.
case, operator, realtime, agent and call are run inside containers by the commands above.
"""


class Help(argparse.RawDescriptionHelpFormatter):
    """Descriptions and epilogs as written; option help wrapped without splitting names like
    lte-bad at the hyphen."""

    def _split_lines(self, text: str, width: int) -> list[str]:
        return textwrap.wrap(text, width, break_on_hyphens=False)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="rtpbench", description=__doc__, epilog=QUICK_START, formatter_class=Help
    )
    parser.add_argument("--version", action="store_true", help="print the version and exit")
    # container commands get no help=, which keeps them out of the listing
    sub = parser.add_subparsers(dest="cmd", title="commands", metavar="COMMAND")
    profiles = f"comma-separated netem profiles: {', '.join(PROFILES)}"
    seed = "seed of the run's random choices (default: %(default)s)"

    p = sub.add_parser(
        "calibrate",
        help="measure this host's timing error against the reference agent (Docker)",
        description="""\
Call the reference agent, which logs the truth, once per network profile and codec, and
compare what the wire shows with it: the error bars every other measurement carries.
Writes summary.md, conditions.json and each call's captures to --out.""",
        epilog="""\
examples:
  uv run rtpbench calibrate --profiles clean --turns 5   # about 1 minute
  uv run rtpbench calibrate                              # every profile, 20 turns: 10 minutes
  uv run --extra vad rtpbench calibrate --barge-in       # interruptions: about 35 minutes
""",
        formatter_class=Help,
    )
    p.add_argument("--out", type=Path, metavar="DIR", help="default: results/<timestamp>")
    kind = p.add_mutually_exclusive_group()
    kind.add_argument("--speech", action="store_true", help="speech detection on real speech")
    kind.add_argument("--barge-in", action="store_true", help="barge-in stop time")
    p.add_argument(
        "--profiles",
        metavar="PROFILE,...",
        help=f"{profiles} (default: all; --speech, --barge-in: clean,mobile)",
    )
    p.add_argument(
        "--codecs",
        metavar="CODEC,...",
        help=f"comma-separated, of {', '.join(CODECS)} (default: pcmu; --speech: pcmu,pcma;"
        " --barge-in: pcma)",
    )
    p.add_argument(
        "--replies", type=Path, metavar="DIR", help="with --speech: agent replies from these WAVs"
    )
    p.add_argument("--turns", type=int, help="default 20; --speech: one per reply; --barge-in: 60")
    p.add_argument("--seed", type=int, default=1, help=seed)
    p.add_argument("--carrier", action="store_true", help="call through the carrier (Docker)")

    p = sub.add_parser(
        "cases",
        help="prove the conformance cases on the reference agent (Docker), or judge a SIP URI",
        description="""\
Without a URI, run each case against the reference agent in Docker, behaving well and in
each way it should fail, and check that every verdict comes out right; exit 1 if one does
not. With a URI, call that agent from this host, capture on --iface (needs root) and judge
it. Writes summary.md, results.json, report.html (a timeline of every call) and the
captures to --out.""",
        epilog="""\
examples:
  uv run --extra vad rtpbench cases                      # every case: about 14 minutes
  uv run --extra vad rtpbench cases --only hold,refer --profiles clean,lte --runs 3
  sudo .venv/bin/rtpbench cases sip:agent@host           # your agent (after uv sync --extra vad)
""",
        formatter_class=Help,
    )
    p.add_argument("uri", nargs="?", help="the agent to judge, e.g. sip:agent@host")
    p.add_argument(
        "--only",
        metavar="CASE,...",
        help="comma-separated cases (default: all; a few run only direct or only with --carrier): "
        + ", ".join(cases.CASES),
    )
    p.add_argument(
        "--profiles",
        default="clean",
        metavar="PROFILE,...",
        help=f"{profiles} (reference agent only; default: clean)",
    )
    p.add_argument("--runs", type=int, default=1, help="repeats per profile (default: 1)")
    p.add_argument("--out", type=Path, metavar="DIR", help="default: results/<timestamp>")
    p.add_argument("--seed", type=int, default=1, help=seed)
    p.add_argument("--iface", default="eth0", help="capture interface, with a URI (default: eth0)")
    p.add_argument(
        "--lines", type=Path, metavar="DIR", help="with a URI: prompt.wav, transfer.wav to say"
    )
    p.add_argument("--carrier", action="store_true", help="call through the carrier (Docker)")

    p = sub.add_parser(
        "target",
        help="cases, turn latency and barge-in against a bundled target (Docker)",
        description="""\
Bring up a target from targets/ next to the reference stack and run every case, a 12-turn
latency call and a 10-turn barge-in call against it through the netem router. Writes
summary.md, results.json, report.html, target.log and the captures to --out. Without
--mock, the target needs its AI engine's credentials: see targets/NAME/compose.yaml.""",
        epilog="""\
examples:
  uv run --extra vad rtpbench target livekit --mock      # no AI account needed: 11 minutes
  uv run --extra vad rtpbench target aivc --mock --only latency,barge-in --profiles clean,lte
""",
        formatter_class=Help,
    )
    p.add_argument("name", choices=TARGETS, metavar="NAME", help="%(choices)s")
    p.add_argument(
        "--only",
        metavar="NAME,...",
        help="comma-separated cases, latency, barge-in (default: all; a few cases run only direct"
        " or only with --carrier): " + ", ".join([*cases.CASES, "latency", "barge-in"]),
    )
    p.add_argument(
        "--profiles", default="clean", metavar="PROFILE,...", help=f"{profiles} (default: clean)"
    )
    p.add_argument("--runs", type=int, default=1, help="repeats per profile (default: 1)")
    p.add_argument("--out", type=Path, metavar="DIR", help="default: results/<timestamp>")
    p.add_argument("--seed", type=int, default=1, help=seed)
    p.add_argument("--carrier", action="store_true", help="call through the carrier (Docker)")
    p.add_argument("--mock", action="store_true", help="the mock engine instead of the AI engine")

    p = sub.add_parser("case", description="run one case's caller side (inside a container)")
    p.add_argument("name")
    p.add_argument("uri")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--iface", default="eth0")
    p.add_argument("--lines", type=Path, help="prompt.wav, transfer.wav to say")
    p.add_argument("--proxy", help="send a transfer's INVITE here (default: the Refer-To host)")

    p = sub.add_parser("operator", description="run the transfer target (inside a container)")
    p.add_argument("--ready", type=Path, default=Path("/tmp/ready"))

    p = sub.add_parser("realtime", description="run the mock engine (inside a container)")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--ready", type=Path, default=Path("/tmp/ready"))

    p = sub.add_parser(
        "report",
        help="judge a cases or target directory again; rewrite its report",
        description="""\
Judge a finished cases or target run with this version's checks, without placing calls.
Rewrites summary.md, results.json and report.html in DIR.""",
        epilog="""\
example:
  uv run --extra vad rtpbench report results/20260101-120000
""",
        formatter_class=Help,
    )
    p.add_argument("out", type=Path, metavar="DIR", help="a cases or target results directory")

    p = sub.add_parser(
        "analyze",
        help="summarise calibration run directories already captured",
        description="""\
Print the summary of calibrate's run directories, without placing calls. Directories with
the same name (other seeds) pool.""",
        epilog="""\
example:
  uv run --extra vad rtpbench analyze results/*/clean    # every calibration's clean runs
""",
        formatter_class=Help,
    )
    p.add_argument("runs", type=Path, nargs="+", metavar="DIR", help="e.g. results/*/clean")

    p = sub.add_parser(
        "index",
        help="write DIR/index.html, linking every result set under DIR",
        description="""\
Write DIR/index.html: for each folder of result sets, every case's verdicts in each set, linked
to its first call's timeline, then each set's conditions and files; calibrations by their
summary. Places no calls.""",
        epilog="""\
example:
  uv run rtpbench index                                  # results/index.html
""",
        formatter_class=Help,
    )
    p.add_argument(
        "dir", type=Path, nargs="?", default=Path("results"), metavar="DIR", help="default: results"
    )

    for name in ("agent", "call"):
        p = sub.add_parser(name, description=f"run the {name} side (inside a container)")
        p.add_argument("--speech", action="store_true", help="speak corpus clips")
        p.add_argument("--barge-in", action="store_true", help="follow the barge-in script")
        if name == "agent":
            p.add_argument("--replies", type=Path, help="with --speech: reply with these WAVs")
            p.add_argument("--case", help="behave as this conformance case needs")
            p.add_argument("--behaviour", default="good", help="with --case: which behaviour")
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
    if args.version:
        from importlib.metadata import version  # ~40 ms: not for every command

        print(f"rtpbench {version('rtpbench')}")
        return
    if args.cmd is None:
        parser.print_help()
        raise SystemExit(2)
    if args.cmd in ("calibrate", "cases", "target"):
        from rtpbench.progress import Progress

        progress = Progress()
    if args.cmd == "calibrate":
        from rtpbench.bench import calibrate

        out = args.out or Path("results") / datetime.now().strftime("%Y%m%d-%H%M%S")
        special = args.speech or args.barge_in
        profiles = args.profiles or ("clean,mobile" if special else ",".join(PROFILES))
        codecs = args.codecs or ("pcmu,pcma" if args.speech else "pcma" if args.barge_in else "")
        with progress:
            summary = calibrate(
                out,
                profiles.split(","),
                args.turns,
                args.seed,
                codecs.split(",") if codecs else None,
                args.speech,
                args.replies,
                args.barge_in,
                args.carrier,
                progress=progress,
            )
        print(summary)
        print(f"results in {out}")
    elif args.cmd == "cases":
        from rtpbench.bench import cases as run_cases

        out = args.out or Path("results") / datetime.now().strftime("%Y%m%d-%H%M%S")
        names = args.only.split(",") if args.only else cases.names(args.carrier)
        with progress:
            summary, proven = run_cases(
                out,
                args.uri,
                names,
                args.profiles.split(","),
                args.runs,
                args.seed,
                args.iface,
                args.lines,
                args.carrier,
                progress=progress,
            )
        print(summary)
        print(f"results in {out}")
        if not proven:
            raise SystemExit(1)
    elif args.cmd == "target":
        from rtpbench.bench import target

        out = args.out or Path("results") / datetime.now().strftime("%Y%m%d-%H%M%S")
        names = (
            args.only.split(",")
            if args.only
            else [*cases.names(args.carrier), "latency", "barge-in"]
        )
        profiles = args.profiles.split(",")
        with progress:
            summary = target(
                out,
                args.name,
                names,
                profiles,
                args.runs,
                args.seed,
                args.carrier,
                args.mock,
                progress=progress,
            )
        print(summary)
        print(f"results in {out}")
    elif args.cmd == "index":
        from rtpbench import report

        (args.dir / "index.html").write_text(report.index(args.dir))
        print(f"wrote {args.dir / 'index.html'}")
    elif args.cmd == "operator":
        from rtpbench.agent import operator

        operator(args.ready)
    elif args.cmd == "realtime":
        from rtpbench import realtime

        realtime.serve(args.out, ready=args.ready)
    elif args.cmd == "report":
        from rtpbench.bench import judge

        print(judge(args.out)[0])
        print(f"report in {args.out / 'report.html'}")
    elif args.cmd == "analyze":
        from rtpbench import bargein, speechcal

        first = json.loads((args.runs[0] / "caller.json").read_text())["turns"][:1] or [{}]
        summarize = speechcal.summarize if "speech" in first[0] else analyze.summarize
        if "prompt" in first[0]:
            summarize = bargein.summarize
        runs: dict[str, list[Path]] = {}
        for run in args.runs:
            runs.setdefault(run.name, []).append(run)
        print(summarize(runs))
    else:
        from rtpbench.capture import capture

        args.out.mkdir(parents=True, exist_ok=True)
        with capture(args.out / f"{'agent' if args.cmd == 'agent' else 'caller'}.pcap", args.iface):
            if args.cmd == "agent":
                from rtpbench.agent import serve

                behaviour = None
                if args.case:
                    from rtpbench.cases import CASES

                    behaviour = CASES[args.case].behaviours()[args.behaviour]
                log = serve(
                    args.out / "ready",
                    seed=args.seed,
                    real=args.speech,
                    replies=args.replies,
                    barge=args.barge_in,
                    case=behaviour,
                )
                if args.case:
                    log |= {"case": args.case, "behaviour": args.behaviour}
            elif args.cmd == "case":
                from rtpbench.cases import run

                log = run(args.name, args.uri, args.seed, args.lines, args.proxy)
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
