"""Reference agent: answers each caller turn a known delay after the caller stops talking.

The delay runs from the last active sample it received (kernel arrival time plus the sample's
offset in its packet) to the first active sample it sends (tick time plus offset), so the
response onset is placed to the sample, not to the packet.
"""

import random
import secrets
import socket
import threading
import time
from pathlib import Path
from typing import Any

from rtpbench import g711, sip
from rtpbench.rtp import FRAME, PTIME_NS, SAMPLE_NS, Packet, Receiver, Sender
from rtpbench.voice import GATE, voice

HANGOVER_NS = 200_000_000  # silence that ends a caller turn
DELAY_RANGE = (0.3, 1.3)  # seconds; the low end leaves 100 ms after the hangover to schedule
RESPONSE_SECONDS = 0.8


class Responder:
    def __init__(self, pt: int, seq0: int, delays: list[float]) -> None:
        self.pt, self.seq0, self.delays = pt, seq0, delays
        self.gate = g711.gate(pt, GATE)
        self.silence = bytes([g711.SILENCE[pt]]) * FRAME
        self.response = g711.encode(pt, voice(RESPONSE_SECONDS, f0=210))
        self.lock = threading.Lock()
        self.turns: list[dict[str, Any]] = []
        self.speaking = False
        self.end_ns, self.end_seq, self.end_off = 0, 0, 0
        self.pending: dict[str, Any] | None = None
        self.pos: int | None = None  # response sample index at the start of the next tick

    def on_packet(self, arrival: int, pkt: Packet) -> None:
        if pkt.pt != self.pt:
            return
        with self.lock:
            if m := self.gate.search(pkt.payload[::-1]):
                off = len(pkt.payload) - 1 - m.start()
                if (end := arrival + off * SAMPLE_NS) > self.end_ns:
                    self.end_ns, self.end_seq, self.end_off = end, pkt.seq, off
                self.speaking = True
            elif self.speaking and arrival - self.end_ns >= HANGOVER_NS:
                self.speaking = False
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

    def source(self, n: int, tick: int) -> bytes:
        with self.lock:
            p = self.pending
            if self.pos is None and p is not None and p["target_ns"] < tick + PTIME_NS:
                off = max(0, round((p["target_ns"] - tick) / SAMPLE_NS))
                p |= {"onset_seq": (self.seq0 + n) & 0xFFFF, "onset_off": off, "tick_ns": tick}
                self.turns.append(p)
                self.pending, self.pos = None, -off
            if self.pos is None:
                return self.silence
            pos, self.pos = self.pos, self.pos + FRAME
            if self.pos >= len(self.response):
                self.pos = None
            head = self.silence[: max(0, -pos)]
            return (head + self.response[max(0, pos) : pos + FRAME]).ljust(FRAME, self.silence[:1])


def _local_ip(peer: tuple[str, int]) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(peer)
        return str(s.getsockname()[0])


def serve(
    ready: Path, sip_port: int = 5060, rtp_port: int = 40000, seed: int = 1
) -> dict[str, Any]:
    """Answer one call; return its per-turn ground truth. Touches `ready` once listening."""
    rng = random.Random(seed)
    delays = [rng.uniform(*DELAY_RANGE) for _ in range(1000)]
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
            responder = Responder(pt, seq0, delays)
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
