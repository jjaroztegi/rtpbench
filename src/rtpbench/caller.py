"""Caller: speaks fixed turns (synthetic or from WAV files) over a real SIP call, or, for
barge-in, reacts to the agent: prompt, wait for the reply, cut in, wait for quiet."""

import bisect
import os
import random
import secrets
import socket
import ssl
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from rtpbench import bargein, g711, sip, speech, srtp, tls
from rtpbench.clock import CLOCK
from rtpbench.rtp import FRAME, PTIME_NS, SAMPLE_NS, Frame, Packet, Receiver, Sender
from rtpbench.voice import GATE, RATE, voice

LEAD_SECONDS = 1.0
UTTERANCE_RANGE = (0.8, 1.6)
GAP_SECONDS = 2.8  # longest delay (1.3 s) + response (0.8 s) + room for netem
QUIET_NS = 3_000_000_000  # agent silence that ends its turn (a real agent answers a barge-in)
REPLY_TIMEOUT_NS = 15_000_000_000
TURN_TIMEOUT_NS = 60_000_000_000
# The caller binds its SIP and RTP sockets from the advertised port on (RTPBENCH_ADVERTISE,
# HOST:PORT), so the router can forward them: a transfer's two calls take four. ADVERTISE_PORT is
# the first when the router's own address on the agent's network is advertised.
ADVERTISE_PORT, ADVERTISE_PORTS = 40000, 8
NO_MEDIA = (
    "an agent that sends its audio to the address in our offer, not back to where ours comes "
    "from, needs that address reachable: see rtpbench target --network and --advertise"
)

Clip = tuple[str, list[int]]
Source = Callable[[int, int], bytes | Frame | None]
Labelled = tuple[str, list[int], list[tuple[int, int]]]


def speech_utterances(seed: int) -> list[Clip]:
    """Every short corpus clip, in a seeded order unlike the agent's replies."""
    clips = [(n, pcm) for n, pcm in speech.clips("tts-", "human-").items() if "-long" not in n]
    random.Random(seed + 1).shuffle(clips)
    return clips


def interjections(seed: int) -> dict[str, list[Clip]]:
    """Corpus clips for each interjection kind, shuffled."""
    out = {
        "interrupt": speech_utterances(seed + 1),
        "backchannel": [(n, p) for n, p in speech.clips("tts-").items() if n.endswith("-bc")],
        "cough": list(speech.clips("cough-").items()),
    }
    for clips in out.values():
        random.Random(seed).shuffle(clips)
    return out


def script(
    turns: int,
    seed: int,
    utterances: list[list[int]] | None = None,
    lead: float = LEAD_SECONDS,
    gap: float = GAP_SECONDS,
) -> tuple[list[int], list[tuple[int, int]]]:
    """PCM for the whole call, and the [start, end) sample span of each turn's utterance."""
    rng = random.Random(seed)
    pcm, spans = [0] * round(lead * RATE), []
    for i in range(turns):
        start = len(pcm)
        pcm += (
            utterances[i % len(utterances)]
            if utterances
            else voice(rng.uniform(*UTTERANCE_RANGE), f0=140)
        )
        spans.append((start, len(pcm)))
        pcm += [0] * round(gap * RATE)
    return pcm, spans


def _udp(port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(("0.0.0.0", port))
    except OSError:
        sock.close()
        raise
    return sock


def _bind[S](make: Callable[[int], S], ports: range) -> S:
    """A socket from `make` on the first of `ports` it can bind."""
    for port in ports:
        try:
            return make(port)
        except OSError:
            continue
    raise sip.SipError(f"no free port in {ports.start}-{ports.stop - 1}")


def parse_uri(uri: str) -> tuple[str, int]:
    hostport = uri.split("@", 1)[-1].split(";", 1)[0]
    scheme, sep, rest = hostport.partition(":")
    if sep and scheme.lower() in ("sip", "sips"):  # no user part; schemes ignore case
        hostport = rest
    host, _, port = hostport.partition(":")
    return host, int(port or (sip.TLS_PORT if sip.secure(uri) else 5060))


def _tls(port: int, hostname: str) -> sip.Tls:
    """SIP over TLS from `port`, checking `hostname`'s certificate against the system's trusted
    certificates, or against RTPBENCH_TLS/ca.pem if there is one; with RTPBENCH_TLS/server.crt
    (and .key) it also takes connections the far end opens. The contexts log their session
    keys to SSLKEYLOGFILE, which judging needs to read the capture."""
    where = Path(os.environ.get("RTPBENCH_TLS", "/nonexistent"))
    ca = where / "ca.pem"
    client = ssl.create_default_context(cafile=ca if ca.exists() else None)
    client.minimum_version = ssl.TLSVersion.TLSv1_2
    client.set_ciphers(tls.CIPHERS_12)
    server = None
    if (where / "server.crt").exists():
        server = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        server.load_cert_chain(where / "server.crt", where / "server.key")
    return sip.Tls(port, client, server, hostname)


class Session:
    """One call: the SIP dialog and the RTP socket, from INVITE to BYE (sent to the URI's host,
    or to `proxy`, a host[:port]; over UDP, or TCP with `tcp`).

    The INVITE goes out at once; `wait` pumps SIP (retransmissions, answers to what the far end
    sends) until a condition holds, so a script can act between messages while media flows.
    """

    def __init__(
        self,
        uri: str,
        codecs: tuple[int, ...],
        headers: list[tuple[str, str]] | None = None,
        dtmf: bool = False,
        proxy: str | None = None,
        tcp: bool = False,
    ) -> None:
        host, port = parse_uri(proxy or uri)  # an outbound proxy takes it whatever its URI
        # hosts as the router resolved them (RTPBENCH_RESOLVE, HOST=IP,...): a name on the
        # agent's Docker network resolves only there, and netem needs the same address
        names = os.environ.get("RTPBENCH_RESOLVE", "").split(",")
        resolved = dict(n.split("=", 1) for n in names if "=" in n)
        peer = (resolved.get(host, host), port)
        if advertise := os.environ.get("RTPBENCH_ADVERTISE"):
            local_ip, _, first = advertise.rpartition(":")
            ports = range(int(first), int(first) + ADVERTISE_PORTS)
        else:
            probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            probe.connect(peer)
            local_ip, ports = probe.getsockname()[0], range(1)  # port 0: any
        sock: socket.socket | sip.Tcp
        # sip.Tcp raises ConnectionRefusedError at the INVITE if the far end takes no TCP
        if sip.secure(uri):
            sock = _bind(lambda p: _tls(p, host), ports)
        else:
            sock = _bind(sip.Tcp, ports) if tcp else _bind(_udp, ports)
        self.rtp = _bind(_udp, ports)
        self.dialog = sip.Dialog.uac(sock, peer, uri, local_ip)
        self.origin = (secrets.randbelow(1 << 31), 0)  # SDP session id, version
        # SRTP (RTPBENCH_SRTP: the suites to offer, in order): our master key per suite, and
        # once answered, the suite and the contexts we send and hear with
        self.offered = [s for s in os.environ.get("RTPBENCH_SRTP", "").split(",") if s]
        self.keys = srtp.master() if self.offered else {}
        self.suite: str | None = None
        self.tx: srtp.Context | None = None
        self.rx: srtp.Context | None = None
        self.srtp_error = ""
        self.held = False
        self.dtmf: int | None = None  # telephone-event payload type, if the answer has it
        port = self.rtp.getsockname()[1]
        offer = sip.sdp(
            local_ip, port, list(codecs), origin=self.origin, dtmf=dtmf, crypto=self._crypto()
        )
        self.headers = headers
        user, password = (os.environ.get(f"RTPBENCH_SIP_{k}") for k in ("USER", "PASSWORD"))
        self.credentials = (user, password) if user and password else None
        self.invite = self.dialog.request("INVITE", offer, headers)
        self.invites = {self.invite.branch: self.invite}
        self.final: sip.Message | None = None  # final response to the INVITE
        self.responses: list[sip.Message] = []
        self.requests: list[sip.Message] = []  # from the far end
        self.remote_bye = False
        self.addr, self.pt = ("", 0), 0
        self.seq0, self.ssrc = secrets.randbelow(1 << 16), secrets.randbelow(1 << 32)
        self.media: tuple[Sender, Receiver] | None = None
        try:
            self.dialog.send(self.invite)
        except OSError as e:  # over TCP the caller may retry over UDP; over TLS it cannot
            if not sip.secure(uri):
                raise
            raise sip.SipError(f"TLS to {peer[0]}:{peer[1]}: {type(e).__name__}: {e}") from e

    def pump(self, timeout: float) -> None:
        """Handle the next SIP message, if one comes within `timeout`."""
        msg = self.dialog.recv(timeout)
        if msg is None or msg.get("call-id") != self.dialog.call_id:
            return
        if not msg.status:
            self._incoming(msg)
            return
        self.responses.append(msg)
        if msg.cseq_method != "INVITE" or msg.status < 200:
            return
        initial = msg.branch == self.invite.branch
        if msg.status >= 300:
            if req := self.invites.get(msg.branch):
                self.dialog.ack_failure(req, msg)
            if initial and (again := self._authorize(self.invite, msg, self.headers)):
                self.invite = again
            elif initial:
                self.final = msg
            return
        if not initial:
            req = self.invites.get(msg.branch)
            if req is not None and req.body and self.offered:  # the answer to our re-offer
                self._srtp(sip.parse_sdp(msg.body))
            self.dialog.ack(msg, self._answer(msg) if req is not None and not req.body else b"")
            return
        self.dialog.confirm(msg)  # every 2xx, retransmissions included
        if self.final is None:
            self.final = msg
            answer = sip.parse_sdp(msg.body)
            self.addr = (answer.ip, answer.port)
            self.pt = next((p for p in answer.pts if p in g711.NAMES), -1)  # -1: answer() ends it
            self.dtmf = answer.dtmf
            if self.offered:
                try:
                    self._srtp(answer)
                except sip.SipError as e:  # answer() ends it
                    self.srtp_error = str(e)

    def _crypto(self, offer: sip.Sdp | None = None) -> list[str] | None:
        """a=crypto values for our next SDP, if we use SRTP: as an offer, every suite we offer
        (the one in use, once there is one); as the answer to `offer`, its line for our suite."""
        if not self.offered:
            return None
        if offer is None:
            suites = [self.suite] if self.suite else self.offered
            return [srtp.line(i + 1, s, self.keys[s]) for i, s in enumerate(suites)]
        tag = self._srtp(offer)
        assert self.suite is not None
        return [srtp.line(tag, self.suite, self.keys[self.suite])]

    def _srtp(self, sdp: sip.Sdp) -> int:
        """Take the agent's key from its SDP for the suite in use (or the first we offered that
        it gives): we hear with it from now on. Its tag; SipError if it gives none of ours."""
        usable = []
        for value in sdp.crypto:
            try:
                usable.append(srtp.parse(value))
            except ValueError:
                continue
        wanted = [self.suite] if self.suite else self.offered
        tag, suite, key = next((c for c in usable if c[1] in wanted), (0, "", b""))
        if not suite:
            given = ", ".join(sdp.crypto) or f"no a=crypto, {sdp.proto}"
            raise sip.SipError(
                f"the agent's SDP has no SRTP suite of {', '.join(wanted)} ({given})"
            )
        if self.tx is None:
            self.suite, self.tx = suite, srtp.Context(suite, self.keys[suite])
        if self.rx is None or self.rx.master != key:
            self.rx = srtp.Context(suite, key)
            if self.media:
                self.media[1].srtp = self.rx
        return tag

    def _authorize(
        self,
        req: sip.Message,
        resp: sip.Message,
        headers: list[tuple[str, str]] | None,
        content_type: str = "application/sdp",
    ) -> sip.Message | None:
        """Send `req` again (a new CSeq) with credentials for the challenge in `resp`, if it is
        one (401, 407), we have credentials (RTPBENCH_SIP_USER, RTPBENCH_SIP_PASSWORD) and `req`
        did not carry them already; the new request."""
        if resp.status not in (401, 407) or self.credentials is None:
            return None
        if req.get("authorization") or req.get("proxy-authorization"):
            return None  # these credentials were refused
        name = "Authorization" if resp.status == 401 else "Proxy-Authorization"
        asked = resp.all("www-authenticate" if resp.status == 401 else "proxy-authenticate")
        value = sip.digest(asked, req.method, req.first.split()[1], *self.credentials)
        hdrs = [*(headers or []), (name, value)]
        again = self.dialog.request(req.method, req.body, hdrs, content_type)
        if again.method == "INVITE":
            self.invites[again.branch] = again
        self.dialog.send(again)
        return again

    def _answer(self, ok: sip.Message) -> bytes:
        """Answer to the offer in a 2xx to a re-INVITE without one (RFC 3261 14.1): the call's
        codec if offered (else the first G.711 offered), the address it gives from now on."""
        offer = sip.parse_sdp(ok.body)
        if not offer.port:
            return b""  # no offer in it: the agent got it wrong; the ACK has nothing to answer
        if self.pt not in offer.pts:
            self.pt = next((p for p in offer.pts if p in g711.NAMES), self.pt)
        self.addr = (offer.ip, offer.port)
        if self.media:
            self.media[0].addr = self.addr
        port = self.rtp.getsockname()[1]
        direction = sip.ANSWER[offer.direction]
        crypto = self._crypto(offer)
        return sip.sdp(self.dialog.local_ip, port, [self.pt], direction, self.origin, crypto=crypto)

    def _incoming(self, req: sip.Message) -> None:
        self.requests.append(req)
        if req.method == "ACK":
            return
        if req.method == "INVITE":  # a refresh, or a change we take as it comes
            port = self.rtp.getsockname()[1]
            crypto = self._crypto(sip.parse_sdp(req.body) if req.body else None)
            sdp = sip.sdp(self.dialog.local_ip, port, [self.pt], origin=self.origin, crypto=crypto)
            self.dialog.reply(req, 200, "OK", sdp)
            return
        self.dialog.reply(req, *((202, "Accepted") if req.method == "REFER" else ()))
        self.remote_bye |= req.method == "BYE"

    def wait(self, cond: Callable[[], bool], timeout: float) -> bool:
        """Pump SIP until `cond()` or `timeout` seconds; whether `cond()` held."""
        deadline = time.monotonic() + timeout
        while not cond():
            if (left := deadline - time.monotonic()) <= 0:
                return False
            self.pump(min(left, 0.05))
        return True

    @property
    def ringing(self) -> bool:
        """A provisional response to the INVITE arrived (so it may be cancelled)."""
        return any(r.branch == self.invite.branch and r.status < 200 for r in self.responses)

    def cancel(self) -> None:
        self.dialog.cancel(self.invite)

    def answer(self, timeout: float = 32.0) -> sip.Message:
        """The 2xx to the INVITE (ACKed); raises on a failure, no answer, or an answer without
        G.711 (after hanging up)."""
        self.wait(lambda: self.final is not None, timeout)
        if self.final is None:
            raise sip.SipError("INVITE timed out")
        if self.final.status >= 300:
            raise sip.SipError(self.final.first)
        if self.srtp_error:
            self.request("BYE")
            raise sip.SipError(self.srtp_error)
        if self.pt < 0:
            self.request("BYE")
            pts = " ".join(map(str, sip.parse_sdp(self.final.body).pts))
            raise sip.SipError(f"answer has no G.711 format (payload types {pts or 'none'})")
        return self.final

    def request(
        self,
        method: str,
        body: bytes = b"",
        headers: list[tuple[str, str]] | None = None,
        content_type: str = "application/sdp",
    ) -> sip.Message | None:
        """Send an in-dialog request; its final response, or None after timer F (32 s)."""
        req = self.dialog.request(method, body, headers, content_type)
        if method == "INVITE":
            self.invites[req.branch] = req
        self.dialog.send(req)

        def final() -> sip.Message | None:
            return next(
                (r for r in self.responses if r.branch == req.branch and r.status >= 200), None
            )

        self.wait(lambda: final() is not None, 64 * sip.T1)
        if (resp := final()) is not None and (
            again := self._authorize(req, resp, headers, content_type)
        ):
            req = again
            self.wait(lambda: final() is not None, 64 * sip.T1)
        return final()

    def reinvite(
        self,
        direction: str = "sendrecv",
        headers: list[tuple[str, str]] | None = None,
        conn: str | None = None,
        offer: bool = True,
        pt: int | None = None,
    ) -> sip.Message | None:
        """Offer the call's codec again, `direction` (sendonly, inactive: hold; sendrecv
        unchanged: a refresh, same SDP version; "": no attribute); `conn` 0.0.0.0 holds the RFC
        2543 way; `pt` offers that codec alone instead (a codec change: the media switches to it
        on a 2xx); `offer` False sends no SDP (the 2xx offers, the ACK answers). The response."""
        hold = direction not in ("sendrecv", "") or conn == "0.0.0.0"
        if hold or self.held or pt is not None:
            self.origin = (self.origin[0], self.origin[1] + 1)
        self.held = hold
        port = self.rtp.getsockname()[1]
        codec = self.pt if pt is None else pt
        sdp = sip.sdp(
            self.dialog.local_ip,
            port,
            [codec],
            direction,
            self.origin,
            conn=conn,
            crypto=self._crypto(),
        )
        resp = self.request("INVITE", sdp if offer else b"", headers)
        if pt is not None and resp is not None and resp.status < 300:
            self.pt = pt
            if self.media:
                self.media[0].pt = pt
        return resp

    def start(self, source: Source, sink: Callable[[int, Packet], None]) -> None:
        start = CLOCK.now() + PTIME_NS
        self.media = (
            Sender(self.rtp, self.addr, self.pt, source, start, self.seq0, self.ssrc, srtp=self.tx),
            Receiver(self.rtp, sink, srtp=self.rx),
        )
        for t in self.media:
            t.start()

    def switch(self) -> None:
        """The caller's audio becomes a new RTP source mid-call, as when a gateway upstream swaps
        media (random SSRC, seq and timestamp origin, marker); `meta` describes the new one."""
        assert self.media is not None
        sender = self.media[0]
        ssrc, seq = secrets.randbelow(1 << 32), secrets.randbelow(1 << 16)
        sender.switch(ssrc, seq, secrets.randbelow(1 << 32))
        self.wait(lambda: sender.switched is not None, 1.0)
        assert sender.switched is not None
        # sample k of the call (from tick 0) is still in the packet with seq seq0 + k // 160
        self.ssrc, self.seq0 = ssrc, (seq - sender.switched) & 0xFFFF

    def hangup(self) -> None:
        """Stop sending, BYE unless the far end hung up, stop receiving."""
        if self.media:
            self.media[0].stop.set()
            self.media[0].join()
        if not self.remote_bye:
            self.request("BYE")
        if self.media:
            self.media[1].stop.set()
            self.media[1].join()

    def run(
        self,
        source: Source,
        sink: Callable[[int, Packet], None],
        until: Callable[[int], bool],
    ) -> bool:
        """Media until `until(now_ns)`, then hang up. True if the far end hung up first."""
        self.start(source, sink)
        self.wait(lambda: self.remote_bye or until(CLOCK.now()), float("inf"))
        self.hangup()
        return self.remote_bye

    def no_media(self, seconds: float) -> sip.SipError:
        return sip.SipError(
            f"no RTP from the agent in {seconds:.0f} s; our offer gave"
            f" c=IN IP4 {self.dialog.local_ip}: {NO_MEDIA}"
        )

    def meta(self, seed: int, remote_bye: bool) -> dict[str, Any]:
        return {"pt": self.pt, "ssrc": self.ssrc, "seq0": self.seq0, "seed": seed} | {
            "remote_bye": remote_bye,
            "call_id": self.dialog.call_id,
            "rtp_port": self.rtp.getsockname()[1],
            "transport": self.dialog.transport,
            **({"srtp": self.suite} if self.offered else {}),
            **({"tls": sock.negotiated()} if isinstance(sock := self.dialog.sock, sip.Tls) else {}),
            "send_errors": self.media[0].send_errors if self.media else [],
        }


def call(
    uri: str,
    turns: int = 20,
    seed: int = 1,
    utterances: list[Clip] | None = None,
    lead: float = LEAD_SECONDS,
    gap: float = GAP_SECONDS,
    codecs: tuple[int, ...] = (g711.PCMU, g711.PCMA),
) -> dict[str, Any]:
    """Place the call; return where each turn's speech ended (packet and sample).

    With utterances, each turn also carries its labelled speech spans as sample indices of the
    stream (sample k is sample k % 160 of the packet with seq seq0 + k // 160).
    """
    labels = [(n, speech.label(u)) for n, u in utterances] if utterances else []
    s = Session(uri, codecs)
    s.answer()
    pcm, spans = script(turns, seed, [u for _, u in utterances or []], lead, gap)
    audio = g711.encode(s.pt, pcm)
    gate = g711.gate(s.pt, GATE)
    silence = bytes([g711.SILENCE[s.pt]]) * FRAME
    frames = [audio[i : i + FRAME].ljust(FRAME, silence[:1]) for i in range(0, len(audio), FRAME)]
    last: list[dict[str, Any]] = []
    for i, (start, end) in enumerate(spans):  # last sample the gate calls active, as the agent sees
        m = gate.search(audio[start:end][::-1])
        assert m is not None
        idx = end - 1 - m.start()
        rec: dict[str, Any] = {"end_seq": (s.seq0 + idx // FRAME) & 0xFFFF, "end_off": idx % FRAME}
        if labels:
            clip, speech_spans = labels[i % len(labels)]
            rec |= {"clip": clip, "speech": [[a + start, b + start] for a, b in speech_spans]}
        last.append(rec)
    tick0 = CLOCK.now() + PTIME_NS  # as `Session.start` schedules it
    hangup_ns = tick0 + len(frames) * PTIME_NS
    starts = [tick0 + start * SAMPLE_NS for start, _ in spans]
    # an agent that has not sent a packet by the end of the first turn's reply time never will
    silent_ns = tick0 + (spans[0][1] if spans else 0) * SAMPLE_NS + REPLY_TIMEOUT_NS
    announce = Turns(len(spans))
    heard = threading.Event()

    def until(now: int) -> bool:
        announce(bisect.bisect_right(starts, now))
        return (not heard.is_set() and now >= silent_ns) or now >= hangup_ns

    remote_bye = s.run(
        lambda n, _t: frames[n] if n < len(frames) else silence, lambda _a, _p: heard.set(), until
    )
    if not heard.is_set():  # by the deadline, or the agent hung up first
        raise s.no_media((CLOCK.now() - tick0) / 1e9)
    return s.meta(seed, remote_bye) | {"turns": last}


class Turns:
    """Prints "turn k/n" as turn k starts, for the host's progress. Called from the SIP loop
    that waits for the call to end, so off the threads that send and receive RTP."""

    def __init__(self, n: int) -> None:
        self.n, self.k = n, 0

    def __call__(self, k: int) -> None:
        if k > self.k:
            self.k = k
            print(f"turn {k}/{self.n}", flush=True)


class Media:
    """Caller audio as an RTP source, one clip at a time, and the agent's audio as a sink: when
    the gate last heard the agent, and each packet's first active sample."""

    def __init__(self, pt: int) -> None:
        self.pt = pt
        self.gate = g711.gate(pt, GATE)
        self.silence = bytes([g711.SILENCE[pt]]) * FRAME
        self.lock = threading.Lock()
        self.audio, self.apos = b"", 0
        self.agent_last = 0

    def on_packet(self, arrival: int, pkt: Packet) -> None:
        if pkt.pt != self.pt or not (first := self.gate.search(pkt.payload)):
            return
        last = self.gate.search(pkt.payload[::-1])
        assert last is not None
        with self.lock:
            end = arrival + (len(pkt.payload) - 1 - last.start()) * SAMPLE_NS
            self.heard(arrival + first.start() * SAMPLE_NS, end)
            self.agent_last = max(self.agent_last, end)

    def recodec(self, pt: int) -> None:
        """Speak and listen in another G.711 law from now on (a codec change)."""
        with self.lock:
            self.pt, self.gate = pt, g711.gate(pt, GATE)
            self.silence = bytes([g711.SILENCE[pt]]) * FRAME

    def heard(self, onset: int, end: int) -> None:
        """A packet with agent speech from `onset` to `end` arrived (under the lock)."""

    def step(self, n: int, tick: int) -> None:
        """Nothing is playing at tick n: start a clip with `play`, or not (under the lock)."""

    def finished(self, tick: int) -> None:
        """The clip just ended (under the lock)."""

    def idle(self, n: int) -> bytes | Frame | None:
        """Tick n's payload when no clip plays: silence, None to send nothing, or a frame of
        another payload type (under the lock)."""
        return self.silence

    def play(self, n: int, clip: tuple[str, bytes, list[tuple[int, int]]]) -> dict[str, Any]:
        """Start `clip` (name, encoded audio, labelled spans) at tick n; its spans in the stream."""
        name, audio, spans = clip
        self.audio, self.apos = audio, 0
        start = n * FRAME
        return {"clip": name, "speech": [[a + start, b + start] for a, b in spans]}

    def source(self, n: int, tick: int) -> bytes | Frame | None:
        with self.lock:
            if not self.audio:
                self.step(n, tick)
            if not self.audio:
                return self.idle(n)
            out = self.audio[self.apos : self.apos + FRAME].ljust(FRAME, self.silence[:1])
            self.apos += FRAME
            if self.apos >= len(self.audio):
                self.audio = b""
                self.finished(tick)
            return out


class Conversation(Media):
    """Barge-in script as an RTP source: each turn a prompt, then, once the agent's reply has
    started, an interjection `at_s` later, then quiet before the next prompt."""

    def __init__(
        self,
        pt: int,
        script: list[tuple[Labelled, Labelled, dict[str, Any]]],
        lead_ns: int,
    ) -> None:
        super().__init__(pt)
        self.script = [
            ((pn, g711.encode(pt, p), ps), (jn, g711.encode(pt, j), js), st)
            for (pn, p, ps), (jn, j, js), st in script
        ]
        self.lead_ns = lead_ns
        self.turns: list[dict[str, Any]] = []
        self.state, self.turn = "lead", 0
        self.t0: int | None = None
        self.since = 0  # when the current state began
        self.wait_until = 0
        self.onset: int | None = None  # first agent sample heard after the prompt
        self.done = False

    def heard(self, onset: int, end: int) -> None:
        if self.state == "reply" and self.onset is None and onset > self.since:
            self.onset = onset

    def finished(self, tick: int) -> None:
        self.state = "reply" if self.state == "prompt" else "quiet"
        self.since, self.onset = tick, None

    def step(self, n: int, tick: int) -> None:
        if self.t0 is None:
            self.t0 = tick
        if self.done:  # the sender keeps ticking until the call notices
            return
        _, interjection, step = self.script[self.turn]
        if self.state == "lead" and tick - self.t0 >= self.lead_ns:
            self._prompt(n, tick)
        elif self.state == "reply" and self.onset is not None:
            self.state, self.wait_until = "barge", self.onset + round(step["at_s"] * 1e9)
        elif self.state == "reply" and tick - self.since > REPLY_TIMEOUT_NS:
            self.state, self.since = "quiet", tick
        elif self.state == "barge" and tick >= self.wait_until:
            self.turns[-1] |= {"kind": step["kind"], "at_s": step["at_s"]} | self.play(
                n, interjection
            )
            self.state = "interject"
        elif self.state == "quiet" and (
            tick - max(self.agent_last, self.since) >= QUIET_NS
            or tick - self.turns[-1]["tick_ns"] > TURN_TIMEOUT_NS
        ):
            self.turn += 1
            if self.turn == len(self.script):
                self.done = True
            else:
                self._prompt(n, tick)

    def _prompt(self, n: int, tick: int) -> None:
        prompt, _, step = self.script[self.turn]
        rec = self.play(n, prompt)
        self.turns.append(
            {
                "prompt": rec["clip"],
                "prompt_speech": rec["speech"],
                "kind": step["kind"],
                "tick_ns": tick,
            }
        )
        self.state = "prompt"


def converse(
    uri: str,
    turns: int = 20,
    seed: int = 1,
    prompts: list[Clip] | None = None,
    lead: float = LEAD_SECONDS,
    codecs: tuple[int, ...] = (g711.PCMU, g711.PCMA),
    interrupts: list[Clip] | None = None,
) -> dict[str, Any]:
    """Barge-in call: `turns` prompts (corpus clips by default), each followed by the planned
    interjection (`interrupts` replace the corpus interruptions). Each turn logs the
    interjection's labelled spans as stream sample indices."""
    prompts = prompts or speech_utterances(seed)
    pool = interjections(seed)
    if interrupts:
        pool["interrupt"] = interrupts
    used = dict.fromkeys(pool, 0)
    labels: dict[str, list[tuple[int, int]]] = {}

    def labelled(clip: Clip) -> Labelled:
        if clip[0] not in labels:
            labels[clip[0]] = speech.label(clip[1])
        return clip[0], clip[1], labels[clip[0]]

    lines = []
    for i, step in enumerate(bargein.plan(seed, turns)):
        clips = pool[step["kind"]]
        said = clips[used[step["kind"]] % len(clips)]
        lines.append((labelled(prompts[i % len(prompts)]), labelled(said), step))
        used[step["kind"]] += 1
    s = Session(uri, codecs)
    s.answer()
    conv = Conversation(s.pt, lines, round(lead * 1e9))
    announce = Turns(turns)
    # as in `call`: no packet by the end of the first prompt's reply time, none at all
    t0 = CLOCK.now() + PTIME_NS
    silent_ns = t0 + round(lead * 1e9) + len(lines[0][0][1]) * SAMPLE_NS + REPLY_TIMEOUT_NS
    heard = threading.Event()

    def until(now: int) -> bool:
        announce(len(conv.turns))
        return (not heard.is_set() and now >= silent_ns) or conv.done

    def sink(arrival: int, pkt: Packet) -> None:
        heard.set()
        conv.on_packet(arrival, pkt)

    remote_bye = s.run(conv.source, sink, until)
    if not heard.is_set():  # by the deadline, or the agent hung up first
        raise s.no_media((CLOCK.now() - t0) / 1e9)
    return s.meta(seed, remote_bye) | {"turns": conv.turns}
