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
from rtpbench.rtp import FRAME, PTIME_NS, SAMPLE_NS, Packet, Receiver, Sender
from rtpbench.voice import GATE, RATE, voice

LEAD_SECONDS = 1.0
UTTERANCE_RANGE = (0.8, 1.6)
GAP_SECONDS = 2.8  # longest delay (1.3 s) + response (0.8 s) + room for netem
QUIET_NS = 3_000_000_000  # agent silence that ends its turn (a real agent answers a barge-in)
REPLY_TIMEOUT_NS = 15_000_000_000
TURN_TIMEOUT_NS = 60_000_000_000

Clip = tuple[str, list[int]]
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
    """One call: the SIP dialog and the RTP socket, from INVITE to BYE."""

    def __init__(self, uri: str, codecs: tuple[int, ...]) -> None:
        peer = parse_uri(uri)
        probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        probe.connect(peer)
        local_ip = probe.getsockname()[0]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", 0))
        self.rtp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rtp.bind(("0.0.0.0", 0))
        self.dialog = sip.Dialog(sock, peer, uri, local_ip)
        ok = self.dialog.invite(sip.sdp(local_ip, self.rtp.getsockname()[1], list(codecs)))
        ip, port, pts = sip.parse_sdp(ok.body)
        self.addr = (ip, port)
        self.pt = next(p for p in pts if p in g711.NAMES)
        self.seq0, self.ssrc = secrets.randbelow(1 << 16), secrets.randbelow(1 << 32)

    def run(
        self,
        source: Callable[[int, int], bytes],
        sink: Callable[[int, Packet], None],
        until: Callable[[int], bool],
    ) -> bool:
        """Media until `until(now_ns)`, then hang up. True if the far end hung up first."""
        start = time.time_ns() + PTIME_NS
        sender = Sender(self.rtp, self.addr, self.pt, source, start, self.seq0, self.ssrc)
        receiver = Receiver(self.rtp, sink)
        sender.start()
        receiver.start()
        remote_bye = False
        while not until(time.time_ns()):
            msg = self.dialog.recv(0.1)
            if msg is None:
                continue
            if msg.status == 200 and msg.cseq_method == "INVITE":
                self.dialog.ack()
            elif msg.method:
                self.dialog.reply(msg)
                if remote_bye := msg.method == "BYE":
                    break
        sender.stop.set()
        receiver.stop.set()
        sender.join()
        receiver.join()
        if not remote_bye:
            self.dialog.bye()
        return remote_bye

    def meta(self, seed: int, remote_bye: bool) -> dict[str, Any]:
        return {"pt": self.pt, "ssrc": self.ssrc, "seq0": self.seq0, "seed": seed} | {
            "remote_bye": remote_bye
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


class Conversation:
    """Barge-in script as an RTP source: each turn a prompt, then, once the agent's reply has
    started, an interjection `at_s` later, then quiet before the next prompt."""

    def __init__(
        self,
        pt: int,
        script: list[tuple[Labelled, Labelled, dict[str, Any]]],
        lead_ns: int,
    ) -> None:
        self.gate = g711.gate(pt, GATE)
        self.silence = bytes([g711.SILENCE[pt]]) * FRAME
        self.script = [
            ((pn, g711.encode(pt, p), ps), (jn, g711.encode(pt, j), js), st)
            for (pn, p, ps), (jn, j, js), st in script
        ]
        self.lead_ns = lead_ns
        self.lock = threading.Lock()
        self.turns: list[dict[str, Any]] = []
        self.state, self.turn = "lead", 0
        self.t0: int | None = None
        self.audio, self.apos = b"", 0
        self.since = 0  # when the current state began
        self.wait_until = 0
        self.onset: int | None = None  # first agent sample heard after the prompt
        self.agent_last = 0
        self.done = False

    def on_packet(self, arrival: int, pkt: Packet) -> None:
        if not (first := self.gate.search(pkt.payload)):
            return
        last = self.gate.search(pkt.payload[::-1])
        assert last is not None
        with self.lock:
            end = arrival + (len(pkt.payload) - 1 - last.start()) * SAMPLE_NS
            self.agent_last = max(self.agent_last, end)
            on = arrival + first.start() * SAMPLE_NS
            if self.state == "reply" and self.onset is None and on > self.since:
                self.onset = on

    def _play(self, n: int, clip: tuple[str, bytes, list[tuple[int, int]]]) -> dict[str, Any]:
        name, audio, spans = clip
        self.audio, self.apos = audio, 0
        start = n * FRAME
        return {"clip": name, "speech": [[a + start, b + start] for a, b in spans]}

    def source(self, n: int, tick: int) -> bytes:
        with self.lock:
            if self.t0 is None:
                self.t0 = tick
            if not self.audio:
                self._step(n, tick)
            if not self.audio:
                return self.silence
            out = self.audio[self.apos : self.apos + FRAME].ljust(FRAME, self.silence[:1])
            self.apos += FRAME
            if self.apos >= len(self.audio):
                self.audio = b""
                self.state = "reply" if self.state == "prompt" else "quiet"
                self.since, self.onset = tick, None
            return out

    def _step(self, n: int, tick: int) -> None:
        assert self.t0 is not None
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
            self.turns[-1] |= {"kind": step["kind"], "at_s": step["at_s"]} | self._play(
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
        rec = self._play(n, prompt)
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
    conv = Conversation(s.pt, lines, round(lead * 1e9))
    remote_bye = s.run(conv.source, conv.on_packet, lambda _now: conv.done)
    return s.meta(seed, remote_bye) | {"turns": conv.turns}
