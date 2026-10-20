"""Minimal SIP over UDP, TCP or TLS: one audio call as UAC or UAS (RFC 3261 subset).

Messages stay plain header lists, so a caller can add, drop or reorder anything before sending.
"""

import hashlib
import re
import secrets
import select
import socket
import ssl
import time
from dataclasses import dataclass, field
from pathlib import Path

from rtpbench import pcap, tls
from rtpbench.g711 import NAMES

T1, T2 = 0.5, 4.0
TLS_PORT = 5061
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


def secure(uri: str) -> bool:
    """Whether a URI asks for TLS: a sips: URI, or transport=tls (RFC 3261 19.1.1)."""
    params = uri.split(">", 1)[0].lower().split(";")
    return params[0].startswith("sips:") or "transport=tls" in params[1:]


def contact(user: str, ip: str, port: int, transport: str, sips: bool = False) -> str:
    """A Contact for this transport: sips: when the request was (RFC 5630 4.1), else sip: with
    transport=tcp or tls on a stream."""
    if sips:
        return f"<sips:{user}@{ip}:{port}>"
    param = f";transport={transport.lower()}" if transport != "UDP" else ""
    return f"<sip:{user}@{ip}:{port}{param}>"


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
    crypto: list[str] | None = None,
) -> bytes:
    """An audio offer or answer; `origin` (session id, version) for a later one; `dtmf` adds
    RFC 4733 telephone-event; `conn` another connection address (0.0.0.0: RFC 2543 hold);
    `direction` "" leaves the attribute out; `crypto`, a=crypto values, makes it SRTP
    (RTP/SAVP, RFC 4568)."""
    sid, version = origin or (secrets.randbelow(1 << 31),) * 2
    events = [TELEPHONE_EVENT] if dtmf else []
    lines = [
        "v=0",
        f"o=rtpbench {sid} {version} IN IP4 {ip}",
        "s=rtpbench",
        f"c=IN IP4 {conn or ip}",
        "t=0 0",
        f"m=audio {port} RTP/{'SAVP' if crypto else 'AVP'} {' '.join(map(str, [*pts, *events]))}",
        *(f"a=rtpmap:{pt} {NAMES[pt]}/8000" for pt in pts),
        *(f"a=rtpmap:{pt} telephone-event/8000" for pt in events),
        *(f"a=fmtp:{pt} 0-16" for pt in events),
        *(f"a=crypto:{c}" for c in crypto or []),
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
    proto: str = "RTP/AVP"
    crypto: list[str] = field(default_factory=list)  # a=crypto values (RFC 4568)


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
                out.port, out.proto = int(fields[1]), fields[2]
                out.pts = [int(p) for p in fields[3:]]
            other = not media
        elif other:  # a section before the audio one (video, say): not ours
            continue
        elif line.startswith("c=IN IP4 ") and (media or not out.ip):
            out.ip = line.split()[2]
        elif line[2:] in DIRECTIONS:  # media level comes later, so it wins
            out.direction = line[2:]
        elif line.lower().startswith("a=rtpmap:") and "telephone-event/8000" in line.lower():
            out.dtmf = int(line[9:].split()[0])
        elif media and line.startswith("a=crypto:"):
            out.crypto.append(line[9:].strip())
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
    (RFC 8760), plain or -sess (with qop auth), qop auth or none."""
    offers = []
    for value in challenges:
        scheme, _, rest = value.strip().partition(" ")
        if scheme.lower() != "digest":
            continue
        p = {m[1].lower(): m[3] if m[3] is not None else m[2] for m in _PARAM.finditer(rest)}
        algorithm = p.get("algorithm", "MD5").upper()
        qops = [q.strip() for q in p.get("qop", "").split(",") if q.strip()]
        # -sess hashes a cnonce in, which only goes out with a qop (RFC 7616 3.4.2)
        usable = "auth" in qops or not (qops or algorithm.endswith("-SESS"))
        if algorithm.removesuffix("-SESS") in _HASH and usable:
            offers.append((list(_HASH).index(algorithm.removesuffix("-SESS")), algorithm, p, qops))
    if not offers:
        raise SipError(f"no digest challenge this caller supports: {'; '.join(challenges)}")
    _, algorithm, p, qops = max(offers, key=lambda o: o[0])
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
    if qops:  # one request per nonce here, so nc is always 1
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
    reuse_port = False  # SO_REUSEPORT on the listener, so connections can leave from its port

    def __init__(self, port: int = 0) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.reuse_port:
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
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
            conn = self._open(addr)
            conn.settimeout(None)
            self.conns[addr], self.buf[addr] = conn, b""
        self.conns[addr].sendall(data)

    def _open(self, addr: tuple[str, int]) -> socket.socket:
        """A connection to `addr`, ready for SIP."""
        return socket.create_connection(addr, timeout=5)

    def _accept(self, conn: socket.socket) -> socket.socket | None:
        """A connection the far end opened, ready for SIP; None to refuse it."""
        return conn

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
                    if (accepted := self._accept(conn)) is not None:
                        self.conns[addr], self.buf[addr] = accepted, b""
                    continue
                addr = next(a for a, c in self.conns.items() if c is s)
                try:
                    data = s.recv(65535)
                    # TLS hands one record over per recv; the rest is decrypted already, and
                    # select would not wake for it
                    while isinstance(s, ssl.SSLSocket) and s.pending():
                        data += s.recv(s.pending())
                except ssl.SSLError:  # a TLS alert, or the connection cut mid-record
                    data = b""
                if data:
                    self.buf[addr] += data
                else:  # closed by the peer
                    s.close()
                    del self.conns[addr]
        return got

    def close(self) -> None:
        for s in self.sockets():
            s.close()


class Tls(Tcp):
    """SIP over TLS (RFC 3261 26.2.1): `Tcp` on TLS connections. Opens them with `client`,
    checking the certificate of `hostname`; accepts them with `server`, or refuses them.

    Its connections leave from the port it listens on, which its Contact and Via give: a far end
    that sends its own requests to the Contact finds the connection already open to that address
    and reuses it, instead of opening one back through the NATs and port forwards on the way."""

    transport = "TLS"
    reuse_port = True

    def __init__(
        self,
        port: int = 0,
        client: ssl.SSLContext | None = None,
        server: ssl.SSLContext | None = None,
        hostname: str | None = None,
    ) -> None:
        super().__init__(port)
        self.client, self.accepting, self.hostname = client, server, hostname
        self.first: dict[str, str] = {}  # version and cipher of the first handshake

    def _open(self, addr: tuple[str, int]) -> socket.socket:
        if self.client is None:
            raise ConnectionRefusedError("no TLS client context")
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for opt in (socket.SO_REUSEADDR, socket.SO_REUSEPORT):
            conn.setsockopt(socket.SOL_SOCKET, opt, 1)
        conn.settimeout(5)
        try:
            conn.bind(("0.0.0.0", self.getsockname()[1]))
            conn.connect(addr)
            tls_conn = self.client.wrap_socket(conn, server_hostname=self.hostname)
        except OSError:
            conn.close()
            raise
        self._note(tls_conn)
        return tls_conn

    def _note(self, conn: ssl.SSLSocket) -> None:
        if not self.first and (cipher := conn.cipher()):
            self.first = {"version": conn.version() or "", "cipher": cipher[0]}

    def _accept(self, conn: socket.socket) -> socket.socket | None:
        if self.accepting is None:
            conn.close()
            return None
        conn.settimeout(5)  # the handshake; a peer that stalls it is dropped
        try:
            tls_conn = self.accepting.wrap_socket(conn, server_side=True)
        except OSError:  # ssl.SSLError among them
            conn.close()
            return None
        tls_conn.settimeout(None)
        self._note(tls_conn)
        return tls_conn

    def negotiated(self) -> dict[str, str]:
        """TLS version and cipher suite of the first connection, closed or not."""
        return self.first


_SIP = re.compile(rb"(SIP/2\.0 \d{3} |[A-Z]+ \S+ SIP/2\.0\r\n)")


def captured(grams: list[pcap.Datagram], keys: Path | None = None) -> list[tuple[int, str, bytes]]:
    """Every SIP message in a capture, in capture order, with its time and sender: datagrams,
    and messages framed from the TCP streams (TLS ones decrypted with the key log `keys`)."""
    udp = [(g.t_ns, g.src, g.payload) for g in grams if not g.tcp and _SIP.match(g.payload)]
    return sorted([*_over_tcp(tls.streams(grams, keys)), *udp])


def _over_tcp(segs: list[pcap.Datagram]) -> list[tuple[int, str, bytes]]:
    """SIP messages in the TCP streams, framed by Content-Length (RFC 3261 18.3), each at the
    capture time of the segment that brought its first byte."""
    out = []
    flows: dict[tuple[str, int, str, int], tuple[bytes, int]] = {}  # bytes not yet a message
    for g in segs:
        flow = (g.src, g.sport, g.dst, g.dport)
        buf, t = flows.get(flow, (b"", g.t_ns))
        buf, t = buf + g.payload, t if buf.strip(b"\r\n") else g.t_ns
        while True:
            buf = buf.lstrip(b"\r\n")  # keep-alive CRLFs
            head, sep, rest = buf.partition(b"\r\n\r\n")
            length = int(parse(head + sep).get("content-length") or 0) if sep else 0
            if not sep or len(rest) < length or not _SIP.match(buf):
                break
            out.append((t, g.src, head + sep + rest[:length]))
            buf, t = rest[length:], g.t_ns
        flows[flow] = (buf, t)
    return out


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
        port, sips = sock.getsockname()[1], target.lower().startswith("sips:")
        self.contact = contact(user, local_ip, port, self.transport, sips)
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
        via = f"SIP/2.0/{self.transport} {self.local_ip}:{port};branch={branch};rport"
        # TLS: ask the far end to send its own requests on this connection (RFC 5923)
        hdrs = [("Via", via + ";alias" if self.transport == "TLS" else via)]
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
