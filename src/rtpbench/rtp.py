"""RTP packets and a 20 ms media clock with kernel receive timestamps."""

import socket
import struct
import threading
from collections.abc import Callable
from dataclasses import dataclass

from rtpbench.clock import CLOCK, Clock
from rtpbench.srtp import Context

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


@dataclass(frozen=True, slots=True)
class Frame:
    """A packet whose payload type, timestamp or marker the source sets itself."""

    pt: int
    payload: bytes
    ts: int
    marker: bool = False


class Sender(threading.Thread):
    """Sends one packet per 20 ms tick on an absolute schedule from `start_ns` on `clock`.

    `source(n, tick_ns)` returns tick n's payload (timestamp n * 160, marker on the first packet
    after a pause), a full `Frame`, or None to send nothing. Seq counts packets sent (RFC 3550),
    so with no pauses tick n carries seq `seq0 + n`. With `srtp`, packets go out protected.
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
        clock: Clock = CLOCK,
        srtp: Context | None = None,
    ) -> None:
        super().__init__(daemon=True)
        self.sock, self.addr, self.pt, self.source, self.clock = sock, addr, pt, source, clock
        self.srtp = srtp
        self.start_ns, self.seq0, self.ssrc = start_ns, seq0, ssrc
        self.stop = threading.Event()
        self.ts0 = 0  # added to every timestamp
        self.new: tuple[int, int, int] | None = None  # switch to (ssrc, seq, ts) at the next tick
        self.switched: int | None = None  # the tick it did
        self.send_errors: list[tuple[int, str]] = []  # (tick, error) of packets the host refused

    def switch(self, ssrc: int, seq: int, ts: int) -> None:
        """From the next packet on, be a new source (RFC 3550: new SSRC, its own random seq and
        timestamp origin): the next packet has `seq`, timestamp `ts` and the marker."""
        self.new = ssrc, seq, ts

    def run(self) -> None:
        n, sent, paused = 0, 0, True
        while not self.stop.is_set():
            tick = self.start_ns + n * PTIME_NS
            out = self.source(n, tick)
            # SRTP is protected before the tick, so encrypting does not delay the send; a switch
            # set meanwhile (from another thread) has it packed again
            early = None
            if self.srtp and out is not None and self.new is None:
                early = self._packet(out, n, sent, paused)
            self.clock.sleep_until(tick)
            if self.new is not None:
                (self.ssrc, self.seq0, ts), self.new = self.new, None
                self.ts0, sent, paused, self.switched = ts - n * FRAME, 0, True, n
                early = None
            if out is not None:
                data = early or self._packet(out, n, sent, paused)
                try:
                    self.sock.sendto(data, self.addr)
                except OSError as e:
                    # refused by the host (a conntrack clash when both ends start at once
                    # gives EPERM): lost before the wire; its seq is spent, the stream goes on
                    self.send_errors.append((n, f"{type(e).__name__}: {e}"))
                sent += 1
            paused = out is None
            n += 1

    def _packet(self, out: bytes | Frame, n: int, sent: int, paused: bool) -> bytes:
        """Tick n's packet, the `sent`th of this source."""
        if not isinstance(out, Frame):
            out = Frame(self.pt, out, n * FRAME, paused)
        seq = (self.seq0 + sent) & 0xFFFF
        ts = (out.ts + self.ts0) & 0xFFFFFFFF
        packet = pack(out.pt, seq, ts, self.ssrc, out.payload, out.marker)
        # its index counts on from seq0: the rollover counter starts at 0 (RFC 3711 3.3.1)
        return self.srtp.protect(packet, self.seq0 + sent) if self.srtp else packet


class Receiver(threading.Thread):
    """Calls `sink(arrival_ns, packet)` for each RTP packet, stamped by the kernel on arrival
    (CLOCK_REALTIME) and put on `clock`; with `srtp`, each that it opens (it may change)."""

    def __init__(
        self,
        sock: socket.socket,
        sink: Callable[[int, Packet], None],
        clock: Clock = CLOCK,
        srtp: Context | None = None,
    ) -> None:
        super().__init__(daemon=True)
        sock.setsockopt(socket.SOL_SOCKET, SO_TIMESTAMPNS, 1)
        sock.settimeout(0.2)
        self.sock, self.sink, self.clock, self.srtp = sock, sink, clock, srtp
        self.stop = threading.Event()

    def run(self) -> None:
        while not self.stop.is_set():
            try:
                data, anc, _flags, _addr = self.sock.recvmsg(2048, 64)
            except TimeoutError:
                continue
            except OSError:
                return
            arrival = self.clock.now()
            for level, kind, raw in anc:
                if level == socket.SOL_SOCKET and kind == SO_TIMESTAMPNS:
                    sec, nsec = struct.unpack("qq", raw[:16])
                    arrival = self.clock.steady(sec * 1_000_000_000 + nsec)
            if self.srtp:
                if (opened := self.srtp.open(data)) is None:
                    continue
                data = opened
            if (pkt := parse(data)) is not None:
                self.sink(arrival, pkt)
