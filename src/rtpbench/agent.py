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
import secrets
import socket
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rtpbench import bargein, g711, sip, speech
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

    def speak(self, target_ns: int, reply: int, kind: str) -> None:
        """Say `self.replies[reply]`, its labelled onset at `target_ns`."""
        with self.lock:
            turn = len(self.turns)
            self.pending = {"turn": turn, "kind": kind, "reply": reply, "target_ns": target_ns}

    def digit(self, at_ns: int, digit: str, via: str) -> None:
        """A digit came in (the key released): note it and, if the case says so, answer."""
        self.digits.append({"digit": digit, "via": via, "at_ns": at_ns})
        if self.dtmf_ns is not None:
            reply = len(self.digits) % len(self.replies)
            self.speak(at_ns + self.dtmf_ns, reply, "dtmf")

    def on_packet(self, arrival: int, pkt: Packet) -> None:
        if pkt.pt == self.events and len(pkt.payload) >= 4:
            if pkt.payload[1] & 0x80 and pkt.ts != self.event_ts:  # end bit, first copy
                self.event_ts = pkt.ts
                self.digit(arrival, DIGITS[pkt.payload[0] % 16], "rfc4733")
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


def _local_ip(peer: tuple[str, int]) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(peer)
        return str(s.getsockname()[0])


class Uas:
    """The reference agent's SIP side of one call: answers (after ringing, if the case says so),
    resends its final response to the INVITE until ACKed, and takes CANCEL and BYE as the case
    says."""

    def __init__(
        self,
        sock: socket.socket,
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
        self.sender: Sender | None = None
        self.threads: list[Sender | Receiver] = []
        self.meta: dict[str, Any] = {}

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

    def handle(self, msg: sip.Message, addr: tuple[str, int]) -> None:
        inv = self.invite
        if msg.status:
            return
        if inv is None and msg.method == "INVITE":
            self.addr = addr
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
        elif msg.method == "INFO" and "dtmf-relay" in msg.get("content-type").lower():
            self._send(sip.response(msg, 200, "OK", self.to_tag))
            body = dict(
                line.partition("=")[::2] for line in msg.body.decode(errors="replace").split()
            )
            if self.responder and (signal := body.get("Signal", "").strip()):
                self.responder.digit(time.time_ns(), signal, "info")
        else:
            self._send(sip.response(msg, 200, "OK", self.to_tag))

    def _invite(self, msg: sip.Message) -> None:
        self.invite = msg
        self._send(sip.response(msg, 100, "Trying"))
        if not [pt for pt in sip.parse_sdp(msg.body).pts if pt in g711.NAMES]:
            self._send(sip.response(msg, 488, "Not Acceptable Here", self.to_tag), final=True)
            self.end_at = time.monotonic() + 64 * sip.T1
        elif self.case.ring_s:
            self._send(sip.response(msg, 180, "Ringing", self.to_tag))
            self.answer_at = time.monotonic() + self.case.ring_s
        else:
            self._answer()

    def _answer(self) -> None:
        assert self.invite is not None
        offer = sip.parse_sdp(self.invite.body)
        self.pt = pt = next(pt for pt in offer.pts if pt in g711.NAMES)
        seq0, ssrc = secrets.randbelow(1 << 16), secrets.randbelow(1 << 32)
        self.responder = r = self.make(pt, seq0)
        r.clock, r.events = self.case.clock, offer.dtmf
        r.dtmf_ns = None if self.case.dtmf_s is None else round(self.case.dtmf_s * 1e9)
        self.dtmf = offer.dtmf is not None
        self._send(self._ok(self.invite, "sendrecv"), final=True)
        start = time.time_ns() + PTIME_NS
        self.sender = Sender(self.rtp, (offer.ip, offer.port), pt, r.source, start, seq0, ssrc)
        self.threads = [self.sender, Receiver(self.rtp, r.on_packet)]
        for t in self.threads:
            t.start()
        if self.case.greet_s is not None:
            r.speak(time.time_ns() + round(self.case.greet_s * 1e9), self.greeting, "greeting")
        self.meta = {"pt": pt, "ssrc": ssrc, "seq0": seq0}

    def _ok(self, req: sip.Message, direction: str) -> sip.Message:
        local = _local_ip(self.addr)
        contact = [("Contact", f"<sip:agent@{local}:{self.sock.getsockname()[1]}>")]
        origin = (self.origin[0], self.origin[1])
        body = sip.sdp(local, self.rtp.getsockname()[1], [self.pt], direction, origin, self.dtmf)
        self.origin[1] += 1
        return sip.response(req, 200, "OK", self.to_tag, body, contact)

    def _reinvite(self, msg: sip.Message) -> None:
        """Answer the offered direction (or sendrecv, ignoring hold); pause sending while the
        answer says the agent does not send."""
        offer = sip.parse_sdp(msg.body)
        direction = sip.ANSWER[offer.direction] if self.case.hold else "sendrecv"
        self.reinvite = msg.branch
        if self.responder:
            with self.responder.lock:
                self.responder.sending = direction in ("sendrecv", "sendonly")
            if offer.port and self.sender:
                self.sender.addr = (offer.ip, offer.port)
        self._send(self._ok(msg, direction), final=True)

    def tick(self) -> None:
        now = time.monotonic()
        if self.answer_at is not None and now >= self.answer_at:
            self.answer_at = None
            self._answer()
        if self.unacked and now >= self.resend_at:
            self.sock.sendto(self.unacked, self.addr)
            self.interval = min(self.interval * 2, sip.T2)
            self.resend_at = now + self.interval
        if self.end_at is not None and now >= self.end_at:
            self.done = True

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
) -> dict[str, Any]:
    """Answer one call; return its per-turn ground truth. Touches `ready` once listening.

    `real`: reply with speech (corpus clips, or the WAVs in `replies`), not the synthetic voice.
    `barge`: reply with the long corpus clips and follow the barge-in plan.
    `case`: answer no turns; behave as a conformance case asks (short then long corpus clips).
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
    hangover = SPEECH_HANGOVER_NS if real else HANGOVER_NS
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", sip_port))
    rtp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rtp.bind(("0.0.0.0", rtp_port))
    ready.touch()

    def responder(pt: int, seq0: int) -> Responder:
        return Responder(pt, seq0, delays, clips, hangover, plan)

    call = Uas(sock, rtp, case or Behaviour(), responder, greeting)
    sock.settimeout(0.02)
    while not call.done:
        try:
            data, addr = sock.recvfrom(65535)
        except TimeoutError:
            pass
        else:
            call.handle(sip.parse(data), addr)
        call.tick()
    call.stop()
    r = call.responder
    return call.meta | {
        "seed": seed,
        "turns": r.turns if r else [],
        "digits": r.digits if r else [],
    }
