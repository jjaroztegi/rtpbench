"""`rtpbench calibrate`: reference agent behind a netem router, one call per profile and codec."""

import hashlib
import json
import os
import platform
import secrets
import shutil
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from rtpbench import analyze, bargein, speech, speechcal
from rtpbench.agent import SPEECH_DELAY_RANGE

ROOT = Path(__file__).resolve().parents[2]
# netem arguments per direction, applied to both router egress interfaces; SIP is exempt
PROFILES = {
    "clean": "",
    "delay": "delay 40ms",
    "jitter": "delay 40ms 10ms distribution normal",
    "loss": "loss 3%",
    "mobile": "delay 60ms 20ms distribution normal loss 3%",
}


def _image_tag() -> str:
    h = hashlib.sha256((ROOT / "Dockerfile").read_bytes())
    for f in sorted([*(ROOT / "src").rglob("*.py"), *(ROOT / "corpus").glob("*.wav")]):
        h.update(f.relative_to(ROOT).as_posix().encode() + f.read_bytes())
    return "rtpbench:" + h.hexdigest()[:12]


class Stack:
    def __init__(self, out: Path) -> None:
        self.project = f"rtpbench-{secrets.token_hex(3)}"
        self.env = os.environ | {"RTPBENCH_IMAGE": _image_tag(), "RTPBENCH_OUT": str(out)}

    def compose(self, *args: str, check: bool = True) -> str:
        cmd = ["docker", "compose", "-p", self.project, "-f", str(ROOT / "compose.yaml"), *args]
        res = subprocess.run(cmd, env=self.env, capture_output=True, text=True)
        if check and res.returncode:
            raise RuntimeError(f"{' '.join(args)} failed:\n{res.stderr}")
        return res.stdout.strip()

    def sh(self, service: str, cmd: str, check: bool = True) -> str:
        return self.compose("exec", "-T", service, "sh", "-c", cmd, check=check)

    def up(self) -> None:
        self.compose("build", "-q", "router")
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


def conditions(stack: Stack, turns: int, seed: int) -> dict[str, Any]:
    def run(*cmd: str) -> str:
        return subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT).stdout.strip()

    cpu = stack.sh("router", "grep -m1 'model name' /proc/cpuinfo | cut -d: -f2")
    return {
        "date": datetime.now(UTC).isoformat(timespec="seconds"),
        "commit": run("git", "describe", "--always", "--dirty"),
        "kernel": stack.sh("router", "uname -r"),
        "cpu": cpu.strip(),
        "docker": run("docker", "version", "--format", "{{.Server.Version}}"),
        "python": stack.sh("router", "python -V"),
        "tcpdump": stack.sh("router", "tcpdump --version 2>&1 | head -1"),
        "host": platform.platform(),
        "turns_per_profile": turns,
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
        conds = conditions(stack, turns, seed) | {"codecs": codecs, "speech": real, "barge": barge}
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
