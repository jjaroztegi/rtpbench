import socket
from collections.abc import Iterator

import pytest

from rtpbench import sip
from rtpbench.cases import Check, Result, Wire, check_cancel


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
