"""Caller: speaks fixed turns (synthetic or from WAV files) over a real SIP call, or, for
barge-in, reacts to the agent: prompt, wait for the reply, cut in, wait for quiet."""

import random
import secrets
import socket
import threading
import time
from collections.abc import Callable
from typing import Any

from rtpbench import bargein, g711, sip, speech
from rtpbench.rtp import FRAME, PTIME_NS, SAMPLE_NS, Frame, Packet, Receiver, Sender
from rtpbench.voice import GATE, RATE, voice

LEAD_SECONDS = 1.0
UTTERANCE_RANGE = (0.8, 1.6)
GAP_SECONDS = 2.8  # longest delay (1.3 s) + response (0.8 s) + room for netem
QUIET_NS = 3_000_000_000  # agent silence that ends its turn (a real agent answers a barge-in)
REPLY_TIMEOUT_NS = 15_000_000_000
TURN_TIMEOUT_NS = 60_000_000_000

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


def parse_uri(uri: str) -> tuple[str, int]:
    hostport = uri.split("@", 1)[-1].split(";", 1)[0].removeprefix("sip:")
    host, _, port = hostport.partition(":")
    return host, int(port or 5060)


class Session:
    """One call: the SIP dialog and the RTP socket, from INVITE to BYE (sent to the URI's host,
    or to `proxy`, a host[:port]).

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
    ) -> None:
        peer = parse_uri(proxy or uri)  # an outbound proxy takes the request whatever its URI
        probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        probe.connect(peer)
        local_ip = probe.getsockname()[0]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", 0))
        self.rtp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rtp.bind(("0.0.0.0", 0))
        self.dialog = sip.Dialog.uac(sock, peer, uri, local_ip)
        self.origin = (secrets.randbelow(1 << 31), 0)  # SDP session id, version
        self.held = False
        self.dtmf: int | None = None  # telephone-event payload type, if the answer has it
        port = self.rtp.getsockname()[1]
        offer = sip.sdp(local_ip, port, list(codecs), origin=self.origin, dtmf=dtmf)
        self.invite = self.dialog.request("INVITE", offer, headers)
        self.invites = {self.invite.branch: self.invite}
        self.final: sip.Message | None = None  # final response to the INVITE
        self.responses: list[sip.Message] = []
        self.requests: list[sip.Message] = []  # from the far end
        self.remote_bye = False
        self.addr, self.pt = ("", 0), 0
        self.seq0, self.ssrc = secrets.randbelow(1 << 16), secrets.randbelow(1 << 32)
        self.media: tuple[Sender, Receiver] | None = None
        self.dialog.send(self.invite)

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
            if initial:
                self.final = msg
            if req := self.invites.get(msg.branch):
                self.dialog.ack_failure(req, msg)
            return
        if not initial:
            self.dialog.ack(msg)
            return
        self.dialog.confirm(msg)  # every 2xx, retransmissions included
        if self.final is None:
            self.final = msg
            answer = sip.parse_sdp(msg.body)
            self.addr = (answer.ip, answer.port)
            self.pt = next((p for p in answer.pts if p in g711.NAMES), -1)  # -1: answer() ends it
            self.dtmf = answer.dtmf

    def _incoming(self, req: sip.Message) -> None:
        self.requests.append(req)
        if req.method == "ACK":
            return
        if req.method == "INVITE":  # a refresh, or a change we take as it comes
            port = self.rtp.getsockname()[1]
            sdp = sip.sdp(self.dialog.local_ip, port, [self.pt], origin=self.origin)
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
        return final()

    def reinvite(
        self, direction: str = "sendrecv", headers: list[tuple[str, str]] | None = None
    ) -> sip.Message | None:
        """Offer the call's codec again, `direction` (sendonly, inactive: hold; sendrecv
        unchanged: a refresh, same SDP version); the response."""
        if direction != "sendrecv" or self.held:
            self.origin = (self.origin[0], self.origin[1] + 1)
        self.held = direction != "sendrecv"
        port = self.rtp.getsockname()[1]
        sdp = sip.sdp(self.dialog.local_ip, port, [self.pt], direction, self.origin)
        return self.request("INVITE", sdp, headers)

    def start(self, source: Source, sink: Callable[[int, Packet], None]) -> None:
        start = time.time_ns() + PTIME_NS
        self.media = (
            Sender(self.rtp, self.addr, self.pt, source, start, self.seq0, self.ssrc),
            Receiver(self.rtp, sink),
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
        self.wait(lambda: self.remote_bye or until(time.time_ns()), float("inf"))
        self.hangup()
        return self.remote_bye

    def meta(self, seed: int, remote_bye: bool) -> dict[str, Any]:
        return {"pt": self.pt, "ssrc": self.ssrc, "seq0": self.seq0, "seed": seed} | {
            "remote_bye": remote_bye,
            "call_id": self.dialog.call_id,
            "rtp_port": self.rtp.getsockname()[1],
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
    hangup_ns = time.time_ns() + PTIME_NS + len(frames) * PTIME_NS
    remote_bye = s.run(
        lambda n, _t: frames[n] if n < len(frames) else silence,
        lambda _a, _p: None,
        lambda now: now >= hangup_ns,
    )
    return s.meta(seed, remote_bye) | {"turns": last}


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
    remote_bye = s.run(conv.source, conv.on_packet, lambda _now: conv.done)
    return s.meta(seed, remote_bye) | {"turns": conv.turns}
