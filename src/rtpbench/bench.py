"""`rtpbench calibrate`: reference agent behind a netem router, one call per profile and codec."""

import hashlib
import json
import os
import platform
import secrets
import shutil
import subprocess
import time
from collections.abc import Callable
from datetime import UTC, datetime
from functools import partial
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from rtpbench import analyze, bargein, speech, speechcal
from rtpbench.agent import SPEECH_DELAY_RANGE

ROOT = Path(__file__).resolve().parents[2]
LINES = ROOT / "corpus" / "lines" / "en"  # the caller's lines against a real agent
# compose targets, targets/<name>/compose.yaml: the SIP user to dial, the variable naming the AI
# engine's endpoint (only its domain and query go into the conditions), and its default
TARGETS = {
    "aivc": ("openai", "OPENAI_URL", "wss://api.openai.com/v1/realtime?model=gpt-realtime-2.1"),
}
# netem arguments per direction, applied to both router egress interfaces; SIP is exempt.
# delay, jitter, loss, mobile: synthetic stimuli for the calibrations (each impairment alone,
# then together). lte, lte-bad: what a mobile caller's path does, from sources:
# - lte: 1% loss, the VoLTE (QCI 1) packet loss target per radio link (3GPP TR 26.989 5.1.1.6.1),
#   in bursts of 2 (mean run in 3GPP's VoLTE delay/error profiles 7-10, EVS-7c S4-141392
#   Annex D); jitter sd 3 ms (commercial LTE in mobility, Elnashar et al., arXiv 1810.02968,
#   fig. 6); 40 ms one way (LTE uplink p99, Nielsen et al., arXiv 1909.03875, fig. 4).
# - lte-bad: 3GPP delay/error profile 8 (VoLTE logs in challenging radio conditions, EVS-7c
#   Annex D): 6.2% loss, mean run 2.1 (Gilbert p 3.2%, r 48%); delay above the floor mean 45 ms,
#   sd 26, p95 90. Delays chosen so that what netem delivers matches (measured over 5000
#   packets: mean 48, sd 23, p95 88).
# `rate` keeps packets in order, as a radio bearer delivers them (independent netem jitter of
# sd 26 ms reorders 30% of packets; the profile 8 trace 3%).
PROFILES = {
    "clean": "",
    "delay": "delay 40ms",
    "jitter": "delay 40ms 10ms distribution normal",
    "loss": "loss 3%",
    "mobile": "delay 60ms 20ms distribution normal loss 3%",
    "lte": "delay 40ms 3ms distribution normal loss gemodel 0.505% 50% rate 100mbit",
    "lte-bad": "delay 36ms 30ms distribution normal loss gemodel 3.2% 48% rate 100mbit",
}


def _image_tag() -> str:
    h = hashlib.sha256((ROOT / "Dockerfile").read_bytes())
    for f in sorted([*(ROOT / "src").rglob("*.py"), *(ROOT / "corpus").rglob("*.wav")]):
        h.update(f.relative_to(ROOT).as_posix().encode() + f.read_bytes())
    return "rtpbench:" + h.hexdigest()[:12]


class Stack:
    """caller | router | agent, plus a target's services when given (paths in its compose file
    are relative to the repository root)."""

    def __init__(self, out: Path, target: str | None = None) -> None:
        self.project = f"rtpbench-{secrets.token_hex(3)}"
        self.env = os.environ | {"RTPBENCH_IMAGE": _image_tag(), "RTPBENCH_OUT": str(out)}
        self.files = [ROOT / "compose.yaml"]
        if target:
            self.files.append(ROOT / "targets" / target / "compose.yaml")

    def compose(self, *args: str, check: bool = True) -> str:
        files = [a for f in self.files for a in ("-f", str(f))]
        cmd = ["docker", "compose", "-p", self.project, *files, *args]
        res = subprocess.run(cmd, env=self.env, capture_output=True, text=True)
        if check and res.returncode:
            raise RuntimeError(f"{' '.join(args)} failed:\n{res.stderr}")
        return res.stdout.strip()

    def sh(self, service: str, cmd: str, check: bool = True) -> str:
        return self.compose("exec", "-T", service, "sh", "-c", cmd, check=check)

    def up(self) -> None:
        self.compose("build", "-q")
        self.compose("up", "-d", "--wait")

    def down(self) -> None:
        self.compose("down", "-t", "0", "--remove-orphans", check=False)

    def netem(self, args: str, peers: list[str]) -> None:
        for ip in peers:
            dev = self.sh("router", f"ip -o route get {ip}").split(" dev ")[1].split()[0]
            self.sh("router", f"tc qdisc del dev {dev} root 2>/dev/null || true")
            if not args:
                continue
            prio = f"root handle 1: prio bands 3 priomap {' '.join(['2'] * 16)}"
            self.sh("router", f"tc qdisc add dev {dev} {prio}")
            self.sh("router", f"tc qdisc add dev {dev} parent 1:3 handle 30: netem {args}")
            for port in ("sport", "dport"):
                match = f"u32 match ip protocol 17 0xff match ip {port} 5060 0xffff flowid 1:1"
                self.sh("router", f"tc filter add dev {dev} parent 1: protocol ip prio 1 {match}")


def _wait_for(path: Path, timeout: float) -> None:
    deadline = time.monotonic() + timeout
    while not path.exists():
        if time.monotonic() > deadline:
            raise TimeoutError(f"{path} did not appear")
        time.sleep(0.1)


def _host(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=ROOT).stdout.strip()


def conditions(sh: Callable[[str], str], seed: int) -> dict[str, Any]:
    """Versions and host; `sh` runs a command where the capture runs (a container or here)."""
    return {
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "commit": _host("git describe --always --dirty"),
        "kernel": sh("uname -r"),
        "cpu": sh("grep -m1 'model name' /proc/cpuinfo | cut -d: -f2").strip(),
        "docker": _host("docker version --format '{{.Server.Version}}'"),
        "python": sh("python3 -V"),
        "tcpdump": sh("tcpdump --version 2>&1 | head -1"),
        "host": platform.platform(),
        "seed": seed,
        "netem_per_direction": PROFILES,
    }


def calibrate(
    out: Path,
    profiles: list[str],
    turns: int | None,
    seed: int,
    codecs: list[str] | None = None,
    real: bool = False,
    replies: Path | None = None,
    barge: bool = False,
) -> str:
    """Timing calibration; with `real` the speech-detection one (the agent replies with corpus
    clips, or the WAVs in `replies`); with `barge` the barge-in one. Each profile runs once
    per codec."""
    out.mkdir(parents=True, exist_ok=True)
    out = out.resolve()
    agent_args, clips = [], None
    if real:
        if replies:
            shutil.copytree(replies, out / "replies", dirs_exist_ok=True)
            agent_args = ["--replies", "/out/replies"]
            clips = {p.stem: speech.read_wav(p) for p in sorted((out / "replies").glob("*.wav"))}
        else:
            clips = {
                n: pcm for n, pcm in speech.clips("tts-", "human-").items() if "-long" not in n
            }
        turns = turns or len(clips)
        gap = max(map(len, clips.values())) / 8000 + SPEECH_DELAY_RANGE[1] + 1.0
        agent_args += ["--speech"]
    if barge:
        agent_args = ["--barge-in"]
    turns = turns or (60 if barge else 20)
    runs = [(p, c) for p in profiles for c in codecs or [""]]
    names = {(p, c): f"{p}-{c}" if c else p for p, c in runs}
    stack = Stack(out)
    try:
        stack.up()
        caller_ip = stack.sh("caller", "hostname -i").split()[0]
        agent_ip = stack.sh("agent", "hostname -i").split()[0]
        conds = conditions(partial(stack.sh, "router"), seed) | {"turns_per_profile": turns}
        conds |= {"codecs": codecs, "speech": real, "barge": barge}
        if replies:
            conds["replies"] = sorted(clips or {})
        (out / "conditions.json").write_text(json.dumps(conds, indent=1))
        for profile, codec in runs:
            name = names[profile, codec]
            run = out / name
            run.mkdir(exist_ok=True)
            stack.netem(PROFILES[profile], [caller_ip, agent_ip])
            args = ["--out", f"/out/{name}", "--seed", str(seed)]
            agent = ["python", "-m", "rtpbench", "agent", *args, *agent_args]
            stack.compose("exec", "-d", "agent", *agent)
            _wait_for(run / "ready", 120)
            print(f"{name}: calling ({turns} turns)", flush=True)
            call = ["call", f"sip:agent@{agent_ip}", "--turns", str(turns), *args]
            if codec:
                call += ["--codec", codec]
            if real:
                call += ["--speech", "--gap", f"{gap:.1f}"]
            if barge:
                call += ["--barge-in"]
            stack.compose("exec", "-T", "caller", "python", "-m", "rtpbench", *call)
            _wait_for(run / "agent.json", 30)
    finally:
        if hasattr(os, "getuid"):  # tcpdump wrote as root; hand the results back
            stack.sh("caller", f"chown -R {os.getuid()}:{os.getgid()} /out", check=False)
        stack.down()
    dirs = {names[r]: out / names[r] for r in runs}
    if barge:
        summary = bargein.summarize(dirs)
    else:
        summary = speechcal.summarize(dirs, clips) if real else analyze.summarize(dirs)
    (out / "summary.md").write_text(summary)
    return summary


def cases(
    out: Path,
    uri: str | None,
    names: list[str],
    profiles: list[str],
    runs: int,
    seed: int,
    iface: str,
    lines: Path | None = None,
) -> tuple[str, bool]:
    """Conformance cases against the reference agent (each behaviour of each case, in Docker
    behind the netem router, `runs` times per profile), or against `uri` from here (capturing on
    `iface`, `runs` times, no netem). Repeat k uses seed + k - 1. Returns the summary and, for
    the reference agent, whether every case was proven in every repeat."""
    from rtpbench import cases as cs
    from rtpbench.capture import capture

    out.mkdir(parents=True, exist_ok=True)
    out = out.resolve()
    done: list[cs.Run] = []
    if uri:
        conds = conditions(_host, seed) | {"target": uri, "iface": iface, "runs": runs}
        conds["python"] = platform.python_version()
        for k in range(1, runs + 1):
            for name in names:
                rel = f"host/{k:02d}/{name}"
                (out / rel).mkdir(parents=True, exist_ok=True)
                print(f"{rel}: calling {uri}", flush=True)
                with capture(out / rel / "caller.pcap", iface):
                    log = cs.run(name, uri, seed + k - 1, lines)
                (out / rel / "caller.json").write_text(json.dumps(log, indent=1))
                done.append(cs.Run("host", k, name, None, rel))
        if uid := os.environ.get("SUDO_UID"):  # run with sudo to capture; hand the results back
            subprocess.run(["chown", "-R", f"{uid}:{os.environ['SUDO_GID']}", str(out)], check=True)
    else:
        stack = Stack(out)
        try:
            stack.up()
            caller_ip = stack.sh("caller", "hostname -i").split()[0]
            agent_ip = stack.sh("agent", "hostname -i").split()[0]
            conds = conditions(partial(stack.sh, "router"), seed)
            conds |= {"profiles": profiles, "runs": runs}
            for profile in profiles:
                stack.netem(PROFILES[profile], [caller_ip, agent_ip])
                for k in range(1, runs + 1):
                    for name in names:
                        for behaviour in cs.CASES[name].behaviours():
                            rel = f"{profile}/{k:02d}/{name}-{behaviour}"
                            (out / rel).mkdir(parents=True, exist_ok=True)
                            args = ["--out", f"/out/{rel}", "--seed", str(seed + k - 1)]
                            agent = ["agent", *args, "--case", name, "--behaviour", behaviour]
                            stack.compose("exec", "-d", "agent", "python", "-m", "rtpbench", *agent)
                            _wait_for(out / rel / "ready", 120)
                            print(f"{rel}: calling", flush=True)
                            call = ["case", name, f"sip:agent@{agent_ip}", *args]
                            stack.compose("exec", "-T", "caller", "python", "-m", "rtpbench", *call)
                            _wait_for(out / rel / "agent.json", 30)
                            done.append(cs.Run(profile, k, name, behaviour, rel))
        finally:
            if hasattr(os, "getuid"):  # tcpdump wrote as root; hand the results back
                stack.sh("caller", f"chown -R {os.getuid()}:{os.getgid()} /out", check=False)
            stack.down()
    (out / "conditions.json").write_text(json.dumps(conds, indent=1))
    summary, ok = judge(out, done)
    return summary, ok or uri is not None


def target(
    out: Path, name: str, names: list[str], profiles: list[str], runs: int, seed: int
) -> str:
    """The cases, a turn-latency call and a barge-in call against the compose target `name`,
    placed from the caller container through the netem router, `runs` times per profile
    (repeat k uses seed + k - 1); returns the summary."""
    from rtpbench import cases as cs

    user, engine_var, engine_default = TARGETS[name]
    out.mkdir(parents=True, exist_ok=True)
    out = out.resolve()

    def inside(*paths: Path) -> list[str]:  # as the caller container sees them
        return [f"/app/{p.relative_to(ROOT).as_posix()}" for p in paths]

    def lines(pattern: str) -> list[str]:
        return inside(*sorted(LINES.glob(pattern)))

    done: list[cs.Run] = []
    stack = Stack(out, name)
    try:
        stack.up()
        caller_ip = stack.sh("caller", "hostname -i").split()[0]
        target_ip = stack.sh("router", "getent hosts target").split()[0]
        router_ip = stack.sh("target", "getent hosts router").split()[0]
        stack.sh("target", f"ip route replace {caller_ip} via {router_ip}")
        url = urlsplit(os.environ.get(engine_var) or engine_default)
        engine = {"domain": ".".join((url.hostname or "").split(".")[-3:]), "query": url.query}
        conds = conditions(partial(stack.sh, "router"), seed)
        conds |= {"profiles": profiles, "runs": runs, "target": name, "engine": engine}
        conds["images"] = stack.compose("images")
        uri = f"sip:{user}@{target_ip}"
        turns = lines("turn-*.wav")
        latency = ["--turns", str(len(turns)), "--lead", "10", "--gap", "15", "--wav", *turns]
        barge = ["--turns", "10", "--lead", "10", "--barge-in", "--wav", *lines("prompt-*.wav")]
        calls = {
            **{c: ["case", c, uri, "--lines", *inside(LINES)] for c in names},
            "latency": ["call", uri, *latency],
            "barge-in": ["call", uri, *barge, "--interrupt", *lines("interrupt-*.wav")],
        }
        for profile in profiles:
            stack.netem(PROFILES[profile], [caller_ip, target_ip])
            for k in range(1, runs + 1):
                for tag, call in calls.items():
                    rel = f"{profile}/{k:02d}/{tag}"
                    print(f"{rel}: calling {uri}", flush=True)
                    args = ["--out", f"/out/{rel}", "--seed", str(seed + k - 1)]
                    stack.compose("exec", "-T", "caller", "python", "-m", "rtpbench", *call, *args)
                done += [cs.Run(profile, k, c, None, f"{profile}/{k:02d}/{c}") for c in names]
        (out / "target.log").write_text(stack.compose("logs", "--no-color", "--timestamps"))
    finally:
        if hasattr(os, "getuid"):  # tcpdump wrote as root; hand the results back
            stack.sh("caller", f"chown -R {os.getuid()}:{os.getgid()} /out", check=False)
        stack.down()
    (out / "conditions.json").write_text(json.dumps(conds, indent=1))
    return judge(out, done)[0]


def judge(out: Path, runs: list[Any] | None = None) -> tuple[str, bool]:
    """Verdicts for the case runs of a results directory (by default the ones its results.json
    lists), plus turn latency and barge-in pooled per profile if it has those calls:
    summary.md, results.json and report.html. Returns the summary and whether every reference
    case was proven in every repeat."""
    from rtpbench import cases as cs
    from rtpbench import report

    if runs is None:
        recs = json.loads((out / "results.json").read_text())
        runs = [cs.Run(*(r[f] for f in cs.Run._fields)) for r in recs]
    summary, records, ok = cs.summarize(out, runs)
    for sub, title, pooled in (
        ("latency", "Turn latency", speechcal.pooled),
        ("barge-in", "Barge-in", bargein.pooled),
    ):
        calls: dict[str, list[Path]] = {}
        for path in sorted(out.glob(f"*/*/{sub}/caller.json")):
            calls.setdefault(path.parts[-4], []).append(path.parent)
        if calls:
            summary += f"\n## {title}\n\n" + pooled(calls)
    (out / "results.json").write_text(json.dumps(records, indent=1))
    (out / "summary.md").write_text(summary)
    (out / "report.html").write_text(report.render(out))
    return summary, ok
