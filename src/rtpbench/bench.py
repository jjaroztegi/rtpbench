"""`rtpbench calibrate`: reference agent behind a netem router, one call per profile and codec."""

import hashlib
import itertools
import json
import os
import platform
import secrets
import shlex
import shutil
import subprocess
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import urlsplit

from rtpbench import analyze, bargein, clock, speech, speechcal
from rtpbench.agent import SPEECH_DELAY_RANGE

if TYPE_CHECKING:  # the CLI's help imports this module for its names; keep that import light
    from rtpbench.progress import Progress

ROOT = Path(__file__).resolve().parents[2]
LINES = ROOT / "corpus" / "lines" / "en"  # the caller's lines against a target
# compose targets, targets/<name>/compose.yaml: the SIP user to dial, and the variables that set
# its AI engine with their defaults (of a URL only its domain and query go into the conditions)
TARGETS = {
    "aivc": (
        "openai",
        {
            "OPENAI_URL": "wss://api.openai.com/v1/realtime?model=gpt-realtime-2.1",
            "OPENAI_REASONING_EFFORT": "low",
        },
    ),
    "livekit": (
        "agent",
        {"AZURE_OPENAI_ENDPOINT": "", "AZURE_OPENAI_DEPLOYMENT": "gpt-realtime-2.1"},
    ),
}
# the same variables pointing at the mock engine (mock/compose.yaml), which takes any key
MOCK = {
    "aivc": {"OPENAI_URL": "ws://realtime:8000/v1/realtime?model=mock", "OPENAI_API_KEY": "mock"},
    "livekit": {
        "AZURE_OPENAI_ENDPOINT": "http://realtime:8000",
        "AZURE_OPENAI_API_KEY": "mock",
        "AZURE_OPENAI_DEPLOYMENT": "mock",
    },
}


def _engine(settings: dict[str, str]) -> dict[str, str]:
    """A target's engine settings as the conditions record them: no account names, no keys."""
    out = {}
    for var, default in settings.items():
        value = os.environ.get(var, default)
        if "://" in value:
            url = urlsplit(value)
            domain = ".".join((url.hostname or "").split(".")[-3:])
            value = f"{domain}?{url.query}" if url.query else domain
        out[var] = value
    return out


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
    """caller | router | agent, plus a target's services when given (on the mock engine with
    `mock`), and the carrier in front of the host `carrier` names (paths in their compose files
    are relative to the repository root). With `uri`, caller | router only, for an agent outside
    the stack: the router also joins the Docker network `network`, and with `ports` (first-last)
    the host publishes that range on the router."""

    def __init__(
        self,
        out: Path,
        target: str | None = None,
        carrier: str | None = None,
        mock: bool = False,
        uri: bool = False,
        network: str | None = None,
        ports: str | None = None,
    ) -> None:
        self.project = f"rtpbench-{secrets.token_hex(3)}"
        self.env = os.environ | {"RTPBENCH_IMAGE": _image_tag(), "RTPBENCH_OUT": str(out)}
        self.files = [ROOT / "compose.yaml"]
        self.services = ["router", "caller"] if uri else []
        self.passed: list[str] = []  # variables passed to the caller's commands, by name only
        if network:
            self.files.append(ROOT / "uri" / "network.yaml")
            self.env["RTPBENCH_NETWORK"] = network
        if ports:
            self.files.append(ROOT / "uri" / "advertise.yaml")
            self.env["RTPBENCH_PORTS"] = ports
        if target:
            self.files.append(ROOT / "targets" / target / "compose.yaml")
        if target and mock:
            self.files.append(ROOT / "mock" / "compose.yaml")
            self.env |= MOCK[target]
        if carrier:
            self.files.append(ROOT / "carrier" / "compose.yaml")
            self.env["RTPBENCH_CARRIER_NEXT"] = carrier
        self.carrier = carrier is not None

    def compose(
        self, *args: str, check: bool = True, lines: Callable[[str], None] | None = None
    ) -> str:
        """Its output; with `lines`, its output and errors together, each line also passed to
        `lines` as it is printed."""
        files = [a for f in self.files for a in ("-f", str(f))]
        cmd = ["docker", "compose", "-p", self.project, *files, *args]
        if lines is None:
            res = subprocess.run(cmd, env=self.env, capture_output=True, text=True)
            code, out, err = res.returncode, res.stdout, res.stderr
        else:
            out = ""
            with subprocess.Popen(
                cmd, env=self.env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            ) as proc:
                for line in proc.stdout or ():
                    lines(line)
                    out += line
            code, err = proc.returncode, out
        if check and code:
            raise RuntimeError(f"{' '.join(args)} failed:\n{err}")
        return out.strip()

    def sh(self, service: str, cmd: str, check: bool = True) -> str:
        return self.compose("exec", "-T", service, "sh", "-c", cmd, check=check)

    def caller(self, *args: str, lines: Callable[[str], None] | None = None) -> str:
        """`rtpbench args` in the caller container."""
        env = [a for name in self.passed for a in ("-e", name)]
        cmd = ["exec", "-T", *env, "caller", "python", "-m", "rtpbench", *args]
        return self.compose(*cmd, lines=lines)

    def up(self, phase: Callable[[str], None]) -> None:
        phase("building images")
        self.compose("build", "-q")
        phase("starting the stack")
        self.compose("up", "-d", "--wait", *self.services)

    def down(self) -> None:
        self.compose("down", "-t", "0", "--remove-orphans", check=False)

    def ip(self, service: str) -> str:
        return self.sh("router", f"getent hosts {service}").split()[0]

    def entry(self, service: str) -> str:
        """Where the caller sends its calls for `service` (the agent, a target, the operator):
        the service, or the carrier."""
        return self.ip("carrier" if self.carrier else service)

    @contextmanager
    def tap(self, rel: str) -> Iterator[None]:
        """With a carrier: capture both of its legs into `rel`/carrier.pcap meanwhile."""
        if not self.carrier:
            yield
            return
        pcap, err = f"/out/{rel}/carrier.pcap", f"/tmp/tap-{secrets.token_hex(3)}"
        cmd = "tcpdump -i eth0 -n -U --immediate-mode -B 32768 --time-stamp-precision=nano"
        pid = self.sh("carrier", f"{cmd} -w {pcap} udp or tcp >/dev/null 2>{err} & echo $!")
        _wait_for(Path(self.env["RTPBENCH_OUT"]) / rel / "carrier.pcap", 10)
        try:
            yield
        finally:
            time.sleep(0.2)
            self.sh(
                "carrier", f"kill -INT {pid}; while kill -0 {pid} 2>/dev/null; do sleep 0.1; done"
            )
            stats = self.sh("carrier", f"cat {err}")
            if "\n0 packets dropped by kernel" not in stats:
                raise RuntimeError(f"tcpdump dropped packets on the carrier:\n{stats}")

    def dev(self, ip: str) -> str:
        """The router's interface towards `ip`."""
        return self.sh("router", f"ip -o route get {ip}").split(" dev ")[1].split()[0]

    def netem(self, args: str, peers: list[str], sip: tuple[int, ...] = (5060,)) -> None:
        """netem on the router's way to each of `peers`; SIP to or from the ports `sip` exempt."""
        for ip in peers:
            dev = self.dev(ip)
            self.sh("router", f"tc qdisc del dev {dev} root 2>/dev/null || true")
            if not args:
                continue
            prio = f"root handle 1: prio bands 3 priomap {' '.join(['2'] * 16)}"
            self.sh("router", f"tc qdisc add dev {dev} {prio}")
            self.sh("router", f"tc qdisc add dev {dev} parent 1:3 handle 30: netem {args}")
            # UDP, TCP
            for proto, way, port in itertools.product((17, 6), ("sport", "dport"), sip):
                match = (
                    f"u32 match ip protocol {proto} 0xff match ip {way} {port} 0xffff flowid 1:1"
                )
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
    """Versions and host; `sh` runs a command in the stack (where the capture runs)."""
    governor = Path("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
    return {
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "commit": _host("git describe --always --dirty"),
        "image": _image_tag(),  # the code the stacks ran, whatever the history
        "kernel": sh("uname -r"),
        "cpus": os.cpu_count(),  # how many, not which model: published conditions name no hardware
        "docker": _host("docker version --format '{{.Server.Version}}'"),
        "python": sh("python3 -V"),
        "tcpdump": sh("tcpdump --version 2>&1 | head -1"),
        "host": platform.platform(),
        "cpu_governor": governor.read_text().strip() if governor.exists() else "",
        "load_start": _load(),
        "seed": seed,
        "netem_per_direction": PROFILES,
    }


def _load() -> list[float]:
    """The host's load averages over 1, 5 and 15 minutes."""
    return [float(x) for x in Path("/proc/loadavg").read_text().split()[:3]]


def _finish(conds: dict[str, Any], steps: list[dict[str, Any]]) -> dict[str, Any]:
    """What the run saw while it ran: wall-clock steps (`clock.watch`) and the load at its end."""
    return conds | {"clock_steps": steps, "load_end": _load()}


def calibrate(
    out: Path,
    profiles: list[str],
    turns: int | None,
    seed: int,
    codecs: list[str] | None = None,
    real: bool = False,
    replies: Path | None = None,
    barge: bool = False,
    carrier: bool = False,
    *,
    progress: Progress,
) -> str:
    """Timing calibration; with `real` the speech-detection one (the agent replies with corpus
    clips, or the WAVs in `replies`); with `barge` the barge-in one; with `carrier` through the
    carrier. Each profile runs once per codec."""
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
    progress.plan(len(runs))
    stack = Stack(out, carrier="agent" if carrier else None)
    try:
        stack.up(progress.phase)
        caller_ip, agent_ip = stack.ip("caller"), stack.entry("agent")
        conds = conditions(partial(stack.sh, "router"), seed) | {"turns_per_profile": turns}
        conds |= {"codecs": codecs, "speech": real, "barge": barge, "carrier": carrier}
        if replies:
            conds["replies"] = sorted(clips or {})
        if carrier:
            conds["images"] = stack.compose("images")
        (out / "conditions.json").write_text(json.dumps(conds, indent=1))
        with clock.watch() as steps:
            for profile, codec in runs:
                name = names[profile, codec]
                run = out / name
                run.mkdir(exist_ok=True)
                progress.unit(name)
                stack.netem(PROFILES[profile], [caller_ip, agent_ip])
                args = ["--out", f"/out/{name}", "--seed", str(seed)]
                agent = ["python", "-m", "rtpbench", "agent", *args, *agent_args]
                stack.compose("exec", "-d", "agent", *agent)
                _wait_for(run / "ready", 120)
                call = ["call", f"sip:agent@{agent_ip}", "--turns", str(turns), *args]
                if codec:
                    call += ["--codec", codec]
                if real:
                    call += ["--speech", "--gap", f"{gap:.1f}"]
                if barge:
                    call += ["--barge-in"]
                with stack.tap(name):
                    stack.caller(*call, lines=progress.turn)
                    _wait_for(run / "agent.json", 30)
                progress.done()
        (out / "conditions.json").write_text(json.dumps(_finish(conds, steps), indent=1))
    finally:
        if hasattr(os, "getuid"):  # tcpdump wrote as root; hand the results back
            stack.sh("caller", f"chown -R {os.getuid()}:{os.getgid()} /out", check=False)
        stack.down()
    progress.phase("analysing")
    dirs = {names[r]: [out / names[r]] for r in runs}
    if barge:
        summary = bargein.summarize(dirs)
    else:
        summary = speechcal.summarize(dirs, clips) if real else analyze.summarize(dirs)
    summary += "\n" + clock.note(clock.steps(out))
    (out / "summary.md").write_text(summary)
    return summary


def cases(
    out: Path,
    names: list[str],
    profiles: list[str],
    runs: int,
    seed: int,
    carrier: bool = False,
    *,
    progress: Progress,
) -> tuple[str, bool]:
    """Conformance cases against the reference agent: each behaviour of each case, in Docker
    behind the netem router and, with `carrier`, the carrier, `runs` times per profile. Repeat k
    uses seed + k - 1. Returns the summary and whether every case was proven in every repeat."""
    from rtpbench import cases as cs

    out.mkdir(parents=True, exist_ok=True)
    out = out.resolve()
    done: list[cs.Run] = []
    progress.plan(len(profiles) * sum(len(cs.CASES[n].behaviours()) for n in names) * runs)
    with clock.watch() as steps:
        stack = Stack(out, carrier="agent" if carrier else None)
        try:
            stack.up(progress.phase)
            caller_ip, agent_ip = stack.ip("caller"), stack.entry("agent")
            proxy = stack.entry("operator")  # the transferee's next hop for a transfer
            conds = conditions(partial(stack.sh, "router"), seed)
            conds |= {"profiles": profiles, "runs": runs, "carrier": carrier}
            if carrier:
                conds["images"] = stack.compose("images")
            for profile in profiles:
                stack.netem(PROFILES[profile], [caller_ip, agent_ip])
                for k in range(1, runs + 1):
                    for name in names:
                        for behaviour in cs.CASES[name].behaviours():
                            rel = f"{profile}/{k:02d}/{name}-{behaviour}"
                            (out / rel).mkdir(parents=True, exist_ok=True)
                            progress.unit(f"{profile} {name}/{behaviour}{_repeat(k, runs)}")
                            args = ["--out", f"/out/{rel}", "--seed", str(seed + k - 1)]
                            agent = ["agent", *args, "--case", name, "--behaviour", behaviour]
                            stack.compose("exec", "-d", "agent", "python", "-m", "rtpbench", *agent)
                            _wait_for(out / rel / "ready", 120)
                            call = ["case", name, f"sip:agent@{agent_ip}", "--proxy", proxy]
                            with stack.tap(rel):
                                stack.caller(*call, *args)
                                _wait_for(out / rel / "agent.json", 30)
                            done.append(cs.Run(profile, k, name, behaviour, rel))
                            _verdict(progress, out / rel, profile, behaviour)
        finally:
            if hasattr(os, "getuid"):  # tcpdump wrote as root; hand the results back
                stack.sh("caller", f"chown -R {os.getuid()}:{os.getgid()} /out", check=False)
            stack.down()
    (out / "conditions.json").write_text(json.dumps(_finish(conds, steps), indent=1))
    progress.phase("judging")
    return judge(out, done)


def _repeat(k: int, runs: int) -> str:
    return f" (repeat {k} of {runs})" if runs > 1 else ""


def _verdict(progress: Progress, run: Path, profile: str, behaviour: str | None) -> None:
    """End the case's unit with its verdict, judged now so a wrong one shows as it happens (the
    summary reuses it)."""
    from rtpbench import cases as cs

    try:
        r = cs.judge(run, profile)
    except Exception as e:  # the summary judges it again, and raises
        progress.done(f"not judged: {e}", False)
        return
    failed = ", ".join(c.name for c in r.checks if not c.ok)
    want = cs.expected(behaviour)
    if want is None:  # a real target: report what failed
        ok = {"pass": True, "fail": False}.get(r.verdict)
        progress.done(r.verdict + (f" ({failed})" if failed else ""), ok)
    elif r.verdict == want:
        progress.done(f"{r.verdict} as expected", True)
    else:
        progress.done(f"{r.verdict}, expected {want}" + (f" ({failed})" if failed else ""), False)


def check_lines(lines: Path, names: list[str]) -> None:
    """Raise unless `lines` has, for the calls in `names`, every line it needs (as in
    corpus/lines/en), each 8 kHz mono 16-bit with speech the labeller can find."""
    from rtpbench import cases as cs

    need = {
        "prompt.wav": any(n in cs.CASES for n in names),
        "transfer.wav": any(n in ("refer", "refer-fail") for n in names),
        "turn-*.wav": "latency" in names,
        "prompt-*.wav": "barge-in" in names,
        "interrupt-*.wav": "barge-in" in names,
    }
    problems = []
    for pattern in (p for p, needed in need.items() if needed):
        if not (files := sorted(lines.glob(pattern))):
            problems.append(f"no {pattern}")
        for f in files:
            try:
                speech.label(speech.read_wav(f))
            except ValueError as e:
                problems.append(f"{f.name}: {e}")
    if problems:
        raise ValueError(f"{lines}: " + "; ".join(problems))


def _reach(
    stack: Stack, caller_ip: str, host: str, network: str | None, advertise: str | None
) -> tuple[str, str | None]:
    """Set the router up for an agent outside the stack, at `host`: replies come back through
    it (so netem holds both ways, not only out) and, when the caller advertises an address
    (`advertise`, or with `network` the router's own there), it forwards the caller's ports.
    Returns the agent's address as the router resolves it and the advertised HOST:PORT."""
    from rtpbench.caller import ADVERTISE_PORT, ADVERTISE_PORTS

    found = stack.sh("router", f"getent ahostsv4 {shlex.quote(host)}", check=False).split()
    if not found:
        raise RuntimeError(f"{host} does not resolve from the stack")
    stack.env["RTPBENCH_RESOLVE"] = f"{host}={found[0]}"
    stack.passed.append("RTPBENCH_RESOLVE")
    callnet = stack.dev(caller_ip)
    stack.sh("router", f"iptables -t nat -A POSTROUTING ! -o {callnet} -j MASQUERADE")
    if network and not advertise:
        route = stack.sh("router", f"ip -o route get {found[0]}").split()
        advertise = f"{route[route.index('src') + 1]}:{ADVERTISE_PORT}"
    if advertise:
        first = int(advertise.rpartition(":")[2])
        span = f"{first}:{first + ADVERTISE_PORTS - 1}"
        dnat = f"-j DNAT --to-destination {caller_ip}"
        for proto in ("udp", "tcp"):
            match = f"! -i {callnet} -p {proto} --dport {span}"
            stack.sh("router", f"iptables -t nat -A PREROUTING {match} {dnat}")
        stack.env["RTPBENCH_ADVERTISE"] = advertise
        stack.passed.append("RTPBENCH_ADVERTISE")
    return found[0], advertise


def target(
    out: Path,
    name: str,
    names: list[str],
    profiles: list[str],
    runs: int,
    seed: int,
    carrier: bool = False,
    mock: bool = False,
    lines: Path | None = None,
    proxy: str | None = None,
    network: str | None = None,
    advertise: str | None = None,
    *,
    progress: Progress,
) -> str:
    """The cases, a turn-latency call and a barge-in call (those of them in `names`) against
    the compose target `name` (on the mock engine with `mock`) or the agent at the SIP URI
    `name`, placed from the caller container through the netem router (and, with `carrier`, the
    carrier), `runs` times per profile (repeat k uses seed + k - 1); returns the summary.

    `lines`: the caller's lines instead of corpus/lines/en. For a URI: `proxy` is where a
    transfer's INVITE goes (else the Refer-To host); the router joins the Docker network
    `network`; the caller advertises `advertise` (HOST:PORT, the host publishing PORT and the
    next few to it), else with `network` its router's address there."""
    from rtpbench import cases as cs
    from rtpbench import realtime
    from rtpbench.caller import ADVERTISE_PORTS, parse_uri

    if lines:
        check_lines(lines, names)
    out.mkdir(parents=True, exist_ok=True)
    out = out.resolve()
    said = LINES
    if lines:
        said = out / "lines"
        shutil.copytree(lines, said, dirs_exist_ok=True)

    def inside(*paths: Path) -> list[str]:  # as the caller container sees them
        return [
            f"/out/{p.relative_to(out).as_posix()}"
            if p.is_relative_to(out)
            else f"/app/{p.relative_to(ROOT).as_posix()}"
            for p in paths
        ]

    def wavs(pattern: str) -> list[str]:
        return inside(*sorted(said.glob(pattern)))

    done: list[cs.Run] = []
    with clock.watch() as steps:
        if name.startswith("sip:"):
            host, port = parse_uri(name)
            ports = None
            if advertise:  # the host publishes the range
                first = int(advertise.rpartition(":")[2])
                ports = f"{first}-{first + ADVERTISE_PORTS - 1}"
            stack = Stack(out, uri=True, network=network, ports=ports)
        else:
            stack = Stack(out, name, "target" if carrier else None, mock)
        try:
            stack.up(progress.phase)
            caller_ip = stack.ip("caller")
            conds = conditions(partial(stack.sh, "router"), seed)
            conds |= {"profiles": profiles, "runs": runs, "target": name, "carrier": carrier}
            conds["mock"] = mock
            if name.startswith("sip:"):
                target_ip, advertise = _reach(stack, caller_ip, host, network, advertise)
                uri, sip = name, tuple(dict.fromkeys((port, 5060)))
                conds |= {"network": network, "advertise": advertise}
            else:
                user, settings = TARGETS[name]
                target_ip, sip = stack.entry("target"), (5060,)
                router_ip = stack.sh("target", "getent hosts router").split()[0]
                stack.sh("target", f"ip route replace {caller_ip} via {router_ip}")
                conds["engine"] = realtime.conditions() if mock else _engine(settings)
                uri, proxy = f"sip:{user}@{target_ip}", stack.entry("operator")
            if lines:
                conds["lines"] = {
                    f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                    for f in sorted(said.glob("*.wav"))
                }
            conds["images"] = stack.compose("images")
            transfer = ["--proxy", proxy] if proxy else []
            turns = wavs("turn-*.wav")
            latency = ["--turns", str(len(turns)), "--lead", "10", "--gap", "15", "--wav", *turns]
            barge = ["--turns", "10", "--lead", "10", "--barge-in", "--wav", *wavs("prompt-*.wav")]
            calls = {
                **{c: ["case", c, uri, *transfer, "--lines", *inside(said)] for c in cs.CASES},
                "latency": ["call", uri, *latency],
                "barge-in": ["call", uri, *barge, "--interrupt", *wavs("interrupt-*.wav")],
            }
            calls = {tag: call for tag, call in calls.items() if tag in names}
            progress.plan(len(profiles) * runs * len(calls))
            for profile in profiles:
                stack.netem(PROFILES[profile], [caller_ip, target_ip], sip)
                for k in range(1, runs + 1):
                    for tag, call in calls.items():
                        rel = f"{profile}/{k:02d}/{tag}"
                        progress.unit(f"{profile} {tag}{_repeat(k, runs)}")
                        args = ["--out", f"/out/{rel}", "--seed", str(seed + k - 1)]
                        (out / rel).mkdir(parents=True, exist_ok=True)
                        try:
                            with stack.tap(rel):
                                stack.caller(*call, *args, lines=progress.turn)
                        except RuntimeError as e:
                            if tag in cs.CASES:
                                raise
                            # the target refused or broke a latency or barge-in call: keep its
                            # capture and the error, and go on; the summary lists it
                            (out / rel / "error.txt").write_text(str(e))
                            progress.done("did not complete", False)
                            continue
                        if tag in cs.CASES:
                            _verdict(progress, out / rel, profile, None)
                        else:
                            progress.done()
                    done += [
                        cs.Run(profile, k, c, None, f"{profile}/{k:02d}/{c}")
                        for c in names
                        if c in cs.CASES
                    ]
            (out / "target.log").write_text(stack.compose("logs", "--no-color", "--timestamps"))
        finally:
            if hasattr(os, "getuid"):  # tcpdump wrote as root; hand the results back
                stack.sh("caller", f"chown -R {os.getuid()}:{os.getgid()} /out", check=False)
            stack.down()
    (out / "conditions.json").write_text(json.dumps(_finish(conds, steps), indent=1))
    progress.phase("judging")
    return judge(out, done)[0]


def _last_line(path: Path) -> str:
    """The error's last line: the caller's exception, when it raised one."""
    return (path.read_text().strip().splitlines() or [""])[-1]


def judge(out: Path, runs: list[Any] | None = None) -> tuple[str, bool]:
    """Verdicts for the case runs of a results directory (by default the ones its results.json
    lists), plus turn latency and barge-in pooled per profile if it has those calls:
    summary.md, results.json and report.html. Returns the summary and whether every reference
    case was proven in every repeat."""
    from rtpbench import cases as cs
    from rtpbench import realtime, report

    if runs is None:
        recs = json.loads((out / "results.json").read_text())
        runs = [cs.Run(*(r[f] for f in cs.Run._fields)) for r in recs]
    summary, records, ok = cs.summarize(out, runs)
    sections: list[tuple[str, str]] = []
    # the agent's stream in every call where it behaves as it should
    agent = [(r.profile, out / r.run) for r in runs if r.behaviour in (None, "good")]
    for sub, title, pooled in (
        ("latency", "Turn latency", speechcal.pooled),
        ("barge-in", "Barge-in", bargein.pooled),
    ):
        calls: dict[str, list[Path]] = {}
        for path in sorted(out.glob(f"*/*/{sub}/caller.json")):
            calls.setdefault(path.parts[-4], []).append(path.parent)
            agent.append((path.parts[-4], path.parent))
        broken = sorted(out.glob(f"*/*/{sub}/error.txt"))
        if calls or broken:
            text = pooled(calls, clock.steps(out)) if calls else ""
            if broken:  # not pooled: no measurement, but not to be dropped silently either
                text += "\nDid not complete (see error.txt):\n\n" + "".join(
                    f"- {p.parent.relative_to(out).as_posix()}: {_last_line(p)}\n" for p in broken
                )
            sections.append((title, text))
            summary += f"\n## {title}\n\n" + text
    if (out / "realtime.jsonl").exists() and (parts := realtime.decompose(out)):
        sections.append(("Turn latency by part", parts))
        summary += "\n## Turn latency by part\n\n" + parts
    if paced := cs.pacing(agent):
        sections.append(("RTP pacing", paced))
        summary += "\n## RTP pacing\n\n" + paced
    (out / "results.json").write_text(json.dumps(records, indent=1))
    (out / "summary.md").write_text(summary)
    (out / "report.html").write_text(report.render(out, sections))
    return summary, ok
