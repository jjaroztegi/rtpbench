"""tcpdump as a context manager: the pcap is the timing source of truth."""

import signal
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def capture(path: Path, iface: str = "eth0", bpf: str = "udp") -> Iterator[None]:
    cmd = ["tcpdump", "-i", iface, "-n", "-Z", "root", "--time-stamp-precision=nano"]
    proc = subprocess.Popen([*cmd, "-w", str(path), bpf], stderr=subprocess.PIPE, text=True)
    assert proc.stderr is not None
    line = proc.stderr.readline()
    if "listening on" not in line:
        proc.kill()
        raise RuntimeError(f"tcpdump did not start: {line.strip()}")
    try:
        yield
    finally:
        proc.send_signal(signal.SIGINT)
        proc.wait(timeout=10)
