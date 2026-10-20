import contextlib
import ssl
import struct
import threading
from pathlib import Path

import pytest

from rtpbench import pcap, sip, tls

INVITE = sip.Message("INVITE sips:agent@agent SIP/2.0", [("Call-ID", "x")], b"v=0\r\n" * 300)
TRYING = sip.Message("SIP/2.0 100 Trying", [("Call-ID", "x")])
OK = sip.Message("SIP/2.0 200 OK", [("Call-ID", "x")], b"v=0\r\n")


def _session(tmp: Path, version: ssl.TLSVersion, ciphers: str | None) -> list[tuple[bool, bytes]]:
    """A TLS session between in-memory endpoints as the caller and the agent set it up: the INVITE,
    then the agent's 100 and 200 in one write. The bytes each side sent, in order (True: client)."""
    tls.certificates(tmp / "tls", ["agent"])
    server = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    server.load_cert_chain(tmp / "tls" / "server.crt", tmp / "tls" / "server.key")
    client = ssl.create_default_context(cafile=tmp / "tls" / "stack-ca.pem")
    client.keylog_filename = str(tmp / "keys.log")
    client.minimum_version = client.maximum_version = version
    client.set_ciphers(ciphers or tls.CIPHERS_12)
    bios = [ssl.MemoryBIO() for _ in range(4)]
    c = client.wrap_bio(bios[0], bios[1], server_hostname="agent")
    s = server.wrap_bio(bios[2], bios[3], server_side=True)
    wire: list[tuple[bool, bytes]] = []

    def move() -> None:
        for out, into, from_client in ((bios[1], bios[2], True), (bios[3], bios[0], False)):
            if data := out.read():
                wire.append((from_client, data))
                into.write(data)

    for _ in range(4):
        for end in (c, s):
            with contextlib.suppress(ssl.SSLWantReadError):
                end.do_handshake()
        move()
    c.write(INVITE.render())
    move()
    assert s.read(65535) == INVITE.render()
    s.write(TRYING.render() + OK.render())
    move()
    return wire


def _pcap(path: Path, wire: list[tuple[bool, bytes]]) -> list[int]:
    """The session as TCP segments of at most 500 bytes, 1 us apart; each segment's time."""
    a, b = ((10, 0, 0, 1), 40000), ((10, 0, 0, 2), 5061)
    data = struct.pack("<IHHiIII", 0xA1B23C4D, 2, 4, 0, 0, 65535, 101)
    seqs, times = {True: 1, False: 7}, list[int]()
    for from_client, chunk in wire:
        (src, sport), (dst, dport) = (a, b) if from_client else (b, a)
        for i in range(0, len(chunk), 500):
            seg, t = chunk[i : i + 500], 1000 * (len(times) + 1)
            tcp = struct.pack("!HHIIBBHHH", sport, dport, seqs[from_client], 0, 80, 24, 9, 0, 0)
            ip = struct.pack(
                "!BBHHHBBH4s4s", 69, 0, 40 + len(seg), 0, 0, 64, 6, 0, bytes(src), bytes(dst)
            )
            data += (
                struct.pack("<IIII", *divmod(t, 10**9), 40 + len(seg), 40 + len(seg))
                + ip
                + tcp
                + seg
            )
            seqs[from_client] += len(seg)
            times.append(t)
    path.write_bytes(data)
    return times


@pytest.mark.parametrize(
    ("version", "ciphers"),
    [
        (ssl.TLSVersion.TLSv1_3, None),
        (ssl.TLSVersion.TLSv1_2, "ECDHE+AESGCM"),
        (ssl.TLSVersion.TLSv1_2, "ECDHE+CHACHA20"),
    ],
)
def test_sip_read_back_from_a_tls_capture(
    tmp_path: Path, version: ssl.TLSVersion, ciphers: str | None
) -> None:
    """Each message in full at the time of the segment carrying its record's first byte, the
    100 and the 200 apart though one record carried both; nothing of the handshake."""
    _pcap(tmp_path / "x.pcap", _session(tmp_path, version, ciphers))
    grams = pcap.read(tmp_path / "x.pcap")
    got = sip.captured(grams, tmp_path / "keys.log")
    assert [(src, data) for _, src, data in got] == [
        ("10.0.0.1", INVITE.render()),
        ("10.0.0.2", TRYING.render()),
        ("10.0.0.2", OK.render()),
    ]
    invite_t, trying_t, ok_t = (t for t, _, _ in got)
    records = [g for g in pcap.streams(grams) if g.payload[:1] == b"\x17"]
    assert invite_t == next(g.t_ns for g in records if g.src == "10.0.0.1")
    assert trying_t == ok_t > invite_t
    (tmp_path / "keys.log").write_text("")
    with pytest.raises(ValueError, match="no keys"):
        sip.captured(grams, tmp_path / "keys.log")


def test_rfc8448_client_application_data() -> None:
    """RFC 8448 3: the client's application data record, TLS_AES_128_GCM_SHA256."""
    secret = bytes.fromhex("9e40646ce79a7f9dc05af8889bce6552875afa0b06df0087f792ebb7c17504a5")
    record = bytes.fromhex(
        "17030300 43a23f70 54b62c94 d0affafe 8228ba55 cbefacea 42f914aa 66bcab3f 2b9819a8"
        " a5b46b39 5bd54a9a 20441e2b 62974e1f 5a6292a2 977014bd 1e3deae6 3aeebb21 694915e4"
    )
    got = tls._open13([(0, 23, record[:5], record[5:])], 0x1301, b"\0" * 32, secret, "rfc")
    assert got == [(0, bytes(range(50)))]


def test_tls_transport_checks_the_name_and_answers_on_the_connection(tmp_path: Path) -> None:
    tls.certificates(tmp_path, ["agent"])
    server_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    server_ctx.load_cert_chain(tmp_path / "server.crt", tmp_path / "server.key")
    trusted = ssl.create_default_context(cafile=tmp_path / "stack-ca.pem")
    server = sip.Tls(server=server_ctx)
    server.settimeout(5)
    addr = ("127.0.0.1", server.getsockname()[1])
    got: list[tuple[bytes, tuple[str, int]]] = []
    accepting = threading.Thread(target=lambda: got.append(server.recvfrom()))
    accepting.start()  # the handshake needs the far end at once
    wrong = sip.Tls(client=trusted, hostname="carrier")
    with pytest.raises(ssl.SSLCertVerificationError):
        wrong.sendto(INVITE.render(), addr)
    client = sip.Tls(client=trusted, hostname="agent")
    client.settimeout(2)
    client.sendto(INVITE.render(), addr)
    accepting.join()
    assert client.negotiated()["version"] == "TLSv1.3"  # kept once the connection closes
    ((data, peer),) = got
    assert data == INVITE.render()
    server.sendto(TRYING.render() + OK.render(), peer)  # one record, two messages
    assert [client.recvfrom()[0] for _ in range(2)] == [TRYING.render(), OK.render()]
    assert client.negotiated()["version"] == "TLSv1.3"
    for t in (server, client, wrong):
        t.close()


def test_tls_uris_and_contacts() -> None:
    from rtpbench.caller import parse_uri

    assert sip.secure("sips:agent@host")
    assert sip.secure("sip:a@h:5070;transport=TLS")
    assert not sip.secure("sip:agent@host;transport=tcp")
    assert parse_uri("sips:agent@host") == ("host", 5061)
    assert parse_uri("sip:proj@sip.example.com;transport=tls") == ("sip.example.com", 5061)
    assert parse_uri("sip:agent@host") == ("host", 5060)
    assert (
        sip.contact("rtpbench", "10.0.0.1", 4000, "TLS", sips=True)
        == "<sips:rtpbench@10.0.0.1:4000>"
    )
    assert (
        sip.contact("rtpbench", "10.0.0.1", 4000, "TLS")
        == "<sip:rtpbench@10.0.0.1:4000;transport=tls>"
    )
    assert sip.contact("rtpbench", "10.0.0.1", 4000, "UDP") == "<sip:rtpbench@10.0.0.1:4000>"


def test_a_refused_handshake_reads_as_no_messages(tmp_path: Path) -> None:
    """The server answers the ClientHello with an alert: nothing to decrypt, no error."""
    hello = _session(tmp_path, ssl.TLSVersion.TLSv1_3, None)[0]
    alert = (False, b"\x15\x03\x03\x00\x02\x02\x28")  # fatal handshake_failure
    _pcap(tmp_path / "x.pcap", [hello, alert])
    assert sip.captured(pcap.read(tmp_path / "x.pcap"), tmp_path / "keys.log") == []
