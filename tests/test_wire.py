import struct
from pathlib import Path

import pytest

from rtpbench import g711, pcap, rtp, sip


@pytest.mark.parametrize("pt", [g711.PCMU, g711.PCMA])
def test_g711_round_trip(pt: int) -> None:
    assert g711.encode(pt, [0]) == bytes([g711.SILENCE[pt]])
    for x in range(-32768, 32768, 7):
        y = g711.decode(pt, g711.encode(pt, [x]))[0]
        assert abs(y - x) <= max(16, abs(x) // 15), (x, y)


def test_rtp_round_trip_skips_csrc_and_extension() -> None:
    raw = rtp.pack(8, 65535, 2**32 - 1, 7, b"abc", marker=True)
    assert rtp.parse(raw) == rtp.Packet(8, 65535, 2**32 - 1, 7, True, b"abc")
    ext = bytes([0x91]) + raw[1:12] + b"CSRC" + b"\xbe\xde\x00\x01" + b"XXXX" + b"abc"
    assert rtp.parse(ext) == rtp.Packet(8, 65535, 2**32 - 1, 7, True, b"abc")
    assert rtp.parse(bytes([0x90]) + raw[1:12] + b"\xbe\xde") is None  # extension cut short


def test_sip_parse_render_and_response() -> None:
    raw = (
        b"INVITE sip:agent@10.0.0.2 SIP/2.0\r\nv: SIP/2.0/UDP 10.0.0.1:5060;branch=z9hG4bKx\r\n"
        b"f: <sip:a@10.0.0.1>;tag=1\r\nt: <sip:agent@10.0.0.2>\r\ni: abc\r\nCSeq: 1 INVITE\r\n"
        b"l: 4\r\n\r\nbody"
    )
    msg = sip.parse(raw)
    assert (msg.method, msg.get("call-id"), msg.get("Via"), msg.body) == (
        "INVITE",
        "abc",
        "SIP/2.0/UDP 10.0.0.1:5060;branch=z9hG4bKx",
        b"body",
    )
    ok = sip.parse(sip.response(msg, 200, "OK", "t2", b"sdp").render())
    assert ok.status == 200
    assert sip.tag(ok.get("to")) == "t2"
    assert ok.get("content-length") == "3"
    assert ok.cseq_method == "INVITE"
    assert ok.get("via") == msg.get("via")


def test_sdp_round_trip() -> None:
    got = sip.parse_sdp(sip.sdp("10.1.2.3", 4000, [0, 8], "sendonly", (7, 3)))
    assert got == sip.Sdp("10.1.2.3", 4000, [0, 8], "sendonly")


def test_sdp_skips_a_section_before_the_audio() -> None:
    body = (
        b"v=0\r\no=- 1 1 IN IP4 10.1.2.3\r\ns=-\r\nt=0 0\r\n"
        b"m=video 0 RTP/AVP 96\r\nc=IN IP4 10.9.9.9\r\na=inactive\r\n"
        b"m=audio 4000 RTP/AVP 8\r\nc=IN IP4 10.1.2.3\r\n"
    )
    assert sip.parse_sdp(body) == sip.Sdp("10.1.2.3", 4000, [8], "sendrecv")


def test_pcap_reads_nanosecond_ethernet_udp(tmp_path: Path) -> None:
    payload = b"hello"
    udp = struct.pack("!HHHH", 5004, 6000, 8 + len(payload), 0) + payload
    ip = struct.pack(
        "!BBHHHBBH4s4s",
        0x45,
        0,
        20 + len(udp),
        0,
        0x4000,
        64,
        17,
        0,
        bytes([10, 0, 0, 1]),
        bytes([10, 0, 0, 2]),
    )
    frame = b"\x00" * 12 + b"\x08\x00" + ip + udp
    data = struct.pack("<IHHiIII", 0xA1B23C4D, 2, 4, 0, 0, 65535, 1)
    data += struct.pack("<IIII", 1_700_000_000, 123_456_789, len(frame), len(frame)) + frame
    cut = frame[:-2]  # snaplen: the datagram is not all there
    data += struct.pack("<IIII", 1_700_000_001, 0, len(cut), len(frame)) + cut
    (tmp_path / "x.pcap").write_bytes(data)
    (d,) = pcap.read(tmp_path / "x.pcap")
    assert d == pcap.Datagram(
        1_700_000_000_123_456_789, "10.0.0.1", 5004, "10.0.0.2", 6000, payload
    )
