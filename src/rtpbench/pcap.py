"""Classic pcap reader (as written by tcpdump -w): IPv4/UDP datagrams with ns timestamps."""

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
    if data[:4] not in _MAGIC:
        raise ValueError(f"{path}: not a classic pcap file")
    order, scale = _MAGIC[data[:4]]
    link = struct.unpack_from(order + "I", data, 20)[0] & 0x0FFFFFFF
    record = struct.Struct(order + "IIII")
    out, pos = [], 24
    while pos + 16 <= len(data):
        sec, frac, incl, _ = record.unpack_from(data, pos)
        frame = data[pos + 16 : pos + 16 + incl]
        pos += 16 + incl
        ip = _ip_offset(link, frame)
        if ip is None or len(frame) < ip + 28 or frame[ip + 9] != 17:
            continue
        if struct.unpack_from("!H", frame, ip + 6)[0] & 0x3FFF:  # fragment
            continue
        udp = ip + 4 * (frame[ip] & 0x0F)
        sport, dport, length = struct.unpack_from("!HHH", frame, udp)
        out.append(
            Datagram(
                sec * 1_000_000_000 + frac * scale,
                socket.inet_ntoa(frame[ip + 12 : ip + 16]),
                sport,
                socket.inet_ntoa(frame[ip + 16 : ip + 20]),
                dport,
                frame[udp + 8 : udp + length],
            )
        )
    return out
