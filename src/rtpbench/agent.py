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
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rtpbench import bargein, g711, sip, speech
from rtpbench.rtp import FRAME, PTIME_NS, SAMPLE_NS, Packet, Receiver, Sender
from rtpbench.voice import GATE, voice

HANGOVER_NS = 200_000_000  # silence that ends a caller turn
DELAY_RANGE = (0.3, 1.3)  # seconds; the low end leaves 100 ms after the hangover to schedule
RESPONSE_SECONDS = 0.8
# Real speech pauses for up to 0.8 s inside a turn as the gate sees it, and clips lead in by up
# to 0.35 s before their labelled onset.
SPEECH_HANGOVER_NS = 1_000_000_000
SPEECH_DELAY_RANGE = (1.5, 2.5)

Reply = tuple[str, list[int], list[tuple[int, int]]]  # name, PCM, labelled speech spans


@dataclass(frozen=True)
class Behaviour:
    """What the reference agent does in a conformance case (see `cases`)."""

    greet_s: float | None = None  # greet this long after sending the 200 OK
    greeting: str = "short"  # a short corpus clip, or a long one (9-15 s)


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

    def speak(self, target_ns: int, reply: int, kind: str) -> None:
        """Say `self.replies[reply]`, its labelled onset at `target_ns`."""
        with self.lock:
            turn = len(self.turns)
            self.pending = {"turn": turn, "kind": kind, "reply": reply, "target_ns": target_ns}

    def on_packet(self, arrival: int, pkt: Packet) -> None:
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

    def source(self, n: int, tick: int) -> bytes:
        with self.lock:
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
    if case:
        delays, short = [], speech_replies(seed)
        clips = short + speech_replies(seed, long=True)
    plan = bargein.plan(seed) if barge else None
    hangover = SPEECH_HANGOVER_NS if real else HANGOVER_NS
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", sip_port))
    rtp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rtp.bind(("0.0.0.0", rtp_port))
    ready.touch()
    to_tag, ok, ok_to, acked = secrets.token_hex(4), b"", ("", 0), False
    call_id, resend_at, interval = "", 0.0, sip.T1
    responder: Responder | None = None
    threads: list[Sender | Receiver] = []
    meta: dict[str, Any] = {}
    while True:
        sock.settimeout(0.1)
        try:
            data, addr = sock.recvfrom(65535)
        except TimeoutError:
            if ok and not acked and time.monotonic() >= resend_at:
                sock.sendto(ok, ok_to)
                interval = min(interval * 2, 4.0)
                resend_at = time.monotonic() + interval
            continue
        msg = sip.parse(data)
        if msg.status:
            continue
        if msg.method == "INVITE" and msg.get("call-id") == call_id:
            sock.sendto(ok, addr)  # retransmitted INVITE
        elif msg.method == "INVITE" and not call_id:
            ip, port, pts = sip.parse_sdp(msg.body)
            codecs = [pt for pt in pts if pt in g711.NAMES]
            if not codecs:
                sock.sendto(sip.response(msg, 488, "Not Acceptable Here", to_tag).render(), addr)
                continue
            pt, local = codecs[0], _local_ip(addr)
            call_id = msg.get("call-id")
            seq0, ssrc = secrets.randbelow(1 << 16), secrets.randbelow(1 << 32)
            responder = Responder(pt, seq0, delays, clips, hangover, plan)
            contact = [("Contact", f"<sip:agent@{local}:{sip_port}>")]
            body = sip.sdp(local, rtp_port, [pt])
            ok = sip.response(msg, 200, "OK", to_tag, body, contact).render()
            sock.sendto(sip.response(msg, 100, "Trying").render(), addr)
            sock.sendto(ok, addr)
            ok_to, resend_at = addr, time.monotonic() + interval
            start = time.time_ns() + PTIME_NS
            threads = [
                Sender(rtp, (ip, port), pt, responder.source, start, seq0, ssrc),
                Receiver(rtp, responder.on_packet),
            ]
            for t in threads:
                t.start()
            if case and case.greet_s is not None:
                greeting = 0 if case.greeting == "short" else len(short)
                responder.speak(time.time_ns() + round(case.greet_s * 1e9), greeting, "greeting")
            meta = {"pt": pt, "ssrc": ssrc, "seq0": seq0, "seed": seed}
        elif msg.method == "ACK":
            acked = True
        elif msg.method == "BYE" and msg.get("call-id") == call_id:
            sock.sendto(sip.response(msg, 200, "OK").render(), addr)
            break
        elif msg.method in ("OPTIONS", "BYE"):
            sock.sendto(sip.response(msg, 200, "OK", to_tag).render(), addr)
    for t in threads:
        t.stop.set()
    for t in threads:
        t.join()
    assert responder is not None
    return meta | {"turns": responder.turns}
