"""SIP over TLS read back from a capture: TLS connections in the TCP streams decrypted with the
caller's key log (the SSLKEYLOGFILE format OpenSSL and Wireshark use), so judging reads the
messages that crossed the wire at the times they crossed it. TLS 1.3, and TLS 1.2 with the
AEAD suites the caller offers. Also the stack's test certificates."""

import bisect
import datetime
import hmac
import struct
from pathlib import Path

from cryptography import x509
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

from rtpbench import pcap

Aead = type[AESGCM] | type[ChaCha20Poly1305]
# cipher suite: AEAD, key length, hash
TLS13: dict[int, tuple[Aead, int, str]] = {
    0x1301: (AESGCM, 16, "sha256"),
    0x1302: (AESGCM, 32, "sha384"),
    0x1303: (ChaCha20Poly1305, 32, "sha256"),
}
TLS12: dict[int, tuple[Aead, int, str]] = {
    0xC02B: (AESGCM, 16, "sha256"),  # ECDHE-ECDSA-AES128-GCM-SHA256
    0xC02F: (AESGCM, 16, "sha256"),  # ECDHE-RSA-AES128-GCM-SHA256
    0xC02C: (AESGCM, 32, "sha384"),  # ECDHE-ECDSA-AES256-GCM-SHA384
    0xC030: (AESGCM, 32, "sha384"),  # ECDHE-RSA-AES256-GCM-SHA384
    0xCCA8: (ChaCha20Poly1305, 32, "sha256"),  # ECDHE-RSA-CHACHA20-POLY1305
    0xCCA9: (ChaCha20Poly1305, 32, "sha256"),  # ECDHE-ECDSA-CHACHA20-POLY1305
}
CIPHERS_12 = "ECDHE+AESGCM:ECDHE+CHACHA20"  # what the caller offers below TLS 1.3: AEAD only
_HASHES = {"sha256": hashes.SHA256, "sha384": hashes.SHA384}
_HANDSHAKE, _CHANGE_CIPHER_SPEC, _APPLICATION_DATA, _KEY_UPDATE = 22, 20, 23, 24

Flow = tuple[str, int, str, int]
Records = list[tuple[int, int, bytes, bytes]]  # offset in the stream, type, header, fragment


def keylog(path: Path) -> dict[tuple[str, bytes], bytes]:
    """(label, client random) -> secret, from a key log."""
    out = {}
    for line in path.read_text().splitlines():
        fields = line.split()
        if len(fields) == 3 and not line.startswith("#"):
            out[fields[0], bytes.fromhex(fields[1])] = bytes.fromhex(fields[2])
    return out


def streams(grams: list[pcap.Datagram], keys: Path | None) -> list[pcap.Datagram]:
    """`pcap.streams(grams)`, but each TLS connection's application data in its place,
    decrypted with the key log `keys`: one piece per record, at the capture time of the
    segment that brought the record's first byte."""
    segs = pcap.streams(grams)
    flows: dict[Flow, tuple[bytearray, list[int], list[int]]] = {}  # stream, offsets, times
    for g in segs:
        data, offs, times = flows.setdefault(
            (g.src, g.sport, g.dst, g.dport), (bytearray(), [], [])
        )
        offs.append(len(data))
        times.append(g.t_ns)
        data += g.payload
    clients = [f for f, (data, _, _) in flows.items() if _hello(data)]
    tls = {*clients, *map(_back, clients)}
    out = [g for g in segs if (g.src, g.sport, g.dst, g.dport) not in tls]
    secrets = keylog(keys) if keys and keys.exists() else {}
    for flow in clients:
        back = _back(flow)
        server = bytes(flows[back][0]) if back in flows else b""
        sides = _connection(bytes(flows[flow][0]), server, secrets, flow)
        for f, pieces in zip((flow, back), sides, strict=True):
            for off, plain in pieces:
                _, offs, times = flows[f]
                t = times[bisect.bisect_right(offs, off) - 1]
                out.append(pcap.Datagram(t, *f, plain, True))
    return sorted(out, key=lambda g: g.t_ns)


def _back(flow: Flow) -> Flow:
    return flow[2], flow[3], flow[0], flow[1]


def _hello(data: bytes | bytearray) -> bool:
    """The stream opens with a TLS ClientHello."""
    return len(data) > 5 and data[0] == _HANDSHAKE and data[1] == 3 and data[5] == 1


def _records(data: bytes) -> Records:
    out, pos = [], 0
    while pos + 5 <= len(data):
        length = struct.unpack_from("!H", data, pos + 3)[0]
        if pos + 5 + length > len(data):  # cut short: the capture ended inside it
            break
        out.append((pos, data[pos], data[pos : pos + 5], data[pos + 5 : pos + 5 + length]))
        pos += 5 + length
    return out


def _connection(
    client: bytes, server: bytes, secrets: dict[tuple[str, bytes], bytes], flow: Flow
) -> tuple[list[tuple[int, bytes]], list[tuple[int, bytes]]]:
    """Application data of each side (stream offset of its record, plaintext)."""
    sent, got = _records(client), _records(server)
    if not got:  # no ServerHello: nothing was ever encrypted
        return [], []
    random = sent[0][3][6:38]  # ClientHello: type, length (3), version (2), random
    hello = got[0][3]  # ServerHello: likewise, then the session id and the cipher suite
    suite = struct.unpack_from("!H", hello, 39 + hello[38])[0]
    where = f"TLS {flow[0]}:{flow[1]} -> {flow[2]}:{flow[3]}"
    if ("CLIENT_TRAFFIC_SECRET_0", random) in secrets:
        if suite not in TLS13:
            raise ValueError(f"{where}: TLS 1.3 cipher suite {suite:#06x} not supported")

        def side(name: str, records: Records) -> list[tuple[int, bytes]]:
            hs, app = (
                secrets[f"{name}_{s}", random]
                for s in ("HANDSHAKE_TRAFFIC_SECRET", "TRAFFIC_SECRET_0")
            )
            return _open13(records, suite, hs, app, where)

        return side("CLIENT", sent), side("SERVER", got)
    if (master := secrets.get(("CLIENT_RANDOM", random))) is None:
        raise ValueError(f"{where}: no keys for it in the key log")
    if suite not in TLS12:
        raise ValueError(f"{where}: TLS 1.2 cipher suite {suite:#06x} not supported")
    aead, size, h = TLS12[suite]
    iv = 4 if aead is AESGCM else 12
    block = _prf(h, master, b"key expansion", hello[6:38] + random, 2 * (size + iv))
    keys = block[: 2 * size]
    ivs = block[2 * size :]
    return (
        _open12(sent, aead, keys[:size], ivs[:iv], where),
        _open12(got, aead, keys[size:], ivs[iv:], where),
    )


def _expand(h: str, secret: bytes, label: bytes, length: int) -> bytes:
    """HKDF-Expand-Label (RFC 8446 7.1), with an empty context."""
    full = b"tls13 " + label
    info = struct.pack("!HB", length, len(full)) + full + b"\x00"
    return HKDFExpand(_HASHES[h](), length, info).derive(secret)


def _open13(
    records: Records, suite: int, handshake: bytes, application: bytes, where: str
) -> list[tuple[int, bytes]]:
    """One side's records of a TLS 1.3 connection: handshake keys first, then the application
    keys (whichever opens the record; AEAD tags make the choice unambiguous), following any
    KeyUpdate (RFC 8446 7.2)."""
    aead, size, h = TLS13[suite]

    def keys(secret: bytes) -> tuple[AESGCM | ChaCha20Poly1305, int]:
        return aead(_expand(h, secret, b"key", size)), int.from_bytes(_expand(h, secret, b"iv", 12))

    (cipher, iv), secret, seq, stage = keys(handshake), handshake, 0, 0
    out = []
    for off, kind, head, frag in records:
        if kind != _APPLICATION_DATA:  # hellos and change_cipher_spec, in the clear
            continue
        while True:
            try:
                plain = cipher.decrypt((iv ^ seq).to_bytes(12), frag, head)
                break
            except InvalidTag:
                if stage:
                    raise ValueError(f"{where}: a record does not decrypt") from None
                (cipher, iv), secret, seq, stage = keys(application), application, 0, 1
        seq += 1
        plain = plain.rstrip(b"\x00")  # padding, then the real content type
        inner, plain = plain[-1], plain[:-1]
        if inner == _APPLICATION_DATA:
            out.append((off, plain))
        elif inner == _HANDSHAKE and stage and plain[:1] == bytes([_KEY_UPDATE]):
            secret = _expand(h, secret, b"traffic upd", _HASHES[h]().digest_size)
            (cipher, iv), seq = keys(secret), 0
    return out


def _prf(h: str, secret: bytes, label: bytes, seed: bytes, length: int) -> bytes:
    """The TLS 1.2 PRF (RFC 5246 5)."""
    seed, a, out = label + seed, label + seed, b""
    while len(out) < length:
        a = hmac.digest(secret, a, h)
        out += hmac.digest(secret, a + seed, h)
    return out[:length]


def _open12(
    records: Records, aead: Aead, key: bytes, iv: bytes, where: str
) -> list[tuple[int, bytes]]:
    """One side's records of a TLS 1.2 connection, encrypted from its ChangeCipherSpec on."""
    cipher, seq, on, out = aead(key), 0, False, []
    for off, kind, head, frag in records:
        if kind == _CHANGE_CIPHER_SPEC:
            on = True
            continue
        if not on:
            continue
        if aead is AESGCM:  # RFC 5288: 4 bytes of the key block, 8 sent with each record
            nonce, body = iv + frag[:8], frag[8:]
        else:  # RFC 7905
            nonce, body = (int.from_bytes(iv) ^ seq).to_bytes(12), frag
        aad = struct.pack("!QB", seq, kind) + head[1:3] + struct.pack("!H", len(body) - 16)
        try:
            plain = cipher.decrypt(nonce, body, aad)
        except InvalidTag:
            raise ValueError(f"{where}: a record does not decrypt") from None
        seq += 1
        if kind == _APPLICATION_DATA:
            out.append((off, plain))
    return out


def certificates(directory: Path, names: list[str]) -> None:
    """A test CA (stack-ca.pem) and one certificate it signs for every name (server.crt, with
    the CA, and server.key), valid for two days: the stack's TLS servers present it."""
    directory.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now(datetime.UTC)
    ca_key, key = ec.generate_private_key(ec.SECP256R1()), ec.generate_private_key(ec.SECP256R1())
    ca_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "rtpbench test CA")])
    ski = x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key())

    def cert(subject: x509.Name, public: ec.EllipticCurvePublicKey) -> x509.CertificateBuilder:
        return (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(ca_name)
            .public_key(public)
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - datetime.timedelta(minutes=5))
            .not_valid_after(now + datetime.timedelta(days=2))
            .add_extension(x509.SubjectKeyIdentifier.from_public_key(public), critical=False)
        )

    ca = (
        cert(ca_name, ca_key.public_key())
        .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
        .add_extension(_usage(cert_sign=True), critical=True)
        .sign(ca_key, hashes.SHA256())
    )
    leaf = (
        cert(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, names[0])]), key.public_key())
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(_usage(cert_sign=False), critical=True)
        .add_extension(
            x509.ExtendedKeyUsage(
                [ExtendedKeyUsageOID.SERVER_AUTH, ExtendedKeyUsageOID.CLIENT_AUTH]
            ),
            critical=False,
        )
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName(n) for n in names]), critical=False
        )
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_subject_key_identifier(ski), critical=False
        )
        .sign(ca_key, hashes.SHA256())
    )
    pem = serialization.Encoding.PEM
    (directory / "stack-ca.pem").write_bytes(ca.public_bytes(pem))
    (directory / "server.crt").write_bytes(leaf.public_bytes(pem) + ca.public_bytes(pem))
    (directory / "server.key").write_bytes(
        key.private_bytes(pem, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    )


def _usage(cert_sign: bool) -> x509.KeyUsage:
    return x509.KeyUsage(
        digital_signature=not cert_sign,
        content_commitment=False,
        key_encipherment=False,
        data_encipherment=False,
        key_agreement=False,
        key_cert_sign=cert_sign,
        crl_sign=cert_sign,
        encipher_only=False,
        decipher_only=False,
    )
