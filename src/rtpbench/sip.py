"""Minimal SIP over UDP: enough for one audio call as UAC or UAS (RFC 3261 subset)."""

import secrets
import socket
import time
from dataclasses import dataclass, field

from rtpbench.g711 import NAMES

T1 = 0.5
_COMPACT = {
    "i": "call-id",
    "f": "from",
    "t": "to",
    "v": "via",
    "m": "contact",
    "l": "content-length",
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


def tag(value: str) -> str:
    for param in value.split(";")[1:]:
        if param.strip().lower().startswith("tag="):
            return param.split("=", 1)[1].strip()
    return ""


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


def sdp(ip: str, port: int, pts: list[int]) -> bytes:
    sid = secrets.randbelow(1 << 31)
    lines = [
        "v=0",
        f"o=rtpbench {sid} {sid} IN IP4 {ip}",
        "s=rtpbench",
        f"c=IN IP4 {ip}",
        "t=0 0",
        f"m=audio {port} RTP/AVP {' '.join(map(str, pts))}",
        *(f"a=rtpmap:{pt} {NAMES[pt]}/8000" for pt in pts),
        "a=ptime:20",
        "a=sendrecv",
    ]
    return ("\r\n".join(lines) + "\r\n").encode()


def parse_sdp(body: bytes) -> tuple[str, int, list[int]]:
    """Connection address, audio port and offered payload types."""
    ip, port, pts = "", 0, []
    for line in body.decode(errors="replace").splitlines():
        if line.startswith("c=IN IP4 "):
            ip = line.split()[2]
        elif line.startswith("m=audio "):
            fields = line.split()
            port, pts = int(fields[1]), [int(p) for p in fields[3:]]
    return ip, port, pts


class SipError(Exception):
    pass


class Dialog:
    """One call from the UAC side: INVITE, ACK, in-dialog requests and BYE."""

    def __init__(self, sock: socket.socket, peer: tuple[str, int], uri: str, local_ip: str) -> None:
        self.sock, self.peer, self.uri, self.local_ip = sock, peer, uri, local_ip
        port = sock.getsockname()[1]
        self.contact = f"<sip:rtpbench@{local_ip}:{port}>"
        self.from_ = f"<sip:rtpbench@{local_ip}>;tag={secrets.token_hex(4)}"
        self.to = f"<{uri}>"
        self.call_id = f"{secrets.token_hex(8)}@{local_ip}"
        self.cseq = 1
        self.target = uri
        self.routes: list[str] = []

    def _request(self, method: str, branch: str, body: bytes = b"", uri: str = "") -> Message:
        port = self.sock.getsockname()[1]
        headers = [("Via", f"SIP/2.0/UDP {self.local_ip}:{port};branch={branch};rport")]
        headers += [("Route", r) for r in self.routes]
        headers += [
            ("Max-Forwards", "70"),
            ("From", self.from_),
            ("To", self.to),
            ("Call-ID", self.call_id),
            ("CSeq", f"{self.cseq} {method}"),
            ("Contact", self.contact),
            ("User-Agent", "rtpbench"),
        ]
        if body:
            headers.append(("Content-Type", "application/sdp"))
        return Message(f"{method} {uri or self.target} SIP/2.0", headers, body)

    def _send(self, msg: Message) -> None:
        self.sock.sendto(msg.render(), self.peer)

    def recv(self, timeout: float) -> Message | None:
        self.sock.settimeout(timeout)
        try:
            data, _ = self.sock.recvfrom(65535)
        except TimeoutError:
            return None
        return parse(data)

    def invite(self, offer: bytes, timeout: float = 32.0) -> Message:
        """Send INVITE with retransmissions (timer A), ACK the final response, return the 2xx."""
        branch = "z9hG4bK" + secrets.token_hex(6)
        req = self._request("INVITE", branch, offer)
        deadline, interval, provisional = time.monotonic() + timeout, T1, False
        self._send(req)
        resend = time.monotonic() + interval
        while time.monotonic() < deadline:
            msg = self.recv(max(0.01, (deadline if provisional else resend) - time.monotonic()))
            if msg is None:
                if not provisional:
                    self._send(req)
                    interval = min(interval * 2, 4.0)
                    resend = time.monotonic() + interval
                continue
            if msg.get("call-id") != self.call_id or msg.cseq_method != "INVITE":
                continue
            if msg.status < 200:
                provisional = True
                continue
            self.to = msg.get("to")
            if msg.status >= 300:
                ack = self._request("ACK", branch, uri=self.uri)
                self._send(ack)
                raise SipError(msg.first)
            self.target = uri_of(msg.get("contact")) or self.uri
            self.routes = list(reversed(msg.all("record-route")))
            self.ack()
            return msg
        raise SipError("INVITE timed out")

    def ack(self) -> None:
        self._send(self._request("ACK", "z9hG4bK" + secrets.token_hex(6)))

    def reply(self, req: Message) -> None:
        """Answer an in-dialog request from the far end (BYE, OPTIONS, re-INVITE refused)."""
        if req.method == "ACK":
            return
        if req.method == "INVITE":
            self._send(response(req, 488, "Not Acceptable Here"))
        else:
            self._send(response(req, 200, "OK"))

    def bye(self, timeout: float = 8.0) -> None:
        self.cseq += 1
        req = self._request("BYE", "z9hG4bK" + secrets.token_hex(6))
        deadline, interval = time.monotonic() + timeout, T1
        while time.monotonic() < deadline:
            self._send(req)
            end = time.monotonic() + interval
            while (left := end - time.monotonic()) > 0:
                msg = self.recv(left)
                if msg is None:
                    break
                if msg.status and msg.cseq_method == "BYE":
                    return
                if msg.status == 200 and msg.cseq_method == "INVITE":
                    self.ack()
                elif msg.method:
                    self.reply(msg)
            interval = min(interval * 2, 4.0)
