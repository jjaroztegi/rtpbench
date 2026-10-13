"""G.711 µ-law (PT 0) and A-law (PT 8), after the Sun reference implementation."""

import re
from collections.abc import Iterable

PCMU, PCMA = 0, 8
NAMES = {PCMU: "PCMU", PCMA: "PCMA"}
SILENCE = {PCMU: 0xFF, PCMA: 0xD5}

_SEG_END = (0x3F, 0x7F, 0xFF, 0x1FF, 0x3FF, 0x7FF, 0xFFF, 0x1FFF)


def _segment(value: int, ends: Iterable[int]) -> int:
    for seg, end in enumerate(ends):
        if value <= end:
            return seg
    return 8


def ulaw_encode(sample: int) -> int:
    value = sample >> 2
    mask = 0xFF
    if value < 0:
        value, mask = -value, 0x7F
    value = min(value, 8159) + 0x21
    seg = _segment(value, _SEG_END)
    if seg >= 8:
        return 0x7F ^ mask
    return ((seg << 4) | ((value >> (seg + 1)) & 0xF)) ^ mask


def ulaw_decode(code: int) -> int:
    code = ~code & 0xFF
    t = (((code & 0xF) << 3) + 0x84) << ((code & 0x70) >> 4)
    return 0x84 - t if code & 0x80 else t - 0x84


def alaw_encode(sample: int) -> int:
    value = sample >> 3
    mask = 0xD5
    if value < 0:
        value, mask = -value - 1, 0x55
    seg = _segment(value, (e >> 1 for e in _SEG_END))
    if seg >= 8:
        return 0x7F ^ mask
    shift = 1 if seg < 2 else seg
    return ((seg << 4) | ((value >> shift) & 0xF)) ^ mask


def alaw_decode(code: int) -> int:
    code ^= 0x55
    t = (code & 0xF) << 4
    seg = (code & 0x70) >> 4
    if seg == 0:
        t += 8
    else:
        t = (t + 0x108) << (seg - 1)
    return t if code & 0x80 else -t


_ENCODE = {PCMU: ulaw_encode, PCMA: alaw_encode}
_DECODE = {PCMU: ulaw_decode, PCMA: alaw_decode}


def encode(pt: int, samples: Iterable[int]) -> bytes:
    enc = _ENCODE[pt]
    return bytes(enc(s) for s in samples)


def decode(pt: int, payload: bytes) -> list[int]:
    dec = _DECODE[pt]
    return [dec(b) for b in payload]


def gate(pt: int, threshold: int) -> re.Pattern[bytes]:
    """A regex matching one encoded sample whose magnitude reaches `threshold`.

    `search` on a payload gives the first active sample; on the reversed payload, the last.
    """
    dec = _DECODE[pt]
    codes = bytes(b for b in range(256) if abs(dec(b)) >= threshold)
    return re.compile(b"[" + re.escape(codes) + b"]")
