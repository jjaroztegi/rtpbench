"""Reference agent: answers each caller turn a known delay after the caller stops talking.

The delay runs from the last active sample it received (kernel arrival time plus the sample's
offset in its packet) to the reply's onset (tick time plus offset), so the onset is placed to
the sample, not to the packet. The synthetic reply's onset is its sample 0; a speech clip's is
its first labelled speech sample, and whatever precedes it in the clip is sent before it.

With a barge-in plan, caller speech that starts while the agent is replying is an interjection,
never a turn: the agent stops (hard cut) the planned delay after the interjection's first
active sample arrived, or carries on, as the plan says.

In a conformance case the agent answers no turns; it does what the case's `Behaviour` says.
"""

import random
import re
import secrets
import select
import socket
import ssl
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rtpbench import bargein, g711, sip, speech, srtp
from rtpbench.clock import CLOCK
from rtpbench.rtp import FRAME, PTIME_NS, SAMPLE_NS, Frame, Packet, Receiver, Sender
from rtpbench.voice import GATE, voice

HANGOVER_NS = 200_000_000  # silence that ends a caller turn
DELAY_RANGE = (0.3, 1.3)  # seconds; the low end leaves 100 ms after the hangover to schedule
RESPONSE_SECONDS = 0.8
# Real speech pauses for up to 0.8 s inside a turn as the gate sees it, and clips lead in by up
# to 0.35 s before their labelled onset.
SPEECH_HANGOVER_NS = 1_000_000_000
SPEECH_DELAY_RANGE = (1.5, 2.5)

Reply = tuple[str, list[int], list[tuple[int, int]]]  # name, PCM, labelled speech spans
DIGITS = "0123456789*#ABCD"  # RFC 4733 events 0-15
EVENT_END_NS = 3 * PTIME_NS  # no packet of an event this long: it ended (RFC 4733 2.5.2.2)
# where transfers go: the `operator` service, which answers (after ringing, and says a few words)
# unless the INVITE carries the BUSY header, which the transferee adds for a transfer meant to fail
OPERATOR = "sip:operator@operator"
BUSY = ("X-Operator", "busy")


@dataclass(frozen=True)
class Behaviour:
    """What the reference agent does in a conformance case (see `cases`)."""

    ring_s: float = 0.0  # send 180 Ringing and answer this long after the INVITE
    cancel: bool = True  # a CANCEL while ringing ends the call (487); else answer anyway
    greet_s: float | None = None  # greet this long after sending the 200 OK
    greeting: str = "short"  # a short corpus clip, or a long one (9-15 s)
    linger_s: float = 0.0  # keep sending RTP this long after answering BYE
    hold: bool = True  # answer a re-INVITE's direction as offered; else sendrecv, never pause
    clock: bool = True  # RTP timestamps keep time while paused; else resume where they stopped
    dtmf_s: float | None = None  # answer a digit (RFC 4733 or INFO) with speech this long after
    refer_s: float | None = None  # blind REFER this long after the caller's first turn ends
    # then: "complete" answers NOTIFYs and hangs up after a final one reporting 2xx; "always"
    # hangs up after the final one whatever it reports; "stay" answers them and stays; "early"
    # hangs up on the 202 and answers NOTIFYs 481
    transfer: str = "complete"
    retake_s: float | None = None  # a transfer failed (final NOTIFY not 2xx): speak this long after
    codec: int | None = None  # answer with this payload type whatever the offer
    timer: bool = False  # take session timers (RFC 4028) with the caller as refresher
    expire: bool = True  # with timer: BYE when the session expires unrefreshed
    reply_s: float | None = None  # answer the caller's first turn with speech this long after
    # what a carrier may send (see `cases`); each False is a way real agents fail it
    compact: bool = True  # compact header names (RFC 3261 7.3.3); else 500 to an INVITE with them
    lenient_sdp: bool = True  # ignore `a=ssrc:<id>` without an attribute; else 488
    late_offer: bool = True  # offer in the 2xx to an INVITE without SDP; else 488
    any_ptime: bool = True  # hear audio packets of any length; else 20 ms ones only
    any_ssrc: bool = True  # hear the caller from any SSRC; else from the first one only
    refresh: bool = True  # keep sending after a re-INVITE; else stop (one-way audio)
    zero_hold: bool = True  # an offer with c=0.0.0.0 holds (RFC 3264 8.4); else keep sending
    reoffer: bool = True  # offer in the 2xx to a re-INVITE without SDP; else a 2xx without SDP
    recodec: bool = True  # take a re-INVITE's other G.711 law; else answer the old one (stale)
    tcp: bool = True  # listen on TCP too (RFC 3261 18: every element MUST); else UDP only
    busy: bool = False  # 486 Busy Here to the INVITE (the operator of a failed transfer)
    # resend our own requests (REFER, BYE) until answered (timer E, RFC 3261 17.1.2.2); else once
    retransmit: bool = True


def speech_replies(seed: int, directory: Path | None = None, long: bool = False) -> list[Reply]:
    """Every WAV in `directory`, or the short corpus replies (`long`: barge-in ones), shuffled."""
    if directory:
        clips = [(p.stem, speech.read_wav(p)) for p in sorted(directory.glob("*.wav"))]
    else:
        corpus = speech.clips("tts-", "human-").items()
        clips = [(n, pcm) for n, pcm in corpus if ("-long" in n) == long]
    random.Random(seed).shuffle(clips)
    return [(n, pcm, speech.label(pcm)) for n, pcm in clips]


class Responder:
    def __init__(
        self,
        pt: int,
        seq0: int,
        delays: list[float],
        replies: list[Reply] | None = None,
        hangover_ns: int = HANGOVER_NS,
        plan: list[dict[str, Any]] | None = None,
    ) -> None:
        self.pt, self.seq0, self.delays, self.hangover_ns = pt, seq0, delays, hangover_ns
        self.plan = plan
        self.gate = g711.gate(pt, GATE)
        self.silence = bytes([g711.SILENCE[pt]]) * FRAME
        replies = replies or [("synthetic", voice(RESPONSE_SECONDS, f0=210), [])]
        self.replies = [(n, g711.encode(pt, pcm), spans) for n, pcm, spans in replies]
        self.response = b""
        self.lock = threading.Lock()
        self.turns: list[dict[str, Any]] = []
        self.speaking = False
        self.end_ns, self.end_seq, self.end_off = 0, 0, 0
        self.pending: dict[str, Any] | None = None
        self.pos: int | None = None  # response sample index at the start of the next tick
        self.current: dict[str, Any] = {}  # the turn being replied to
        self.interjecting = False  # the caller's current burst started while we replied
        self.cut_ns: int | None = None
        self.sending, self.clock = True, True  # not sending: on hold
        self.skipped, self.paused = 0, True  # ticks not sent; marker on the next packet
        self.events: int | None = None  # telephone-event payload type
        self.dtmf_ns: int | None = None  # reply this long after a digit
        self.digits: list[dict[str, Any]] = []
        self.event_ts: int | None = None  # RTP timestamp of the last event that ended
        self.event_open: tuple[int, int, str] | None = None  # ts, last arrival, digit: no end yet
        self.ends: list[int] = []  # caller turn ends, when answering no turns

    def speak(self, target_ns: int, reply: int, kind: str) -> None:
        """Say `self.replies[reply]`, its labelled onset at `target_ns`."""
        with self.lock:
            turn = len(self.turns)
            self.pending = {"turn": turn, "kind": kind, "reply": reply, "target_ns": target_ns}

    def recodec(self, pt: int) -> None:
        """Speak and hear the other G.711 law from now on (the caller changed codec)."""
        replies = [(n, g711.encode(pt, g711.decode(self.pt, a)), s) for n, a, s in self.replies]
        with self.lock:
            self.response = g711.encode(pt, g711.decode(self.pt, self.response))
            self.pt, self.replies, self.gate = pt, replies, g711.gate(pt, GATE)
            self.silence = bytes([g711.SILENCE[pt]]) * FRAME

    def digit(self, at_ns: int, digit: str, via: str) -> None:
        """A digit came in (the key released): note it and, if the case says so, answer."""
        self.digits.append({"digit": digit, "via": via, "at_ns": at_ns})
        if self.dtmf_ns is not None:
            reply = len(self.digits) % len(self.replies)
            self.speak(at_ns + self.dtmf_ns, reply, "dtmf")

    def on_packet(self, arrival: int, pkt: Packet) -> None:
        if pkt.pt == self.events and len(pkt.payload) >= 4:
            if pkt.ts == self.event_ts:  # an event already taken
                return
            if pkt.payload[1] & 0x80:  # end bit, first copy
                self.event_ts, self.event_open = pkt.ts, None
                self.digit(arrival, DIGITS[pkt.payload[0] % 16], "rfc4733")
            else:
                self.event_open = (pkt.ts, arrival, DIGITS[pkt.payload[0] % 16])
            return
        if pkt.pt != self.pt:
            return
        with self.lock:
            if m := self.gate.search(pkt.payload[::-1]):
                if not self.speaking and self.plan is not None:
                    self.interjecting = self.pos is not None
                    if self.interjecting and "barge" not in self.current:
                        self._interjection(arrival, pkt)
                off = len(pkt.payload) - 1 - m.start()
                if (end := arrival + off * SAMPLE_NS) > self.end_ns:
                    self.end_ns, self.end_seq, self.end_off = end, pkt.seq, off
                self.speaking = True
            elif self.speaking and arrival - self.end_ns >= self.hangover_ns:
                self.speaking = False
                if self.interjecting or not self.delays:
                    if not self.interjecting:
                        self.ends.append(self.end_ns)
                    self.interjecting = False
                    return
                turn = len(self.turns) + (self.pending is not None)
                delay_ns = round(self.delays[turn % len(self.delays)] * 1e9)
                self.pending = {
                    "turn": turn,
                    "delay_ns": delay_ns,
                    "end_ns": self.end_ns,
                    "end_seq": self.end_seq,
                    "end_off": self.end_off,
                    "target_ns": self.end_ns + delay_ns,
                }

    def _interjection(self, arrival: int, pkt: Packet) -> None:
        assert self.plan is not None
        first = self.gate.search(pkt.payload)
        assert first is not None
        step = self.plan[self.current["turn"] % len(self.plan)]
        trigger = arrival + first.start() * SAMPLE_NS
        delay_ns = round(step["stop_delay_s"] * 1e9)
        self.current["barge"] = {
            "trigger_ns": trigger,
            "trigger_seq": pkt.seq,
            "trigger_off": first.start(),
            "stop_delay_ns": delay_ns,
        }
        if step["stop"]:
            self.cut_ns = trigger + delay_ns

    def source(self, n: int, tick: int) -> bytes | Frame | None:
        # an event whose end packets were all lost still happened: RFC 4733 2.5.2.2 ends it once
        # packets stop (and extends a tone by no more than three packet interarrival times)
        if (e := self.event_open) is not None and tick - e[1] > EVENT_END_NS:
            self.event_ts, self.event_open = e[0], None
            self.digit(e[1] + EVENT_END_NS, e[2], "rfc4733")
        with self.lock:
            out = self._audio(n - self.skipped, tick)
            if not self.sending:
                self.skipped += 1
                self.paused = True
                return None
            marker, self.paused = self.paused, False
            if self.clock:
                return out  # timestamp n * 160: the clock ran on while paused
            return Frame(self.pt, out, (n - self.skipped) * FRAME, marker)

    def _audio(self, n: int, tick: int) -> bytes:
        """Tick n's payload (under the lock); n counts packets sent, as seq does."""
        p = self.pending
        pick = p.get("reply", p["turn"]) if p else 0
        name, audio, spans = self.replies[pick % len(self.replies)] if p else ("", b"", [])
        lead = spans[0][0] if spans else 0
        # a start in the last half sample rounds to the next tick's sample 0, not to 160
        off = round((p["target_ns"] - tick) / SAMPLE_NS) - lead if p else FRAME
        if self.pos is None and p is not None and off < FRAME:
            off = max(0, off)
            start = n * FRAME + off  # stream sample index (from seq0) of the clip's sample 0
            onset = start + lead
            p |= {
                "onset_seq": (self.seq0 + onset // FRAME) & 0xFFFF,
                "onset_off": onset % FRAME,
                "tick_ns": tick,
            }
            if spans:
                p |= {
                    "clip": name,
                    "start": start,
                    "speech": [[a + start, b + start] for a, b in spans],
                }
            self.turns.append(p)
            self.pending, self.pos, self.response, self.current = None, -off, audio, p
        if self.pos is None:
            return self.silence
        pos, self.pos = self.pos, self.pos + FRAME
        if self.pos >= len(self.response):
            self.pos = None
        head = self.silence[: max(0, -pos)]
        out = (head + self.response[max(0, pos) : pos + FRAME]).ljust(FRAME, self.silence[:1])
        if self.cut_ns is not None and (cut := round((self.cut_ns - tick) / SAMPLE_NS)) < FRAME:
            cut = max(0, cut)
            self.current["barge"]["cut"] = n * FRAME + cut  # first sample not sent
            self.pos = None
            out = out[:cut] + self.silence[cut:]
        if self.pos is None:
            self.cut_ns = None
        return out


def _savp(sdp: sip.Sdp) -> bool:
    return sdp.proto == "RTP/SAVP"


def _usable(sdp: sip.Sdp) -> list[tuple[int, str, bytes]]:
    """The a=crypto lines of `sdp` this agent can take, in the offer's order."""
    out = []
    for value in sdp.crypto:
        try:
            out.append(srtp.parse(value))
        except ValueError:
            continue
    return out


def _local_ip(peer: tuple[str, int]) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(peer)
        return str(s.getsockname()[0])


class Uas:
    """The reference agent's SIP side of one call: answers (after ringing, if the case says so),
    resends its final response to the INVITE until ACKed, and takes CANCEL and BYE as the case
    says. `sock`: the transport the INVITE came on (a UDP socket or `sip.Tcp`)."""

    def __init__(
        self,
        sock: socket.socket | sip.Tcp,
        rtp: socket.socket,
        case: Behaviour,
        responder: Callable[[int, int], Responder],
        greeting: int,
    ) -> None:
        self.sock, self.rtp, self.case = sock, rtp, case
        self.make, self.greeting = responder, greeting
        self.to_tag = secrets.token_hex(4)
        self.invite: sip.Message | None = None
        self.addr = ("", 0)
        self.last = b""  # latest response to the INVITE, resent if the INVITE is
        self.unacked = b""  # final response to the INVITE, resent until ACKed
        self.resend_at, self.interval = 0.0, sip.T1
        self.answer_at: float | None = None
        self.reinvite = ""  # branch of the latest re-INVITE
        self.origin = [secrets.randbelow(1 << 31), 0]  # SDP session id, version
        self.end_at: float | None = None
        self.done = False
        self.responder: Responder | None = None
        self.pt, self.dtmf = 0, False
        self.late = False  # the INVITE had no offer: ours goes in the 2xx, theirs in the ACK
        self.seq0 = 0
        self.heard_ssrc: int | None = None
        self.replied = False
        self.dialog: sip.Dialog | None = None  # for requests of our own (REFER, BYE)
        self.refer: sip.Message | None = None
        self.bye: sip.Message | None = None
        self.expire_at: float | None = None  # session timer: BYE then, unless refreshed
        self.sender: Sender | None = None
        self.threads: list[Sender | Receiver] = []
        self.meta: dict[str, Any] = {}
        # SRTP when the caller offers it (SDES): our master key per suite; the suite we took,
        # what we send with and what we hear with
        self.keys = srtp.master()
        self.suite: str | None = None
        self.tx: srtp.Context | None = None
        self.rx: srtp.Context | None = None

    def _send(self, resp: sip.Message, final: bool = False) -> None:
        data = resp.render()
        self.sock.sendto(data, self.addr)
        if resp.cseq_method == "INVITE":
            self.last = data
            if final:
                self.unacked, self.resend_at, self.interval = (
                    data,
                    time.monotonic() + sip.T1,
                    sip.T1,
                )

    def handle(
        self, msg: sip.Message, addr: tuple[str, int], via: socket.socket | sip.Tcp | None = None
    ) -> None:
        """A message from `addr`, on `via` (the call's transport if None)."""
        inv = self.invite
        if msg.status:
            self._response(msg)
            return
        if inv is None and msg.method == "INVITE":
            self.addr, self.sock = addr, via or self.sock
            self._invite(msg)
        elif inv is None or msg.get("call-id") != inv.get("call-id"):
            if msg.method not in ("ACK", "INVITE"):
                self.sock.sendto(sip.response(msg, 481, "Call Does Not Exist").render(), addr)
        elif msg.method == "INVITE" and msg.branch in (inv.branch, self.reinvite):
            self.sock.sendto(self.last, addr)  # retransmission
        elif msg.method == "INVITE":
            self._reinvite(msg)
        elif msg.method == "ACK":
            self.unacked = b""
            if self.late and self.sender is None and self.dialog and msg.body:
                answer = sip.parse_sdp(msg.body)
                if (pt := next((p for p in answer.pts if p in g711.NAMES), self.pt)) != self.pt:
                    self.pt = pt
                    self._prepare(answer)
                self._media(answer)
            elif msg.body and self.suite:  # the answer to our offer in a 2xx: the caller's key
                self._crypto(sip.parse_sdp(msg.body))
            self.done |= self.responder is None  # ACK for a 487: the call never was
        elif msg.method == "CANCEL":
            self._send(sip.response(msg, 200, "OK", self.to_tag))
            if self.answer_at is not None and self.case.cancel:  # still ringing
                self.answer_at = None
                self._send(sip.response(inv, 487, "Request Terminated", self.to_tag), final=True)
                self.end_at = time.monotonic() + 64 * sip.T1
        elif msg.method == "BYE":
            self._send(sip.response(msg, 200, "OK", self.to_tag))
            self.end_at = time.monotonic() + self.case.linger_s
        elif msg.method == "NOTIFY":
            if self.case.transfer == "early":
                self._send(sip.response(msg, 481, "Subscription Does Not Exist", self.to_tag))
                return
            self._send(sip.response(msg, 200, "OK", self.to_tag))
            final = "terminated" in msg.get("subscription-state")
            ok = msg.body[8:9] == b"2"  # sipfrag "SIP/2.0 2xx"
            if final and (
                self.case.transfer == "always" or (ok and self.case.transfer == "complete")
            ):
                self._hang_up()
            elif final and not ok and self.case.retake_s is not None and (r := self.responder):
                retake = round(self.case.retake_s * 1e9)
                r.speak(CLOCK.now() + retake, (self.greeting + 1) % len(r.replies), "retake")
        elif msg.method == "INFO" and "dtmf-relay" in msg.get("content-type").lower():
            self._send(sip.response(msg, 200, "OK", self.to_tag))
            body = dict(
                line.partition("=")[::2] for line in msg.body.decode(errors="replace").split()
            )
            if self.responder and (signal := body.get("Signal", "").strip()):
                self.responder.digit(CLOCK.now(), signal, "info")
        else:
            self._send(sip.response(msg, 200, "OK", self.to_tag))

    def _response(self, msg: sip.Message) -> None:
        if self.dialog is None:
            return
        self.dialog.answered(msg)
        taken = self.refer is not None and msg.branch == self.refer.branch and msg.status == 202
        if self.bye and msg.branch == self.bye.branch and msg.status >= 200:
            self.end_at = time.monotonic() + (5.0 if self.case.transfer == "early" else 0.0)
        elif taken and self.case.transfer == "early":  # blind: done once the REFER is taken
            self._hang_up()

    def _hang_up(self) -> None:
        assert self.dialog is not None
        if self.bye is None:
            self.bye = self.dialog.request("BYE")
            self.dialog.send(self.bye)

    def _invite(self, msg: sip.Message) -> None:
        self.invite = msg
        self._send(sip.response(msg, 100, "Trying"))
        self.late = not msg.body and self.case.late_offer
        compact = any(k.lower() in sip._COMPACT for k, _ in msg.headers)
        malformed = re.search(rb"^a=ssrc:\d+\r?$", msg.body, re.MULTILINE)
        if self.case.busy:
            self._send(sip.response(msg, 486, "Busy Here", self.to_tag), final=True)
            self.end_at = time.monotonic() + 64 * sip.T1
        elif compact and not self.case.compact:  # a parser that knows the long names only
            self._send(sip.response(msg, 500, "Server Internal Error", self.to_tag), final=True)
            self.end_at = time.monotonic() + 64 * sip.T1
        elif not self.late and (
            (malformed and not self.case.lenient_sdp)
            or not [pt for pt in sip.parse_sdp(msg.body).pts if pt in g711.NAMES]
            or (_savp(sip.parse_sdp(msg.body)) and not _usable(sip.parse_sdp(msg.body)))
        ):
            self._send(sip.response(msg, 488, "Not Acceptable Here", self.to_tag), final=True)
            self.end_at = time.monotonic() + 64 * sip.T1
        elif self.case.ring_s:
            self._send(sip.response(msg, 180, "Ringing", self.to_tag))
            self.answer_at = time.monotonic() + self.case.ring_s
        else:
            self._answer()

    def _answer(self) -> None:
        """Answer with the session (or, to an INVITE without one, an offer of both laws, the
        media starting on the ACK's answer)."""
        assert self.invite is not None
        offer = sip.parse_sdp(self.invite.body)
        pt = next((pt for pt in offer.pts if pt in g711.NAMES), g711.PCMU)
        self.pt = pt if self.case.codec is None else self.case.codec
        self.dtmf = offer.dtmf is not None
        self._prepare(offer)  # before the 2xx: it takes a while (encodes every clip)
        self._send(self._ok(self.invite, "sendrecv"), final=True)
        self.dialog = sip.Dialog.uas(
            self.sock, self.addr, self.invite, _local_ip(self.addr), self.to_tag
        )
        if not self.late:
            self._media(offer)

    def _prepare(self, remote: sip.Sdp) -> None:
        self.seq0 = secrets.randbelow(1 << 16)
        self.responder = r = self.make(self.pt, self.seq0)
        r.clock, r.events = self.case.clock, remote.dtmf
        r.dtmf_ns = None if self.case.dtmf_s is None else round(self.case.dtmf_s * 1e9)

    def _crypto(self, offer: sip.Sdp | None) -> list[str] | None:
        """a=crypto values for our SDP: the answer to an SRTP `offer` (its first suite we take,
        or the one in use), our offer of the suite in use when there is no offer, else none."""
        if offer is None:
            return [srtp.line(1, self.suite, self.keys[self.suite])] if self.suite else None
        if not _savp(offer):
            return None
        # the suite stays the call's: a re-INVITE without it is refused (`_reinvite`)
        pick = next((c for c in _usable(offer) if c[1] == (self.suite or c[1])), None)
        if pick is None:
            return None
        tag, suite, key = pick
        if self.tx is None:
            self.suite, self.tx = suite, srtp.Context(suite, self.keys[suite])
        if self.rx is None or self.rx.master != key:
            self.rx = srtp.Context(suite, key, self.rx.state if self.rx else None)
            for t in self.threads:
                if isinstance(t, Receiver):
                    t.srtp = self.rx
        return [srtp.line(tag, suite, self.keys[suite])]

    def _media(self, remote: sip.Sdp) -> None:
        """Start sending to and hearing the far end of the negotiated session."""
        r = self.responder
        assert r is not None
        ssrc = secrets.randbelow(1 << 32)
        start = CLOCK.now() + PTIME_NS
        addr = (remote.ip, remote.port)
        self.sender = Sender(
            self.rtp, addr, self.pt, r.source, start, self.seq0, ssrc, srtp=self.tx
        )
        self.threads = [self.sender, Receiver(self.rtp, self._hear, srtp=self.rx)]
        for t in self.threads:
            t.start()
        if self.case.greet_s is not None:
            r.speak(CLOCK.now() + round(self.case.greet_s * 1e9), self.greeting, "greeting")
        self.meta = {"pt": self.pt, "ssrc": ssrc, "seq0": self.seq0, "srtp": self.suite}

    def _hear(self, arrival: int, pkt: Packet) -> None:
        """The caller's RTP, as far as this agent's receiver takes it."""
        if pkt.pt == self.pt and len(pkt.payload) != FRAME and not self.case.any_ptime:
            return
        self.heard_ssrc = pkt.ssrc if self.heard_ssrc is None else self.heard_ssrc
        if pkt.ssrc != self.heard_ssrc and not self.case.any_ssrc:
            return
        assert self.responder is not None
        self.responder.on_packet(arrival, pkt)

    def _ok(self, req: sip.Message, direction: str) -> sip.Message:
        local = _local_ip(self.addr)
        assert self.invite is not None
        transport = getattr(self.sock, "transport", "UDP")
        sips = self.invite.first.split()[1].lower().startswith("sips:")
        contact = sip.contact("agent", local, self.sock.getsockname()[1], transport, sips)
        extra = [("Contact", contact)]
        origin = (self.origin[0], self.origin[1])
        pts = list(g711.NAMES) if self.late and self.sender is None else [self.pt]
        crypto = self._crypto(sip.parse_sdp(req.body) if req.body else None)
        body = sip.sdp(
            local, self.rtp.getsockname()[1], pts, direction, origin, self.dtmf, crypto=crypto
        )
        self.origin[1] += 1
        if self.case.timer and (expires := req.get("session-expires")):
            # RFC 4028 9: keep the interval and the caller as refresher, so Require: timer
            interval = int(expires.split(";")[0])
            extra += [("Require", "timer"), ("Supported", "timer")]
            extra.append(("Session-Expires", f"{interval};refresher=uac"))
            if self.case.expire:  # 10: BYE min(32 s, a third) before it would expire
                self.expire_at = time.monotonic() + interval - min(32, interval / 3)
        return sip.response(req, 200, "OK", self.to_tag, body, extra)

    def _reinvite(self, msg: sip.Message) -> None:
        """Answer the offered direction (or sendrecv, ignoring hold); pause sending while the
        answer says the agent does not send."""
        offer = sip.parse_sdp(msg.body)
        self.reinvite = msg.branch  # a retransmission gets the same answer
        if self.suite and _savp(offer) and all(c[1] != self.suite for c in _usable(offer)):
            self._send(sip.response(msg, 488, "Not Acceptable Here", self.to_tag), final=True)
            return
        direction = sip.ANSWER[offer.direction] if self.case.hold else "sendrecv"
        zero = offer.ip == "0.0.0.0"  # RFC 3264 8.4: send nothing
        law = next((pt for pt in offer.pts if pt in g711.NAMES), self.pt)
        if self.responder:
            if law != self.pt and self.case.recodec:
                self.pt = law
                self.responder.recodec(law)
                if self.sender:
                    self.sender.pt = law
            with self.responder.lock:
                sending = direction in ("sendrecv", "sendonly") and self.case.refresh
                self.responder.sending = sending and not (zero and self.case.zero_hold)
            if offer.port and self.sender and not zero:
                self.sender.addr = (offer.ip, offer.port)
        ok = self._ok(msg, direction)
        if not msg.body and not self.case.reoffer:
            ok.body, ok.headers = b"", [h for h in ok.headers if h[0] != "Content-Type"]
        self._send(ok, final=True)

    def tick(self) -> None:
        now = time.monotonic()
        if self.dialog and self.case.retransmit:
            self.dialog.retransmit()
        if self.refer is None and self._since_turn(self.case.refer_s):
            self._transfer()
        if self.case.reply_s is not None and not self.replied and (r := self.responder) and r.ends:
            self.replied = True
            r.speak(r.ends[0] + round(self.case.reply_s * 1e9), self.greeting + 1, "reply")
        if self.expire_at is not None and now >= self.expire_at:
            self.expire_at = None
            self._hang_up()
        if self.answer_at is not None and now >= self.answer_at:
            self.answer_at = None
            self._answer()
        if self.unacked and now >= self.resend_at:
            self.sock.sendto(self.unacked, self.addr)
            self.interval = min(self.interval * 2, sip.T2)
            self.resend_at = now + self.interval
        if self.end_at is not None and now >= self.end_at:
            self.done = True

    def _since_turn(self, seconds: float | None) -> bool:
        """The caller's first turn ended at least `seconds` ago."""
        r = self.responder
        if r is None or not r.ends or seconds is None:
            return False
        return CLOCK.now() >= r.ends[0] + seconds * 1e9

    def _transfer(self) -> None:
        """Blind transfer (RFC 5589): REFER the caller to an operator."""
        assert self.dialog is not None
        local = self.dialog.local_ip
        headers = [("Refer-To", f"<{OPERATOR}>"), ("Referred-By", f"<sip:agent@{local}>")]
        self.refer = self.dialog.request("REFER", headers=headers)
        self.dialog.send(self.refer)

    def stop(self) -> None:
        for t in self.threads:
            t.stop.set()
        for t in self.threads:
            t.join()


def serve(
    ready: Path,
    sip_port: int = 5060,
    rtp_port: int = 40000,
    seed: int = 1,
    real: bool = False,
    replies: Path | None = None,
    barge: bool = False,
    case: Behaviour | None = None,
    tls: Path | None = None,
) -> dict[str, Any]:
    """Answer one call; return its per-turn ground truth. Touches `ready` once listening.

    `real`: reply with speech (corpus clips, or the WAVs in `replies`), not the synthetic voice.
    `barge`: reply with the long corpus clips and follow the barge-in plan.
    `case`: answer no turns; behave as a conformance case asks (short then long corpus clips).
    `tls`: a directory with server.crt and server.key; SIP over TLS on 5061 too.
    """
    real = real or barge
    rng = random.Random(seed)
    delays = [rng.uniform(*(SPEECH_DELAY_RANGE if real else DELAY_RANGE)) for _ in range(1000)]
    clips = speech_replies(seed, replies, long=barge) if real else None
    greeting = 0
    if case:
        delays, short = [], speech_replies(seed)
        clips, greeting = (
            short + speech_replies(seed, long=True),
            len(short) * (case.greeting == "long"),
        )
    plan = bargein.plan(seed) if barge else None
    # case callers speak real speech too, whose pauses would end a turn mid-sentence
    hangover = SPEECH_HANGOVER_NS if real or case else HANGOVER_NS
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", sip_port))
    streams: list[sip.Tcp] = [sip.Tcp(sip_port)] if (case or Behaviour()).tcp else []
    if tls:
        ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ctx.load_cert_chain(tls / "server.crt", tls / "server.key")
        streams.append(sip.Tls(sip.TLS_PORT, server=ctx))
    rtp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rtp.bind(("0.0.0.0", rtp_port))
    ready.touch()

    def responder(pt: int, seq0: int) -> Responder:
        return Responder(pt, seq0, delays, clips, hangover, plan)

    call = Uas(sock, rtp, case or Behaviour(), responder, greeting)
    sock.settimeout(0)
    for t in streams:
        t.settimeout(0)
    while not call.done:
        ready_socks = select.select(
            [sock, *(s for t in streams for s in t.sockets())], [], [], 0.02
        )
        try:
            if sock in ready_socks[0]:
                data, addr = sock.recvfrom(65535)
                call.handle(sip.parse(data), addr, sock)
        except BlockingIOError:
            pass
        for t in streams:  # each, even unwoken: a message may wait read already
            try:
                data, addr = t.recvfrom()
            except TimeoutError:
                continue
            call.handle(sip.parse(data), addr, t)
        call.tick()
    call.stop()
    r = call.responder
    return call.meta | {
        "seed": seed,
        "turns": r.turns if r else [],
        "digits": r.digits if r else [],
        "send_errors": call.sender.send_errors if call.sender else [],
    }


def operator(ready: Path, sip_port: int = 5060) -> None:
    """The transfer target: takes any number of calls, each on its own RTP socket; rings for a
    second, answers and says a few words, or is busy when the INVITE asks (BUSY). Runs until
    killed; touches `ready` once listening."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", sip_port))
    sock.settimeout(0.02)
    clips = speech_replies(1)[:2]  # encoded per call: a greeting is all it says
    calls: dict[str, Uas] = {}
    ready.touch()
    while True:
        try:
            data, addr = sock.recvfrom(65535)
        except TimeoutError:
            pass
        else:
            msg = sip.parse(data)
            call_id = msg.get("call-id")
            if call_id not in calls and msg.method == "INVITE" and not sip.tag(msg.get("to")):
                busy = msg.get(BUSY[0]).lower() == BUSY[1]
                case = Behaviour(busy=True) if busy else Behaviour(ring_s=1.0, greet_s=0.5)
                rtp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                rtp.bind(("0.0.0.0", 0))
                calls[call_id] = Uas(
                    sock, rtp, case, lambda pt, seq0: Responder(pt, seq0, [], clips), 0
                )
                print(f"operator: {call_id} {'busy' if busy else 'answers'}", flush=True)
            if call := calls.get(call_id):
                call.handle(msg, addr)
            elif msg.method not in ("", "ACK"):
                sock.sendto(sip.response(msg, 481, "Call Does Not Exist").render(), addr)
        for call_id, call in list(calls.items()):
            call.tick()
            if call.done:
                call.stop()
                call.rtp.close()
                del calls[call_id]
