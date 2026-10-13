import random
import socket
import struct
import threading
import time
from collections.abc import Iterator
from typing import Any

import pytest

from rtpbench import cases, g711, rtp, sip
from rtpbench.agent import Responder
from rtpbench.caller import Session
from rtpbench.cases import FLOOR_PACKETS, Check, Result, Script, Wire, _floor, check_cancel


@pytest.fixture
def pair() -> Iterator[tuple[socket.socket, socket.socket]]:
    a, b = (socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(2))
    for s in (a, b):
        s.bind(("127.0.0.1", 0))
        s.settimeout(1)
    yield a, b
    a.close()
    b.close()


def got(s: socket.socket) -> sip.Message:
    return sip.parse(s.recvfrom(65535)[0])


def test_dialog_from_both_sides(pair: tuple[socket.socket, socket.socket]) -> None:
    a, b = pair
    uac = sip.Dialog.uac(a, b.getsockname(), "sip:agent@127.0.0.1", "127.0.0.1")
    invite = uac.request("INVITE", b"v=0\r\n")
    uac.send(invite)
    received = got(b)
    assert received.get("cseq") == "1 INVITE"
    uas = sip.Dialog.uas(b, a.getsockname(), received, "127.0.0.1", "t2")
    ok = sip.response(received, 200, "OK", "t2", extra=[("Contact", uas.contact)])
    uac.answered(ok)
    assert not uac.pending
    uac.confirm(ok)
    ack = got(b)
    assert (ack.method, ack.get("cseq"), ack.first.split()[1]) == ("ACK", "1 ACK", uri(uas))
    bye = uas.request("BYE")
    assert bye.get("from") == ok.get("to")
    assert sip.tag(bye.get("from")) == "t2"
    assert bye.get("to") == invite.get("from")
    assert bye.first == f"BYE {uri(uac)} SIP/2.0"


def test_failure_ack_keeps_the_invite_branch(pair: tuple[socket.socket, socket.socket]) -> None:
    a, b = pair
    uac = sip.Dialog.uac(a, b.getsockname(), "sip:agent@127.0.0.1", "127.0.0.1")
    invite = uac.request("INVITE", b"v=0\r\n")
    uac.send(invite)
    busy = sip.response(got(b), 486, "Busy Here", "t2")
    uac.answered(busy)
    uac.ack_failure(invite, busy)
    ack = got(b)
    assert ack.branch == invite.branch
    assert ack.get("cseq") == "1 ACK"
    assert sip.tag(ack.get("to")) == "t2"
    assert not uac.pending


def test_requests_retransmit_until_answered(pair: tuple[socket.socket, socket.socket]) -> None:
    a, b = pair
    uac = sip.Dialog.uac(a, b.getsockname(), "sip:agent@127.0.0.1", "127.0.0.1")
    bye = uac.request("BYE")
    uac.send(bye)
    assert uac.recv(sip.T1 * 1.5) is None  # one retransmission due meanwhile
    assert [got(b).branch for _ in range(2)] == [bye.branch] * 2
    uac.answered(sip.response(bye, 200, "OK"))
    assert not uac.pending


def uri(d: sip.Dialog) -> str:
    return sip.uri_of(d.contact)


def test_answer_without_g711_hangs_up(pair: tuple[socket.socket, socket.socket]) -> None:
    _, b = pair
    seen: list[str] = []

    def uas() -> None:  # answers G.722 only, then takes the BYE
        while True:
            data, addr = b.recvfrom(65535)
            msg = sip.parse(data)
            seen.append(msg.method)
            if msg.method == "INVITE":
                body = b"v=0\r\nc=IN IP4 127.0.0.1\r\nm=audio 4000 RTP/AVP 9\r\n"
                contact = [("Contact", "<sip:agent@127.0.0.1>")]
                b.sendto(sip.response(msg, 200, "OK", "t2", body, contact).render(), addr)
            elif msg.method == "BYE":
                b.sendto(sip.response(msg, 200, "OK").render(), addr)
                return

    s = Session(f"sip:agent@127.0.0.1:{b.getsockname()[1]}", (g711.PCMU,))
    t = threading.Thread(target=uas)
    t.start()
    with pytest.raises(sip.SipError, match=r"no G\.711 format \(payload types 9\)"):
        s.answer(timeout=2)
    t.join()
    assert seen == ["INVITE", "ACK", "BYE"]


def test_verdict() -> None:
    assert Result([Check("a", True), Check("b", None)]).verdict == "inconclusive"
    assert Result([Check("a", False), Check("b", None)]).verdict == "fail"
    assert Result([Check("a", True)]).verdict == "pass"


def msg(first: str, cseq: str) -> sip.Message:
    return sip.Message(first, [("CSeq", cseq)])


@pytest.mark.parametrize(
    ("answered_at", "verdict"), [(5, "inconclusive"), (3000, "fail"), (None, "pass")]
)
def test_cancel_race_is_not_a_failure(answered_at: int | None, verdict: str) -> None:
    final = msg("SIP/2.0 200 OK", "1 INVITE") if answered_at else msg("SIP/2.0 487 X", "1 INVITE")
    msgs = [
        (0, True, msg("CANCEL sip:a SIP/2.0", "1 CANCEL")),
        (answered_at or 2, False, final),
        (10, False, msg("SIP/2.0 200 OK", "1 CANCEL")),
    ]
    w = Wire({}, None, sorted(msgs, key=lambda m: m[0]), [], [])
    assert check_cancel(w).verdict == verdict


def test_sender_pause_keeps_seq_and_clock(pair: tuple[socket.socket, socket.socket]) -> None:
    a, b = pair
    paused = range(3, 7)
    send = rtp.Sender(
        a, b.getsockname(), 8, lambda n, _t: None if n in paused else bytes(160), 0, 65534, 9
    )
    send.start_ns = time.time_ns()
    send.start()
    got = [rtp.parse(b.recvfrom(2048)[0]) for _ in range(6)]
    send.stop.set()
    send.join()
    assert [(p.seq, p.ts, p.marker) for p in got if p] == [
        (65534, 0, True),
        (65535, 160, False),
        (0, 320, False),
        (1, 7 * 160, True),  # next seq, timestamp kept time, marker after the pause
        (2, 8 * 160, False),
        (3, 9 * 160, False),
    ]


@pytest.mark.parametrize("clock", [True, False])
def test_agent_on_hold_sends_nothing(clock: bool) -> None:
    r = Responder(8, seq0=0, delays=[])
    r.clock = clock
    out = []
    for n in range(10):
        r.sending = not 3 <= n < 7
        out.append(r.source(n, n * rtp.PTIME_NS))
    assert [o is None for o in out] == [False] * 3 + [True] * 4 + [False] * 3
    if clock:  # the sender stamps it n * 160
        assert isinstance(out[7], bytes)
    else:  # timestamps resume where they stopped
        assert out[7] == rtp.Frame(8, r.silence, 3 * rtp.FRAME, True)


def test_rfc4733_digit_frames() -> None:
    m = Script(8, events=101)
    m.press("#")
    out = [m.source(n, 0) for n in range(3, 12)]
    events = [o for o in out if isinstance(o, rtp.Frame)]
    assert [(f.ts, f.marker) for f in events] == [(3 * 160, True)] + [(3 * 160, False)] * 6
    fields = [struct.unpack("!BBH", f.payload) for f in events]
    # event 11, volume 10; duration grows to 100 ms; the end packet three times
    assert fields == [(11, 10, d) for d in (160, 320, 480, 640)] + [(11, 0x8A, 800)] * 3
    assert out[7:] == [m.silence] * 2
    assert not m.busy()


@pytest.mark.parametrize(("clock", "want"), [(True, 0.0), (False, -3000.0)])
def test_clock_drift_across_a_pause_is_past_jitter(clock: bool, want: float) -> None:
    """3 s pause, 20 ms jitter (sd) on every packet: one packet each side is often 40 ms off,
    the transit floor over 25 packets is not."""
    rng = random.Random(1)

    def stream(n0: int, ts0: int) -> list[tuple[int, rtp.Packet]]:
        out = []
        for i in range(FLOOR_PACKETS):
            sent = (n0 + i) * 20_000_000
            ts = (ts0 + i * 160) & 0xFFFFFFFF
            out.append(
                (
                    sent + round(max(0.0, rng.gauss(60, 20)) * 1e6),
                    rtp.Packet(0, i, ts, 1, False, b""),
                )
            )
        return out

    ts0 = 0xFFFFFF00  # wraps across the pause
    before = stream(0, ts0)
    resumed = FLOOR_PACKETS + 150  # 3 s later
    after = stream(resumed, ts0 + (resumed if clock else FLOOR_PACKETS) * 160)
    drift = _floor(before, ts0) - _floor(after, ts0)
    assert abs(drift - want) < 15


def test_hold_resume_seq_by_sequence_not_arrival() -> None:
    """Packets reordered at both edges of the hold: still the next seq, nothing lost."""

    def sip_msg(first: str, branch: str, direction: str = "") -> sip.Message:
        cseq = "1 INVITE"
        body = sip.sdp("10.0.0.2", 4000, [0], direction) if direction else b""
        return sip.Message(first, [("Via", f"SIP/2.0/UDP x;branch={branch}"), ("CSeq", cseq)], body)

    s = 1_000_000_000
    msgs = [
        (0, True, sip_msg("INVITE sip:a SIP/2.0", "b0", "sendrecv")),
        (s, True, sip_msg("INVITE sip:a SIP/2.0", "b1", "sendonly")),
        (s + 10**7, False, sip_msg("SIP/2.0 200 OK", "b1", "recvonly")),
        (4 * s, True, sip_msg("INVITE sip:a SIP/2.0", "b2", "sendrecv")),
        (4 * s + 10**7, False, sip_msg("SIP/2.0 200 OK", "b2", "sendrecv")),
    ]

    def pkt(seq: int, at: int) -> tuple[int, rtp.Packet]:
        return at * 20_000_000 + 60_000_000, rtp.Packet(0, seq, at * 160, 7, False, b"")

    held = [pkt(n, n) for n in range(48)] + [pkt(n, n + 160) for n in range(48, 100)]
    for i in (46, 48):  # 47 arrives before 46, 49 before 48
        held[i], held[i + 1] = (held[i][0], held[i + 1][1]), (held[i + 1][0], held[i][1])
    w = Wire({"pt": 0}, None, msgs, [], held)
    same = next(c for c in cases.check_hold(w).checks if c.name.endswith("same RTP stream"))
    assert same.ok, same.detail
    assert "seq 47->48" in same.detail


def test_repeats_group_and_flips_are_reported() -> None:
    bar = list(cases.WIRE)

    def rec(repeat: int, verdict: str, ms: float, behaviour: str | None = "good") -> dict[str, Any]:
        ok = verdict == "pass"
        return {
            "profile": "lte",
            "repeat": repeat,
            "case": "greeting",
            "behaviour": behaviour,
            "run": f"lte/{repeat:02d}/greeting-good",
            "verdict": verdict,
            "checks": [{"name": "agent speaks within 2000 ms", "ok": ok, "detail": ""}],
            "timings": [{"name": "200 OK to agent speech", "ms": ms, "bar": bar, "truth_ms": None}],
        }

    steady = [rec(k, "pass", 1000.0 + k) for k in (1, 2, 3)]
    assert cases.verdicts(steady) == "pass 3/3"
    assert cases.timings(steady) == [
        ("200 OK to agent speech", "1002.0 [1001.0, 1003.0] ms (-0.4/+0.4) n=3")
    ]
    assert cases.proven(steady)
    flips = [*steady, rec(4, "fail", 2500.0)]
    assert cases.verdicts(flips) == "flips: pass 3, fail 1"
    assert cases.failures(flips) == ["agent speaks within 2000 ms (1/4)"]
    assert not cases.proven(flips)
    assert list(cases.groups(flips)) == [("lte", "greeting", "good")]
    assert cases.proven([rec(1, "fail", 2500.0, None)])  # a real target proves nothing
