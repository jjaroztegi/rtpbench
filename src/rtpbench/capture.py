"""tcpdump as a context manager: the pcap is the timing source of truth."""

import signal
import subprocess
import sys
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def capture(path: Path, iface: str = "eth0", bpf: str = "udp or tcp") -> Iterator[None]:
    # Immediate mode: without it libpcap hands packets over in blocks of up to a second, and
    # stopping tcpdump right after a BYE loses the end of the call. 32 MiB of kernel buffer
    # (default 2): a busy host once starved a capture of four streams into a drop.
    cmd = ["tcpdump", "-i", iface, "-n", "-Z", "root", "--immediate-mode", "-B", "32768"]
    cmd += ["--time-stamp-precision=nano", "-w", str(path), bpf]
    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)
    assert proc.stderr is not None
    line = proc.stderr.readline()
    if "listening on" not in line:
        proc.kill()
        raise RuntimeError(f"tcpdump did not start: {line.strip()}")
    try:
        yield
    finally:
        time.sleep(0.2)
        proc.send_signal(signal.SIGINT)
        _, err = proc.communicate(timeout=10)
        print(f"{path.name}: " + "; ".join(err.split("\n")[:3]).strip("; "), file=sys.stderr)
        if "\n0 packets dropped by kernel" not in err:
            raise RuntimeError(f"tcpdump dropped packets writing {path}:\n{err}")
