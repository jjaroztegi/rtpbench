"""rtpbench: wire-level latency tests for voice agents over SIP/RTP."""

import argparse
import json
import os
import shutil
import textwrap
from datetime import datetime
from pathlib import Path

from rtpbench import analyze, cases, pcap
from rtpbench.bench import PROFILES, TARGETS, docker, is_uri
from rtpbench.caller import GAP_SECONDS, LEAD_SECONDS
from rtpbench.srtp import SUITES

CODECS = {"pcmu": 0, "pcma": 8}
LARGE_INVITE_TLS = "large-invite: not over TLS (it checks the switch from UDP to TCP)"
TLS_HELP = "SIP over TLS to the agent (or the carrier), certified by the stack's test CA"
SRTP_HELP = (
    "SRTP keyed in the SDP (SDES), offering these suites in this order (default: "
    + ", ".join(SUITES)
    + ")"
)
QUICK_START = """\
quick start, from a clone (Linux, Docker 28 or later, uv):
  uv run rtpbench calibrate --profiles clean --turns 5   # how exactly this host times the wire
  uv run --extra vad rtpbench cases                      # prove every case on the reference agent
  uv run --extra vad rtpbench target livekit --mock      # a bundled target, no AI account needed
  uv run --extra vad rtpbench target sip:agent@host      # your agent

Each run writes results/<timestamp>/. rtpbench COMMAND --help shows its options and valid
values; docs/ in the repository explains the measurements, error bars and cases.
case, operator, realtime, agent and call are run inside containers by the commands above.
"""


class Help(argparse.RawDescriptionHelpFormatter):
    """Descriptions and epilogs as written; option help wrapped without splitting names like
    lte-bad at the hyphen."""

    def _split_lines(self, text: str, width: int) -> list[str]:
        return textwrap.wrap(text, width, break_on_hyphens=False)


def _target_args(args: argparse.Namespace) -> str | None:
    """What is wrong with `rtpbench target`'s arguments, if anything."""
    from rtpbench.caller import parse_uri

    uri_only = {
        "--proxy": args.proxy,
        "--network": args.network,
        "--advertise": args.advertise,
        "--ca": args.ca,
    }
    if not is_uri(args.name):
        if args.name not in TARGETS:
            return f"NAME|URI: {args.name!r} is neither {', '.join(TARGETS)} nor a sip: URI"
        if given := [k for k, v in uri_only.items() if v]:
            return f"{', '.join(given)}: with a URI only"
        if (args.tls or args.srtp) and not args.carrier:
            return "--tls, --srtp: with a URI, or through the carrier (--carrier)"
        if args.lines and args.mock:
            return "--lines: not with --mock, which recognises only the bundled lines"
        return None
    if args.mock or args.carrier or args.tls:
        return "--mock, --carrier, --tls: with a bundled target only (a URI gives TLS as sips:)"
    if ":" in args.name.split(":", 1)[1].split("@")[0] and "@" in args.name:
        return "the URI has a password: give credentials in the environment, not the URI"
    host, _ = parse_uri(args.name)
    if host == "localhost" or host.startswith("127."):
        return f"{host}: the caller runs in Docker; give this host's own address, or --network"
    if args.ca and not args.ca.is_file():
        return f"--ca: {args.ca} is not a file"
    if args.advertise:
        from rtpbench.caller import ADVERTISE_PORTS

        adv_host, _, adv_port = args.advertise.rpartition(":")
        if not adv_host or not adv_port.isdigit():
            return "--advertise: HOST:PORT"
        if not 1 <= int(adv_port) <= 65536 - ADVERTISE_PORTS:
            return f"--advertise: PORT 1-{65536 - ADVERTISE_PORTS}, the first of {ADVERTISE_PORTS}"
    return None


def _suites(value: str | None) -> list[str] | None:
    return value.split(",") if value else None


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
    p.add_argument("--tls", action="store_true", help=TLS_HELP)
    p.add_argument("--srtp", nargs="?", const=",".join(SUITES), metavar="SUITE,...", help=SRTP_HELP)

    p = sub.add_parser(
        "cases",
        help="prove the conformance cases on the reference agent (Docker)",
        description="""\
Run each case against the reference agent in Docker, behaving well and in each way it should
fail, and check that every verdict comes out right; exit 1 if one does not. Writes summary.md,
results.json, report.html (a timeline of every call) and the captures to --out. To judge an
agent, use `rtpbench target`.""",
        epilog="""\
examples:
  uv run --extra vad rtpbench cases                      # every case: about 17 minutes
  uv run --extra vad rtpbench cases --only hold,refer --profiles clean,lte --runs 3
""",
        formatter_class=Help,
    )
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
        help=f"{profiles} (default: clean)",
    )
    p.add_argument("--runs", type=int, default=1, help="repeats per profile (default: 1)")
    p.add_argument("--out", type=Path, metavar="DIR", help="default: results/<timestamp>")
    p.add_argument("--seed", type=int, default=1, help=seed)
    p.add_argument("--carrier", action="store_true", help="call through the carrier (Docker)")
    p.add_argument("--tls", action="store_true", help=TLS_HELP)
    p.add_argument("--srtp", nargs="?", const=",".join(SUITES), metavar="SUITE,...", help=SRTP_HELP)

    p = sub.add_parser(
        "target",
        help="cases, turn latency and barge-in against a bundled target or a SIP URI (Docker)",
        description="""\
Run every case, a 12-turn latency call and a 10-turn barge-in call through the netem router
against a target from targets/ (brought up next to it) or the agent at a SIP URI. Writes
summary.md, results.json, report.html, target.log and the captures to --out. Without
--mock, a bundled target needs its AI engine's credentials: see targets/NAME/compose.yaml.""",
        epilog="""\
examples:
  uv run --extra vad rtpbench target livekit --mock      # no AI account needed: 11 minutes
  uv run --extra vad rtpbench target aivc --mock --only latency,barge-in --profiles clean,lte
  uv run --extra vad rtpbench target sip:agent@203.0.113.7 --profiles clean,lte
  uv run --extra vad rtpbench target sip:agent@agent --network myagent_default
  uv run --extra vad rtpbench target 'sip:agent@agent.example.com;transport=tls'
""",
        formatter_class=Help,
    )
    p.add_argument(
        "name",
        metavar="NAME|URI",
        help=f"{', '.join(TARGETS)}, or the agent's URI: sip:user@host[:port], over TLS with"
        " sips: or ;transport=tls",
    )
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
    p.add_argument(
        "--lines",
        type=Path,
        metavar="DIR",
        help="the caller's lines, named as in corpus/lines/en (not with --mock)",
    )
    p.add_argument(
        "--proxy", metavar="HOST", help="URI: send a transfer's INVITE here, not to the operator"
    )
    p.add_argument(
        "--network",
        metavar="NAME",
        help="URI: the Docker network the agent is on, when it runs in Docker on this host",
    )
    p.add_argument(
        "--advertise",
        metavar="HOST:PORT",
        help="URI: an address where the agent reaches this host; it publishes PORT and the next 7",
    )
    p.add_argument(
        "--ca",
        type=Path,
        metavar="FILE",
        help="URI or --proxy over TLS: trust the certificates in FILE (PEM), not the system's",
    )
    p.add_argument(
        "--srtp",
        nargs="?",
        const=",".join(SUITES),
        metavar="SUITE,...",
        help="URI, or with --carrier: " + SRTP_HELP,
    )
    p.add_argument(
        "--tls",
        action="store_true",
        help="with --carrier: SIP over TLS to the carrier (a URI says so itself: sips:)",
    )

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

    p = sub.add_parser(
        "realtime",
        description="run the mock engine, a plain-ws OpenAI Realtime server: in the stack's "
        "container, or on this host for an agent of your own",
    )
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--port", type=int, help="ws port (default: 8000)")
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
  uv run --extra vad rtpbench report results/20260101-120000 --agent-pcap agent.pcap
""",
        formatter_class=Help,
    )
    p.add_argument("out", type=Path, metavar="DIR", help="a cases or target results directory")
    p.add_argument(
        "--agent-pcap",
        type=Path,
        metavar="FILE",
        help="a capture taken at the agent during the run (tcpdump -w), to split its own RTP "
        "pacing from the path's; copied into DIR, where later reports find it",
    )

    p = sub.add_parser(
        "check",
        help="pass or fail a target run against a policy; exit 1 if it fails (CI)",
        description="""\
Judge a finished target run against a policy, without placing calls: the cases that may fail,
limits on turn latency and barge-in, and how far they may grow from an earlier run's
check.json. Writes check.md and check.json in DIR; exits 1 if the run fails the policy, 2 if
the policy, DIR or the previous check.json cannot be used. Without --policy, every case must
pass.""",
        epilog="""\
example:
  uv run --extra vad rtpbench check results/20260101-120000 --policy rtpbench.toml \\
      --previous baseline/check.json
""",
        formatter_class=Help,
    )
    p.add_argument("out", type=Path, metavar="DIR", help="a target results directory")
    p.add_argument("--policy", type=Path, metavar="FILE", help="TOML; see docs/ci.md")
    p.add_argument(
        "--previous", type=Path, metavar="FILE", help="an earlier run's check.json to compare with"
    )

    p = sub.add_parser(
        "analyze",
        help="summarise calibration run directories already captured",
        description="""\
Print the summary of calibrate's run directories, without placing calls. Directories with
the same name (other seeds) pool.""",
        epilog="""\
example:
  uv run --extra vad rtpbench analyze results/*/clean    # every calibration's clean runs
  uv run --extra vad rtpbench analyze --methods results/*/lte-pcmu   # --speech runs only
""",
        formatter_class=Help,
    )
    p.add_argument("runs", type=Path, nargs="+", metavar="DIR", help="e.g. results/*/clean")
    p.add_argument(
        "--methods",
        action="store_true",
        help="calibrate --speech runs: turn latency by common measurement methods against truth",
    )

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
    p.add_argument(
        "--markdown",
        metavar="URL",
        help="link Markdown files to URL/<path under DIR>, where they render (default: as files)",
    )

    for name in ("agent", "call"):
        p = sub.add_parser(name, description=f"run the {name} side (inside a container)")
        p.add_argument("--speech", action="store_true", help="speak corpus clips")
        p.add_argument("--barge-in", action="store_true", help="follow the barge-in script")
        if name == "agent":
            p.add_argument("--replies", type=Path, help="with --speech: reply with these WAVs")
            p.add_argument("--case", help="behave as this conformance case needs")
            p.add_argument("--behaviour", default="good", help="with --case: which behaviour")
            p.add_argument("--tls", type=Path, help="SIP over TLS too, with server.crt here")
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
    if unknown := [
        s for s in (getattr(args, "srtp", None) or "").split(",") if s and s not in SUITES
    ]:
        parser.error(f"--srtp: {', '.join(unknown)}: not one of {', '.join(SUITES)}")
    if args.cmd in ("calibrate", "cases", "target"):
        from rtpbench.progress import Progress

        progress = Progress()
    if args.cmd == "calibrate":
        from rtpbench.bench import calibrate

        out = args.out or Path("results") / datetime.now().strftime("%Y%m%d-%H%M%S")
        special = args.speech or args.barge_in
        profiles = args.profiles or ("clean,mobile" if special else ",".join(PROFILES))
        codecs = args.codecs or ("pcmu,pcma" if args.speech else "pcma" if args.barge_in else "")
        docker()
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
                args.tls,
                _suites(args.srtp),
                progress=progress,
            )
        print(summary)
        print(f"results in {out}")
    elif args.cmd == "cases":
        from rtpbench.bench import cases as run_cases

        out = args.out or Path("results") / datetime.now().strftime("%Y%m%d-%H%M%S")
        names = args.only.split(",") if args.only else cases.names(args.carrier, args.tls)
        if args.tls and "large-invite" in names:
            parser.error(LARGE_INVITE_TLS)
        docker()
        with progress:
            summary, proven = run_cases(
                out,
                names,
                args.profiles.split(","),
                args.runs,
                args.seed,
                args.carrier,
                args.tls,
                _suites(args.srtp),
                progress=progress,
            )
        print(summary)
        print(f"results in {out}")
        if not proven:
            raise SystemExit(1)
    elif args.cmd == "target":
        from rtpbench.bench import check_lines, target

        if problem := _target_args(args):
            parser.error(problem)
        out = args.out or Path("results") / datetime.now().strftime("%Y%m%d-%H%M%S")
        from rtpbench.sip import secure

        tls = secure(args.name) if is_uri(args.name) else args.tls
        names = (
            args.only.split(",")
            if args.only
            else [*cases.names(args.carrier, tls), "latency", "barge-in"]
        )
        if args.lines and (problems := check_lines(args.lines, names)):
            parser.error(f"--lines {args.lines}:\n  " + "\n  ".join(problems))
        if tls and "large-invite" in names:
            parser.error(LARGE_INVITE_TLS)
        profiles = args.profiles.split(",")
        docker()
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
                args.lines,
                args.proxy,
                args.network,
                args.advertise,
                args.ca,
                _suites(args.srtp),
                args.tls,
                progress=progress,
            )
        print(summary)
        print(f"results in {out}")
    elif args.cmd == "index":
        from rtpbench import report

        (args.dir / "index.html").write_text(report.index(args.dir, args.markdown))
        print(f"wrote {args.dir / 'index.html'}")
    elif args.cmd == "operator":
        from rtpbench.agent import operator

        operator(args.ready)
    elif args.cmd == "realtime":
        from rtpbench import realtime

        port = realtime.PORT if args.port is None else args.port
        if not 1 <= port <= 65535:
            parser.error("--port: 1-65535")
        realtime.serve(args.out, port, args.ready)
    elif args.cmd == "report":
        from rtpbench.bench import judge

        if args.agent_pcap:
            side = args.out / cases.AGENT_SIDE
            try:
                pcap.read(args.agent_pcap)  # refused here, not copied in to break later reports
            except (OSError, ValueError) as e:
                parser.error(f"--agent-pcap: {e} (tcpdump -w writes one)")
            if not (side.exists() and side.samefile(args.agent_pcap)):
                shutil.copyfile(args.agent_pcap, side)
        print(judge(args.out)[0])
        print(f"report in {args.out / 'report.html'}")
    elif args.cmd == "check":
        from rtpbench.check import InputError, check

        try:
            text, ok = check(args.out, args.policy, args.previous)
        except InputError as e:
            parser.error(str(e))
        print(text)
        if not ok:
            raise SystemExit(1)
    elif args.cmd == "analyze":
        from rtpbench import bargein, speechcal

        first = json.loads((args.runs[0] / "caller.json").read_text())["turns"][:1] or [{}]
        summarize = speechcal.summarize if "speech" in first[0] else analyze.summarize
        if "prompt" in first[0]:
            summarize = bargein.summarize
        if args.methods:
            summarize = speechcal.methods
        runs: dict[str, list[Path]] = {}
        for run in args.runs:
            runs.setdefault(run.name, []).append(run)
        print(summarize(runs))
    else:
        from rtpbench.capture import capture

        args.out.mkdir(parents=True, exist_ok=True)
        if args.cmd != "agent":  # the caller's TLS session keys, which judging decrypts with
            os.environ["SSLKEYLOGFILE"] = str(args.out / "keys.log")
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
                    tls=args.tls,
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
