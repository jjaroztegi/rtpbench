"""Classic pcap reader (as written by tcpdump -w): IPv4 UDP datagrams and TCP segments with
data, with ns timestamps."""

import socket
import struct
from dataclasses import dataclass
from pathlib import Path

_MAGIC = {
    b"\xd4\xc3\xb2\xa1": ("<", 1000),
    b"\x4d\x3c\xb2\xa1": ("<", 1),
    b"\xa1\xb2\xc3\xd4": (">", 1000),
    b"\xa1\xb2\x3c\x4d": (">", 1),
}
_ETHERNET, _RAW, _SLL, _SLL2 = 1, 101, 113, 276


@dataclass(frozen=True, slots=True)
class Datagram:
    t_ns: int
    src: str
    sport: int
    dst: str
    dport: int
    payload: bytes
    tcp: bool = False
    seq: int = 0  # TCP sequence number of the payload's first byte


def _ip_offset(link: int, frame: bytes) -> int | None:
    if link == _ETHERNET:
        off, ethertype = 14, struct.unpack_from("!H", frame, 12)[0]
        while ethertype == 0x8100:
            ethertype = struct.unpack_from("!H", frame, off + 2)[0]
            off += 4
        return off if ethertype == 0x0800 else None
    if link == _SLL:
        return 16 if struct.unpack_from("!H", frame, 14)[0] == 0x0800 else None
    if link == _SLL2:
        return 20 if struct.unpack_from("!H", frame, 0)[0] == 0x0800 else None
    return 0 if link == _RAW else None


def read(path: Path) -> list[Datagram]:
    data = path.read_bytes()
    if len(data) < 24 or data[:4] not in _MAGIC:
        raise ValueError(f"{path}: not a classic pcap file")
    order, scale = _MAGIC[data[:4]]
    link = struct.unpack_from(order + "I", data, 20)[0] & 0x0FFFFFFF
    record = struct.Struct(order + "IIII")
    out, pos = [], 24
    while pos + 16 <= len(data):
        sec, frac, incl, _ = record.unpack_from(data, pos)
        frame = data[pos + 16 : pos + 16 + incl]
        pos += 16 + incl
        try:
            ip = _ip_offset(link, frame)
        except struct.error:  # shorter than its link header says
            continue
        if ip is None or len(frame) < ip + 28 or frame[ip + 9] not in (6, 17):
            continue
        if struct.unpack_from("!H", frame, ip + 6)[0] & 0x3FFF:  # fragment
            continue
        t = sec * 1_000_000_000 + frac * scale
        src, dst = (
            socket.inet_ntoa(frame[ip + 12 : ip + 16]),
            socket.inet_ntoa(frame[ip + 16 : ip + 20]),
        )
        l4 = ip + 4 * (frame[ip] & 0x0F)
        if frame[ip + 9] == 6:  # TCP: segments that carry data
            end = ip + struct.unpack_from("!H", frame, ip + 2)[0]
            if len(frame) < l4 + 20 or len(frame) < end:
                continue
            sport, dport, seq = struct.unpack_from("!HHI", frame, l4)
            body = frame[l4 + 4 * (frame[l4 + 12] >> 4) : end]
            if body:
                out.append(Datagram(t, src, sport, dst, dport, body, True, seq))
            continue
        if len(frame) < l4 + 8:
            continue
        sport, dport, length = struct.unpack_from("!HHH", frame, l4)
        if length < 8 or len(frame) < l4 + length:  # cut short by the snaplen
            continue
        out.append(Datagram(t, src, sport, dst, dport, frame[l4 + 8 : l4 + length]))
    return out


def streams(grams: list[Datagram]) -> list[Datagram]:
    """The TCP segments of `grams` that add bytes to their flow's stream, in capture order,
    each cut to the bytes it adds (a retransmission adds none)."""
    out: list[Datagram] = []
    nxt: dict[tuple[str, int, str, int], int] = {}  # next sequence number per flow
    for g in grams:
        if not g.tcp:
            continue
        flow = (g.src, g.sport, g.dst, g.dport)
        seen = (nxt.get(flow, g.seq) - g.seq) & 0xFFFFFFFF
        if seen >= 1 << 31:  # a gap: bytes lost before the capture saw them
            seen = 0
        if seen >= len(g.payload):
            continue
        nxt[flow] = (g.seq + len(g.payload)) & 0xFFFFFFFF
        out.append(Datagram(g.t_ns, *flow, g.payload[seen:], True, g.seq + seen))
    return out
