"""Minimal SIP over UDP or TCP: one audio call as UAC or UAS (RFC 3261 subset).

Messages stay plain header lists, so a caller can add, drop or reorder anything before sending.
"""

import hashlib
import re
import secrets
import select
import socket
import time
from dataclasses import dataclass, field

from rtpbench.g711 import NAMES

T1, T2 = 0.5, 4.0
_COMPACT = {
    "i": "call-id",
    "f": "from",
    "t": "to",
    "v": "via",
    "m": "contact",
    "l": "content-length",
    "c": "content-type",
}


@dataclass
class Message:
    first: str
    headers: list[tuple[str, str]] = field(default_factory=list)
    body: bytes = b""

    def get(self, name: str) -> str:
        name = name.lower()
        for key, value in self.headers:
            if _COMPACT.get(key.lower(), key.lower()) == name:
                return value
        return ""

    def all(self, name: str) -> list[str]:
        name = name.lower()
        return [v for k, v in self.headers if _COMPACT.get(k.lower(), k.lower()) == name]

    @property
    def status(self) -> int:
        return int(self.first.split()[1]) if self.first.startswith("SIP/2.0") else 0

    @property
    def method(self) -> str:
        return "" if self.status else self.first.split()[0]

    @property
    def cseq_method(self) -> str:
        return self.get("cseq").split()[-1]

    @property
    def branch(self) -> str:
        return param(self.get("via"), "branch")

    def render(self) -> bytes:
        lines = [self.first, *(f"{k}: {v}" for k, v in self.headers if k != "Content-Length")]
        lines.append(f"Content-Length: {len(self.body)}")
        return ("\r\n".join(lines) + "\r\n\r\n").encode() + self.body


def parse(data: bytes) -> Message:
    head, _, body = data.partition(b"\r\n\r\n")
    first, *lines = head.decode(errors="replace").split("\r\n")
    headers: list[tuple[str, str]] = []
    for line in lines:
        if line[:1] in (" ", "\t") and headers:  # folded continuation
            headers[-1] = (headers[-1][0], headers[-1][1] + " " + line.strip())
        elif ":" in line:
            key, value = line.split(":", 1)
            headers.append((key.strip(), value.strip()))
    return Message(first, headers, body)


def param(value: str, name: str) -> str:
    """A header parameter (`tag`, `branch`, `refresher`...) outside the <URI>."""
    for p in value.rsplit(">", 1)[-1].split(";")[1:]:
        key, _, v = p.partition("=")
        if key.strip().lower() == name:
            return v.strip()
    return ""


def tag(value: str) -> str:
    return param(value, "tag")


def uri_of(value: str) -> str:
    return value.split("<", 1)[1].split(">", 1)[0] if "<" in value else value.split(";")[0]


def response(
    req: Message,
    status: int,
    reason: str,
    to_tag: str = "",
    body: bytes = b"",
    extra: list[tuple[str, str]] | None = None,
) -> Message:
    to = req.get("to")
    if to_tag and not tag(to):
        to += f";tag={to_tag}"
    headers = [("Via", v) for v in req.all("via")]
    headers += [("Record-Route", v) for v in req.all("record-route")]
    headers += [
        ("From", req.get("from")),
        ("To", to),
        ("Call-ID", req.get("call-id")),
        ("CSeq", req.get("cseq")),
    ]
    headers += extra or []
    if body:
        headers.append(("Content-Type", "application/sdp"))
    return Message(f"SIP/2.0 {status} {reason}", headers, body)


def sdp(
    ip: str,
    port: int,
    pts: list[int],
    direction: str = "sendrecv",
    origin: tuple[int, int] | None = None,
    dtmf: bool = False,
    conn: str | None = None,
) -> bytes:
    """An audio offer or answer; `origin` (session id, version) for a later one; `dtmf` adds
    RFC 4733 telephone-event; `conn` another connection address (0.0.0.0: RFC 2543 hold);
    `direction` "" leaves the attribute out."""
    sid, version = origin or (secrets.randbelow(1 << 31),) * 2
    events = [TELEPHONE_EVENT] if dtmf else []
    lines = [
        "v=0",
        f"o=rtpbench {sid} {version} IN IP4 {ip}",
        "s=rtpbench",
        f"c=IN IP4 {conn or ip}",
        "t=0 0",
        f"m=audio {port} RTP/AVP {' '.join(map(str, [*pts, *events]))}",
        *(f"a=rtpmap:{pt} {NAMES[pt]}/8000" for pt in pts),
        *(f"a=rtpmap:{pt} telephone-event/8000" for pt in events),
        *(f"a=fmtp:{pt} 0-16" for pt in events),
        "a=ptime:20",
        *([f"a={direction}"] if direction else []),
    ]
    return ("\r\n".join(lines) + "\r\n").encode()


@dataclass
class Sdp:
    ip: str = ""
    port: int = 0
    pts: list[int] = field(default_factory=list)
    direction: str = "sendrecv"
    dtmf: int | None = None  # telephone-event payload type


TELEPHONE_EVENT = 101
DIRECTIONS = ("sendrecv", "sendonly", "recvonly", "inactive")
# what an answerer that honours the offer replies with (RFC 3264 6.1)
ANSWER = {
    "sendrecv": "sendrecv",
    "sendonly": "recvonly",
    "recvonly": "sendonly",
    "inactive": "inactive",
}


def parse_sdp(body: bytes) -> Sdp:
    """Connection address, port, payload types and direction of the first audio stream."""
    out, media, other = Sdp(), False, False
    for line in body.decode(errors="replace").splitlines():
        if line.startswith("m="):
            if media:
                break
            if media := line.startswith("m=audio "):
                fields = line.split()
                out.port, out.pts = int(fields[1]), [int(p) for p in fields[3:]]
            other = not media
        elif other:  # a section before the audio one (video, say): not ours
            continue
        elif line.startswith("c=IN IP4 ") and (media or not out.ip):
            out.ip = line.split()[2]
        elif line[2:] in DIRECTIONS:  # media level comes later, so it wins
            out.direction = line[2:]
        elif line.lower().startswith("a=rtpmap:") and "telephone-event/8000" in line.lower():
            out.dtmf = int(line[9:].split()[0])
    return out


class SipError(Exception):
    pass


_PARAM = re.compile(r'([\w-]+)\s*=\s*("([^"]*)"|[^,\s]*)')
_HASH = {"MD5": hashlib.md5, "SHA-256": hashlib.sha256}  # strongest last


def digest(
    challenges: list[str],
    method: str,
    uri: str,
    user: str,
    password: str,
    cnonce: str | None = None,
) -> str:
    """An Authorization or Proxy-Authorization value answering the strongest of `challenges`
    (WWW- or Proxy-Authenticate values) this supports: digest (RFC 7616) with MD5 or SHA-256
    (RFC 8760), plain or -sess, qop auth or none."""
    offers = []
    for value in challenges:
        scheme, _, rest = value.strip().partition(" ")
        if scheme.lower() != "digest":
            continue
        p = {m[1].lower(): m[3] if m[3] is not None else m[2] for m in _PARAM.finditer(rest)}
        algorithm = p.get("algorithm", "MD5").upper()
        qops = [q.strip() for q in p.get("qop", "").split(",") if q.strip()]
        if algorithm.removesuffix("-SESS") in _HASH and (not qops or "auth" in qops):
            offers.append((list(_HASH).index(algorithm.removesuffix("-SESS")), algorithm, p))
    if not offers:
        raise SipError(f"no digest challenge this caller supports: {'; '.join(challenges)}")
    _, algorithm, p = max(offers, key=lambda o: o[0])
    h = _HASH[algorithm.removesuffix("-SESS")]

    def hex_(text: str) -> str:
        return h(text.encode()).hexdigest()

    cnonce = cnonce or secrets.token_hex(8)
    realm, nonce = p.get("realm", ""), p.get("nonce", "")
    ha1 = hex_(f"{user}:{realm}:{password}")
    if algorithm.endswith("-SESS"):
        ha1 = hex_(f"{ha1}:{nonce}:{cnonce}")
    ha2 = hex_(f"{method}:{uri}")
    fields = [
        f'username="{user}"',
        f'realm="{realm}"',
        f'nonce="{nonce}"',
        f'uri="{uri}"',
        f"algorithm={algorithm}",
    ]
    if "qop" in p:  # one request per nonce here, so nc is always 1
        response = hex_(f"{ha1}:{nonce}:00000001:{cnonce}:auth:{ha2}")
        fields += [f'cnonce="{cnonce}"', "qop=auth", "nc=00000001"]
    else:
        response = hex_(f"{ha1}:{nonce}:{ha2}")
    fields.insert(4, f'response="{response}"')
    if "opaque" in p:
        fields.append(f'opaque="{p["opaque"]}"')
    return "Digest " + ", ".join(fields)


class Tcp:
    """SIP over TCP behind a UDP socket's interface (`sendto`, `recvfrom`, `settimeout`,
    `getsockname`), so a dialog runs on either. Listens on `port`; `sendto` uses the connection
    to or from that address, or opens one; messages are framed by Content-Length (RFC 3261
    18.3). The peer of an accepted connection is its address, so answers go back on it."""

    transport = "TCP"

    def __init__(self, port: int = 0) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("0.0.0.0", port))
        self.server.listen(16)
        self.conns: dict[tuple[str, int], socket.socket] = {}
        self.buf: dict[tuple[str, int], bytes] = {}
        self.timeout: float | None = None

    def getsockname(self) -> tuple[str, int]:
        name: tuple[str, int] = self.server.getsockname()
        return name

    def settimeout(self, timeout: float | None) -> None:
        self.timeout = timeout

    def sockets(self) -> list[socket.socket]:
        return [self.server, *self.conns.values()]

    def sendto(self, data: bytes, addr: tuple[str, int]) -> None:
        """Send on the connection with `addr`; ConnectionRefusedError if none can be opened."""
        if addr not in self.conns:
            conn = socket.create_connection(addr, timeout=5)
            conn.settimeout(None)
            self.conns[addr], self.buf[addr] = conn, b""
        self.conns[addr].sendall(data)

    def _message(self) -> tuple[bytes, tuple[str, int]] | None:
        """A complete message already read, if any."""
        for addr, buf in self.buf.items():
            head, sep, rest = buf.lstrip(b"\r\n").partition(b"\r\n\r\n")
            if not sep:
                continue
            length = int(parse(head + sep).get("content-length") or 0)
            if len(rest) >= length:
                self.buf[addr] = rest[length:]
                return head + sep + rest[:length], addr
        return None

    def recvfrom(self, _bufsize: int = 0) -> tuple[bytes, tuple[str, int]]:
        """The next message and who sent it; TimeoutError after the timeout."""
        deadline = None if self.timeout is None else time.monotonic() + self.timeout
        while (got := self._message()) is None:
            left = None if deadline is None else max(0.0, deadline - time.monotonic())
            ready, _, _ = select.select(self.sockets(), [], [], left)
            if not ready:
                raise TimeoutError
            for s in ready:
                if s is self.server:
                    conn, addr = s.accept()
                    self.conns[addr], self.buf[addr] = conn, b""
                    continue
                addr = next(a for a, c in self.conns.items() if c is s)
                data = s.recv(65535)
                if data:
                    self.buf[addr] += data
                else:  # closed by the peer
                    s.close()
                    del self.conns[addr]
        return got

    def close(self) -> None:
        for s in self.sockets():
            s.close()


@dataclass
class _Tx:
    msg: Message
    due: float  # next retransmission
    interval: float
    end: float  # give up (timer B/F)


class Dialog:
    """One call's dialog from either side: builds in-dialog requests and retransmits them over
    UDP (timer A for INVITE until a provisional, timer E otherwise) until a final response."""

    def __init__(
        self,
        sock: socket.socket | Tcp,
        peer: tuple[str, int],
        local_ip: str,
        local: str,
        remote: str,
        call_id: str,
        target: str,
        user: str = "rtpbench",
    ) -> None:
        self.sock, self.peer, self.local_ip = sock, peer, local_ip
        self.local, self.remote, self.call_id, self.target = local, remote, call_id, target
        self.transport: str = getattr(sock, "transport", "UDP")
        param = ";transport=tcp" if self.transport == "TCP" else ""
        self.contact = f"<sip:{user}@{local_ip}:{sock.getsockname()[1]}{param}>"
        self.cseq = 0
        self.routes: list[str] = []
        self.pending: dict[tuple[str, str], _Tx] = {}  # (branch, method)

    @classmethod
    def uac(
        cls, sock: socket.socket | Tcp, peer: tuple[str, int], uri: str, local_ip: str
    ) -> Dialog:
        local = f"<sip:rtpbench@{local_ip}>;tag={secrets.token_hex(4)}"
        call_id = f"{secrets.token_hex(8)}@{local_ip}"
        return cls(sock, peer, local_ip, local, f"<{uri}>", call_id, uri)

    @classmethod
    def uas(
        cls,
        sock: socket.socket | Tcp,
        peer: tuple[str, int],
        invite: Message,
        local_ip: str,
        to_tag: str,
    ) -> Dialog:
        d = cls(
            sock,
            peer,
            local_ip,
            f"{invite.get('to')};tag={to_tag}",
            invite.get("from"),
            invite.get("call-id"),
            uri_of(invite.get("contact")),
            "agent",
        )
        d.routes = invite.all("record-route")
        return d

    def request(
        self,
        method: str,
        body: bytes = b"",
        headers: list[tuple[str, str]] | None = None,
        content_type: str = "application/sdp",
    ) -> Message:
        """A new in-dialog request with its own CSeq and branch, not yet sent."""
        if method != "ACK":
            self.cseq += 1
        port = self.sock.getsockname()[1]
        branch = "z9hG4bK" + secrets.token_hex(6)
        hdrs = [("Via", f"SIP/2.0/{self.transport} {self.local_ip}:{port};branch={branch};rport")]
        hdrs += [("Route", r) for r in self.routes]
        hdrs += [
            ("Max-Forwards", "70"),
            ("From", self.local),
            ("To", self.remote),
            ("Call-ID", self.call_id),
            ("CSeq", f"{self.cseq} {method}"),
            ("Contact", self.contact),
            ("User-Agent", "rtpbench"),
            *(headers or []),
        ]
        if body:
            hdrs.append(("Content-Type", content_type))
        return Message(f"{method} {self.target} SIP/2.0", hdrs, body)

    def send(self, msg: Message) -> None:
        """Send; a request other than ACK is retransmitted until its final response (over UDP;
        TCP is reliable, RFC 3261 17.1.1.2)."""
        self.sock.sendto(msg.render(), self.peer)
        if msg.method and msg.method != "ACK":
            now = time.monotonic()
            first = now + T1 if self.transport == "UDP" else now + 64 * T1
            self.pending[msg.branch, msg.method] = _Tx(msg, first, T1, now + 64 * T1)

    def retransmit(self) -> float:
        """Resend what is due; seconds until the next resend (at most 0.1)."""
        now, wait = time.monotonic(), 0.1
        for key, tx in list(self.pending.items()):
            if now >= tx.end:
                del self.pending[key]
                continue
            if now >= tx.due:
                self.sock.sendto(tx.msg.render(), self.peer)
                tx.interval = (
                    tx.interval * 2 if tx.msg.method == "INVITE" else min(tx.interval * 2, T2)
                )
                tx.due = now + tx.interval
            wait = min(wait, tx.due - now)
        return max(0.001, wait)

    def answered(self, resp: Message) -> None:
        """A response arrived: stop retransmitting its request (INVITE: on any response)."""
        key = (resp.branch, resp.cseq_method)
        if (tx := self.pending.get(key)) is None:
            return
        if resp.status >= 200:
            del self.pending[key]
        elif tx.msg.method == "INVITE":
            tx.due = tx.end  # timer A stops; the entry stays until the final response

    def recv(self, timeout: float) -> Message | None:
        """Next message within `timeout`, retransmitting meanwhile."""
        deadline = time.monotonic() + timeout
        while (left := deadline - time.monotonic()) > 0:
            self.sock.settimeout(min(left, self.retransmit()))
            try:
                data, _ = self.sock.recvfrom(65535)
            except TimeoutError:
                continue
            msg = parse(data)
            if msg.status:
                self.answered(msg)
            return msg
        return None

    def confirm(self, ok: Message) -> None:
        """UAC: take the remote tag, target and route set from a 2xx to INVITE, and ACK it."""
        self.remote = ok.get("to")
        self.target = uri_of(ok.get("contact")) or self.target
        self.routes = list(reversed(ok.all("record-route")))
        self.ack(ok)

    def ack(self, ok: Message, body: bytes = b"") -> None:
        """ACK a 2xx to an INVITE (with `body`, the answer to an offer in the 2xx)."""
        ack = self.request("ACK", body)
        cseq = ok.get("cseq").split()[0] + " ACK"
        ack.headers = [(k, cseq if k == "CSeq" else v) for k, v in ack.headers]
        self.send(ack)

    def _same_transaction(self, invite: Message, method: str, to: str) -> Message:
        """ACK of a non-2xx, or CANCEL: the INVITE's branch, Request-URI and CSeq number."""
        keep = ("Via", "Route", "Max-Forwards", "From", "Call-ID")
        headers = [(k, v) for k, v in invite.headers if k in keep]
        headers += [("To", to), ("CSeq", invite.get("cseq").split()[0] + " " + method)]
        return Message(f"{method} {invite.first.split()[1]} SIP/2.0", headers)

    def ack_failure(self, invite: Message, resp: Message) -> None:
        self.send(self._same_transaction(invite, "ACK", resp.get("to")))

    def cancel(self, invite: Message) -> Message:
        msg = self._same_transaction(invite, "CANCEL", invite.get("to"))
        self.send(msg)
        return msg

    def reply(self, req: Message, status: int = 200, reason: str = "OK", body: bytes = b"") -> None:
        extra = [("Contact", self.contact)] if req.method == "INVITE" else []
        resp = response(req, status, reason, tag(self.local), body, extra)
        self.sock.sendto(resp.render(), self.peer)
