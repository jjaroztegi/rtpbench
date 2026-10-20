"""SRTP (RFC 3711) keyed in the SDP (SDES, RFC 4568): protecting and opening RTP packets for the
caller and the reference agent, and for judging, which opens the captured packets with the keys
in the captured SDP. AES counter mode with HMAC-SHA1, and AES-GCM (RFC 7714); no MKI, no
session parameters, key derivation rate 0."""

import base64
import hmac
import secrets
import struct
from dataclasses import dataclass

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from rtpbench import sip


@dataclass(frozen=True)
class Suite:
    salt: int  # master and session salt, bytes
    tag: int  # authentication tag, bytes
    gcm: bool


KEY = 16  # master and session key, bytes
SUITES = {  # in the order the caller offers them
    "AES_CM_128_HMAC_SHA1_80": Suite(14, 10, False),
    "AES_CM_128_HMAC_SHA1_32": Suite(14, 4, False),
    "AEAD_AES_128_GCM": Suite(12, 16, True),
}
_ENCRYPTION, _AUTHENTICATION, _SALT = 0, 1, 2  # key derivation labels (RFC 3711 4.3.2)


def _prf(key: bytes, salt: bytes, label: int, length: int) -> bytes:
    """AES-CM key derivation (RFC 3711 4.3.1) at index 0; a 12-byte salt (AES-GCM, RFC 7714 11)
    padded with zeros, as libsrtp and pion do."""
    x = bytearray(salt.ljust(14, b"\0") + b"\0\0")
    x[7] ^= label
    enc = Cipher(algorithms.AES(key), modes.CTR(bytes(x))).encryptor()
    return enc.update(b"\0" * length) + enc.finalize()


def _header(data: bytes) -> int:
    """Length of the RTP header, CSRCs and extension included."""
    n = 12 + 4 * (data[0] & 0x0F)
    if data[0] & 0x10 and len(data) >= n + 4:
        n += 4 + 4 * struct.unpack_from("!H", data, n + 2)[0]
    return n


class Context:
    """One direction's crypto context (RFC 3711 3.2) from its master key and salt, for every SSRC
    it carries: `protect` for the sender, which knows each packet's index; `open` for whoever
    receives (a peer, or judging), which estimates the index with a rollover counter per SSRC
    (3.3.1). `state` carries those counters over from the context a new key replaces: a rekey
    does not reset them (RFC 3711 3.3.1)."""

    def __init__(
        self, suite: str, master: bytes, state: dict[int, tuple[int, int]] | None = None
    ) -> None:
        spec = SUITES[suite]
        key, salt = master[:KEY], master[KEY:]
        self.suite, self.master, self.spec = suite, master, spec
        self.key = _prf(key, salt, _ENCRYPTION, KEY)
        self.salt = _prf(key, salt, _SALT, spec.salt)
        self.auth = b"" if spec.gcm else _prf(key, salt, _AUTHENTICATION, 20)
        # SSRC: rollover counter, highest seq
        self.state: dict[int, tuple[int, int]] = {} if state is None else state

    def _iv(self, ssrc: int, index: int) -> bytes:
        if self.spec.gcm:  # RFC 7714 8.1
            block = struct.pack("!xxIIH", ssrc, index >> 16, index & 0xFFFF)
            return bytes(a ^ b for a, b in zip(block, self.salt, strict=True))
        iv = int.from_bytes(self.salt) << 16 ^ ssrc << 64 ^ index << 16  # RFC 3711 4.1.1
        return iv.to_bytes(16)

    def _ctr(self, ssrc: int, index: int, data: bytes) -> bytes:
        return (
            Cipher(algorithms.AES(self.key), modes.CTR(self._iv(ssrc, index)))
            .encryptor()
            .update(data)
        )

    def _tag(self, packet: bytes, roc: int) -> bytes:
        return hmac.digest(self.auth, packet + struct.pack("!I", roc), "sha1")[: self.spec.tag]

    def protect(self, packet: bytes, index: int) -> bytes:
        """`packet` (RTP) as SRTP; `index`: its 48-bit packet index, rollover counter and seq."""
        n, ssrc = _header(packet), struct.unpack_from("!I", packet, 8)[0]
        head, body = packet[:n], packet[n:]
        if self.spec.gcm:
            return head + AESGCM(self.key).encrypt(self._iv(ssrc, index), body, head)
        out = head + self._ctr(ssrc, index, body)
        return out + self._tag(out, index >> 16)

    def open(self, data: bytes) -> bytes | None:
        """The RTP packet in `data` (SRTP), or None if it does not authenticate."""
        if len(data) < 12 + self.spec.tag or len(data) < _header(data) + self.spec.tag:
            return None
        n = _header(data)
        ssrc, seq = struct.unpack_from("!I", data, 8)[0], struct.unpack_from("!H", data, 2)[0]
        roc, high = self.state.get(ssrc, (0, seq))
        if high < 32768:  # the guess of RFC 3711 3.3.1: the closest index to the highest yet
            v = roc - 1 if seq - high > 32768 else roc
        else:
            v = roc + 1 if high - 32768 > seq else roc
        if v < 0:
            return None
        index = v << 16 | seq
        if self.spec.gcm:
            try:
                body = AESGCM(self.key).decrypt(self._iv(ssrc, index), data[n:], data[:n])
            except InvalidTag:
                return None
        else:
            packet, tag = data[: -self.spec.tag], data[-self.spec.tag :]
            if not hmac.compare_digest(self._tag(packet, v), tag):
                return None
            body = self._ctr(ssrc, index, packet[n:])
        if v > roc:
            roc, high = v, seq
        elif v == roc and seq > high:
            high = seq
        self.state[ssrc] = (roc, high)
        return data[:n] + body


def master() -> dict[str, bytes]:
    """A fresh master key and salt for each suite."""
    return {name: secrets.token_bytes(KEY + s.salt) for name, s in SUITES.items()}


def line(tag: int, suite: str, key: bytes) -> str:
    """An `a=crypto` value (RFC 4568 9.1)."""
    return f"{tag} {suite} inline:{base64.b64encode(key).decode()}"


def parse(value: str) -> tuple[int, str, bytes]:
    """Tag, suite and master key and salt of an `a=crypto` value; ValueError if this cannot
    use it (an unknown suite, MKI, session parameters, a key of the wrong length)."""
    fields = value.split()
    if len(fields) != 3 or not fields[0].isdigit() or fields[1] not in SUITES:
        raise ValueError(
            f"a=crypto:{value}: not supported (one known suite, no session parameters)"
        )
    params = fields[2].removeprefix("inline:").split("|")
    if not fields[2].startswith("inline:") or len(params) > 2 or ":" in params[-1]:
        raise ValueError(f"a=crypto:{value}: not supported (one inline key, no MKI)")
    key = base64.b64decode(params[0] + "=" * (-len(params[0]) % 4))
    if len(key) != KEY + SUITES[fields[1]].salt:
        raise ValueError(f"a=crypto:{value}: the key and salt are {len(key)} bytes")
    return int(fields[0]), fields[1], key


class Keyring:
    """Opens the packets of one direction of a captured call with any of the keys its side gave
    in the SDP: the one that authenticates a packet's SSRC stays with it until one fails. The
    keys share one rollover counter per SSRC, as the side's successive keys do."""

    def __init__(self, keys: list[tuple[str, bytes]]) -> None:
        state: dict[int, tuple[int, int]] = {}
        self.contexts = [Context(s, k, state) for s, k in dict.fromkeys(keys)]
        self.bound: dict[int, Context] = {}
        self.failed = 0  # packets that no key opened

    def open(self, data: bytes) -> bytes | None:
        ssrc = struct.unpack_from("!I", data, 8)[0] if len(data) >= 12 else 0
        first = [self.bound[ssrc]] if ssrc in self.bound else []
        for ctx in [*first, *(c for c in self.contexts if c not in first)]:
            if (plain := ctx.open(data)) is not None:
                self.bound[ssrc] = ctx
                return plain
        self.failed += 1
        return None


def keyrings(msgs: list[tuple[bool, bytes]]) -> tuple[Keyring, Keyring] | None:
    """Keyrings for the caller's packets and the agent's, from the bodies of the SIP messages
    of a call (whether the caller sent it, body); None if none offered SRTP."""
    keys: dict[bool, list[tuple[str, bytes]]] = {True: [], False: []}
    for from_caller, body in msgs:
        for value in sip.parse_sdp(body).crypto if body else []:
            try:
                _, suite, key = parse(value)
            except ValueError:
                continue
            keys[from_caller].append((suite, key))
    if not keys[True] and not keys[False]:
        return None
    return Keyring(keys[True]), Keyring(keys[False])
