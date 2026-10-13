"""RTP packets and a 20 ms media clock with kernel receive timestamps."""

import socket
import struct
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass

FRAME = 160  # samples per 20 ms packet at 8 kHz
PTIME_NS = 20_000_000
SAMPLE_NS = 125_000
SO_TIMESTAMPNS = 35  # Linux value; Python does not export it
_HEADER = struct.Struct("!BBHII")


@dataclass(frozen=True, slots=True)
class Packet:
    pt: int
    seq: int
    ts: int
    ssrc: int
    marker: bool
    payload: bytes


def pack(pt: int, seq: int, ts: int, ssrc: int, payload: bytes, marker: bool = False) -> bytes:
    return _HEADER.pack(0x80, pt | (0x80 if marker else 0), seq, ts, ssrc) + payload


def parse(data: bytes) -> Packet | None:
    if len(data) < 12 or data[0] >> 6 != 2:
        return None
    b0, b1, seq, ts, ssrc = _HEADER.unpack_from(data)
    start = 12 + 4 * (b0 & 0x0F)
    if b0 & 0x10:
        if len(data) < start + 4:
            return None
        start += 4 + 4 * struct.unpack_from("!H", data, start + 2)[0]
    end = len(data) - (data[-1] if b0 & 0x20 else 0)
    if start > end:
        return None
    return Packet(b1 & 0x7F, seq, ts, ssrc, bool(b1 & 0x80), data[start:end])


def sleep_until(t_ns: int) -> None:
    """Sleep to an absolute CLOCK_REALTIME instant; spin the last millisecond for precision."""
    while (left := t_ns - time.time_ns()) > 1_000_000:
        time.sleep((left - 1_000_000) / 1e9)
    while time.time_ns() < t_ns:
        pass


@dataclass(frozen=True, slots=True)
class Frame:
    """A packet whose payload type, timestamp or marker the source sets itself."""

    pt: int
    payload: bytes
    ts: int
    marker: bool = False


class Sender(threading.Thread):
    """Sends one packet per 20 ms tick on an absolute schedule from `start_ns`.

    `source(n, tick_ns)` returns tick n's payload (timestamp n * 160, marker on the first packet
    after a pause), a full `Frame`, or None to send nothing. Seq counts packets sent (RFC 3550),
    so with no pauses tick n carries seq `seq0 + n`.
    """

    def __init__(
        self,
        sock: socket.socket,
        addr: tuple[str, int],
        pt: int,
        source: Callable[[int, int], bytes | Frame | None],
        start_ns: int,
        seq0: int,
        ssrc: int,
    ) -> None:
        super().__init__(daemon=True)
        self.sock, self.addr, self.pt, self.source = sock, addr, pt, source
        self.start_ns, self.seq0, self.ssrc = start_ns, seq0, ssrc
        self.stop = threading.Event()

    def run(self) -> None:
        n, sent, paused = 0, 0, True
        while not self.stop.is_set():
            tick = self.start_ns + n * PTIME_NS
            out = self.source(n, tick)
            sleep_until(tick)
            if out is not None:
                if not isinstance(out, Frame):
                    out = Frame(self.pt, out, n * FRAME, paused)
                seq = (self.seq0 + sent) & 0xFFFF
                data = pack(out.pt, seq, out.ts & 0xFFFFFFFF, self.ssrc, out.payload, out.marker)
                self.sock.sendto(data, self.addr)
                sent += 1
            paused = out is None
            n += 1


class Receiver(threading.Thread):
    """Calls `sink(arrival_ns, packet)` for each RTP packet, stamped by the kernel on arrival."""

    def __init__(self, sock: socket.socket, sink: Callable[[int, Packet], None]) -> None:
        super().__init__(daemon=True)
        sock.setsockopt(socket.SOL_SOCKET, SO_TIMESTAMPNS, 1)
        sock.settimeout(0.2)
        self.sock, self.sink = sock, sink
        self.stop = threading.Event()

    def run(self) -> None:
        while not self.stop.is_set():
            try:
                data, anc, _flags, _addr = self.sock.recvmsg(2048, 64)
            except TimeoutError:
                continue
            except OSError:
                return
            arrival = time.time_ns()
            for level, kind, raw in anc:
                if level == socket.SOL_SOCKET and kind == SO_TIMESTAMPNS:
                    sec, nsec = struct.unpack("qq", raw[:16])
                    arrival = sec * 1_000_000_000 + nsec
            if (pkt := parse(data)) is not None:
                self.sink(arrival, pkt)
