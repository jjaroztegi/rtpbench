"""Mock engine: a deterministic stand-in for the OpenAI Realtime API (GA protocol).

A WebSocket server (stdlib only) that speaks the protocol both public targets use: G.711 in
and out (AI Voice Connector CE, by OPENAI_URL) or 24 kHz PCM16 (LiveKit's `with_azure`, by its
endpoint). It hears the caller with the reference agent's energy gate: a turn starts at the
first voiced 10 ms frame and ends after HANGOVER_NS of audio without one. At the end of a turn
it tells which of the caller's lines (corpus/lines/en) was said from its energy envelope and,
HANGOVER_NS + DELAY_NS after the turn's last labelled sample arrived (labelled as the caller's
lines are), answers: the transfer line
with a call to the transfer tool, a long question with a long clip, anything else with a short
one (always the same clips). A turn that starts while it answers cancels the answer, as server
VAD does. Audio goes out in 100 ms deltas, kept LEAD_NS ahead of real time.

Every answer is logged (`/out/realtime.jsonl`) with when the caller's speech ended as heard
here and when the first audio went out, on the clock captures stamp: a target's turn latency
then splits into its uplink, this engine's known share and its downlink (`decompose`). What
arrives is recorded as it arrived (`/out/realtime/<session>.raw`, `.idx`), so the summary can
say what a target did to the caller's audio (`uplink`) as to the engine's (`downlink`).
"""

import asyncio
import base64
import hashlib
import json
import math
import secrets
import statistics
import struct
from array import array
from collections.abc import Sequence
from pathlib import Path
from typing import Any, BinaryIO, TextIO

from rtpbench import g711, speech
from rtpbench.clock import CLOCK
from rtpbench.voice import GATE

PORT = 8000
FRAME = 80  # 10 ms at 8 kHz
PACKET = 160  # 20 ms
HANGOVER_NS = 1_000_000_000  # silence that ends a turn (real speech pauses up to 0.8 s inside)
DELAY_NS = 500_000_000  # from the end of a turn to the answer
DELTA_MS = 100  # audio per delta
LEAD_NS = 500_000_000  # how far ahead of real time the audio is sent
SPAN_DB = 40  # a line runs from its first to its last 20 ms within this of its loudest
TOOL = "transfer_call"
SHORT, LONG = "tts-ljspeech-s00", "tts-ljspeech-long"
_GUID = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def envelope(pcm: list[int]) -> list[float]:
    """20 ms log energy (dB) over 8 kHz samples: a packet's worth, so a lost packet blurs one
    value instead of splitting two."""
    return [
        10 * math.log10(sum(s * s for s in pcm[i : i + PACKET]) / PACKET + 1.0)
        for i in range(0, len(pcm) - PACKET + 1, PACKET)
    ]


def shape(pcm: list[int]) -> list[float]:
    """The envelope from the first to the last value within SPAN_DB of its loudest, less its mean:
    the same for a line at any level (one connector passes G.711 through, another resamples and
    re-encodes it on the way)."""
    e = envelope(pcm)
    if not e:
        return []
    on = [i for i, x in enumerate(e) if x >= max(e) - SPAN_DB]
    e = e[on[0] : on[-1] + 1]
    mean = sum(e) / len(e)
    return [x - mean for x in e]


def distance(a: list[float], b: list[float]) -> float:
    """Mean dB apart along the closest time warp of two envelopes that strays from the diagonal by
    500 ms or a fifth of the longer, whichever is more: packets dropped or concealed on the way
    stretch or shrink a line, which a straight comparison takes for a different line. inf if the
    lengths differ by more."""
    n, m = len(a), len(b)
    band = max(25, max(n, m) // 5)
    if not n or not m or abs(n - m) > band:
        return math.inf
    prev = [0.0] + [math.inf] * m
    for i in range(1, n + 1):
        cur = [math.inf] * (m + 1)
        for j in range(max(1, i - band), min(m, i + band) + 1):
            cur[j] = abs(a[i - 1] - b[j - 1]) + min(prev[j], prev[j - 1], cur[j - 1])
        prev = cur
    return prev[m] / (n + m)


class Lines:
    """The caller's lines, and what to answer each with."""

    def __init__(self) -> None:
        paths = sorted((speech.CORPUS / "lines" / "en").glob("*.wav"))
        self.refs = {p.stem: shape(speech.read_wav(p)) for p in paths}
        self.clips = {}
        for name in (SHORT, LONG):  # from the labelled onset, so sample 0 is speech
            pcm = speech.read_wav(speech.CORPUS / f"{name}.wav")
            self.clips[name] = pcm[speech.label(pcm)[0][0] :]

    def recognise(self, pcm: list[int]) -> tuple[str, float]:
        """The line nearest to `pcm` (8 kHz) and its distance; "" if no line is near its length.
        No distance limit: a target's path can move a line by as much as a different line differs
        (LiveKit's by 1.7 dB, where the nearest other line was 2.8), and the caller says only its
        lines, or short interjections that come out as short turns."""
        e = shape(pcm)
        best = min(((distance(e, r), n) for n, r in self.refs.items()), default=(math.inf, ""))
        return (best[1] if best[0] < math.inf else ""), best[0]

    @staticmethod
    def answer(line: str) -> str:
        """The clip for a line, or TOOL."""
        if line == "transfer":
            return TOOL
        return LONG if line.startswith("prompt") else SHORT


# --- WebSocket (RFC 6455, server side: text frames out, masked frames in) ---


async def _handshake(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> str:
    head = (await reader.readuntil(b"\r\n\r\n")).decode(errors="replace").split("\r\n")
    headers = {k.strip().lower(): v.strip() for k, _, v in (h.partition(":") for h in head[1:])}
    key = headers["sec-websocket-key"].encode()
    accept = base64.b64encode(hashlib.sha1(key + _GUID).digest()).decode()
    writer.write(
        (
            "HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
            f"Sec-WebSocket-Accept: {accept}\r\n\r\n"
        ).encode()
    )
    await writer.drain()
    return head[0]


async def _frame(reader: asyncio.StreamReader) -> tuple[int, bytes]:
    """One message: opcode and payload (continuation frames joined)."""
    data, first = b"", None
    while True:
        b0, b1 = await reader.readexactly(2)
        n = b1 & 0x7F
        if n == 126:
            n = struct.unpack("!H", await reader.readexactly(2))[0]
        elif n == 127:
            n = struct.unpack("!Q", await reader.readexactly(8))[0]
        mask = await reader.readexactly(4) if b1 & 0x80 else b""
        chunk = await reader.readexactly(n)
        if mask:
            chunk = bytes(c ^ mask[i % 4] for i, c in enumerate(chunk))
        if b0 & 0x0F >= 8:  # a control frame may sit between fragments
            return b0 & 0x0F, chunk
        first = b0 & 0x0F if first is None else first
        data += chunk
        if b0 & 0x80:
            return first, data


def _pack(opcode: int, data: bytes) -> bytes:
    n = len(data)
    if n < 126:
        head = struct.pack("!BB", 0x80 | opcode, n)
    elif n < 1 << 16:
        head = struct.pack("!BBH", 0x80 | opcode, 126, n)
    else:
        head = struct.pack("!BBQ", 0x80 | opcode, 127, n)
    return head + data


# --- the engine ---


def _id(prefix: str) -> str:
    return f"{prefix}_{secrets.token_hex(8)}"


def _upsample(pcm: list[int]) -> bytes:
    """8 kHz samples as 24 kHz PCM16, by linear interpolation."""
    up = array("h")
    for a, b in zip(pcm, [*pcm[1:], pcm[-1]], strict=True):
        up.extend((a, round(a + (b - a) / 3), round(a + 2 * (b - a) / 3)))
    return up.tobytes()


class Session:
    """One WebSocket connection: a conversation."""

    def __init__(self, writer: asyncio.StreamWriter, lines: Lines, log: Path) -> None:
        self.writer, self.lines, self.log = writer, lines, log
        self.id = _id("sess")
        self.session: dict[str, Any] = {"type": "realtime", "object": "realtime.session"}
        self.pt: int | None = None  # G.711 law, or None for 24 kHz PCM16
        self.heard: list[int] = []  # the current turn, 8 kHz
        self.heard_at: list[int] = []  # clock time of each of its 10 ms frames' sample 0
        self.speaking = False
        self.last_voiced = 0  # clock time of the turn's last voiced sample
        self.quiet = 0  # samples since it
        self.started = 0  # clock time the turn started
        self.answering: asyncio.Task[None] | None = None
        self.responding = False  # an answer has been created and is not done
        self.user_item = ""
        self.last_item = ""
        self.tools: list[str] = []
        self.kept: tuple[BinaryIO, TextIO] | None = None  # realtime/<id>.raw and .idx

    # outgoing

    async def send(self, event: dict[str, Any]) -> None:
        event = {"event_id": _id("event")} | event
        self.writer.write(_pack(1, json.dumps(event).encode()))
        await self.writer.drain()

    def note(self, record: dict[str, Any]) -> None:
        with self.log.open("a") as f:
            f.write(json.dumps({"session": self.id} | record) + "\n")

    # incoming

    async def handle(self, event: dict[str, Any]) -> None:
        kind = event.get("type")
        if kind == "session.update":
            self.configure(event.get("session", {}))
            await self.send({"type": "session.updated", "session": self.session})
        elif kind == "input_audio_buffer.append":
            audio, now = base64.b64decode(event["audio"]), CLOCK.now()
            await self.hear(audio, now)
            self.keep(audio, now)
        elif kind == "response.create":
            asked, now = event.get("response", {}), CLOCK.now()
            self.start(self.reply(self.lines.answer(""), "create", asked, now, {"asked_ns": now}))
        elif kind == "response.cancel":
            await self.cancel()
        elif kind == "conversation.item.create":
            item = event.get("item", {}) | {"id": event.get("item", {}).get("id") or _id("item")}
            await self.added(item)
        elif kind == "conversation.item.truncate":
            await self.send(
                {
                    "type": "conversation.item.truncated",
                    "item_id": event.get("item_id"),
                    "content_index": event.get("content_index", 0),
                    "audio_end_ms": event.get("audio_end_ms", 0),
                }
            )
        elif kind in ("input_audio_buffer.clear", "input_audio_buffer.commit"):
            if kind.endswith("clear"):
                self.heard, self.speaking = [], False
            await self.send(
                {"type": kind.replace("clear", "cleared").replace("commit", "committed")}
            )

    def keep(self, audio: bytes, arrival: int) -> None:
        """Record what arrived as it arrived: the bytes to realtime/<id>.raw, and the arrival
        time, byte count and format (pcmu, pcma or pcm16 at 24 kHz) to realtime/<id>.idx."""
        if self.kept is None:
            where = self.log.parent / "realtime"
            where.mkdir(exist_ok=True)
            raw, idx = where / f"{self.id}.raw", where / f"{self.id}.idx"
            self.kept = raw.open("ab"), idx.open("a")
        fmt = "pcm16" if self.pt is None else g711.NAMES[self.pt].lower()
        self.kept[0].write(audio)
        self.kept[1].write(f"{arrival} {len(audio)} {fmt}\n")
        for f in self.kept:
            f.flush()  # whole appends on disk, however the engine is stopped

    def close(self) -> None:
        if self.kept is not None:
            for f in self.kept:
                f.close()

    def configure(self, update: dict[str, Any]) -> None:
        self.session |= update
        fmt = update.get("audio", {}).get("input", {}).get("format", {}).get("type", "")
        if fmt:
            self.pt = {"audio/pcmu": g711.PCMU, "audio/pcma": g711.PCMA}.get(fmt)
        if "tools" in update:
            self.tools = [t.get("name", "") for t in update["tools"]]
        self.note({"event": "session", "format": fmt or None, "tools": self.tools})

    async def added(self, item: dict[str, Any]) -> None:
        await self.send(
            {"type": "conversation.item.added", "previous_item_id": self.last_item or None}
            | {"item": item}
        )
        await self.send({"type": "conversation.item.done", "item": item})
        self.last_item = item["id"]

    def decode(self, audio: bytes) -> list[int]:
        """8 kHz samples of what was appended."""
        if self.pt is not None:
            return g711.decode(self.pt, audio)
        pcm = array("h", audio[: len(audio) // 2 * 2])
        return [round((pcm[i] + pcm[i + 1] + pcm[i + 2]) / 3) for i in range(0, len(pcm) - 2, 3)]

    def encode(self, pcm: list[int]) -> bytes:
        """8 kHz samples as this session sends audio."""
        return g711.encode(self.pt, pcm) if self.pt is not None else _upsample(pcm)

    async def hear(self, audio: bytes, arrival: int) -> None:
        """Audio that arrived at `arrival`: turns start and end, by the audio itself (a turn ends
        after HANGOVER_NS of silent audio, however fast it came). Sample k of a chunk sits at
        arrival + k/8000 s, the convention the captures' analysis uses for a packet."""
        pcm = self.decode(audio)
        for i in range(0, len(pcm), FRAME):
            frame = pcm[i : i + FRAME]
            t0 = arrival + i * 125_000  # the frame's sample 0
            loud = [k for k, s in enumerate(frame) if abs(s) >= GATE]
            if loud:
                if not self.speaking:
                    await self.turn_starts(t0 + loud[0] * 125_000)
                self.last_voiced = t0 + loud[-1] * 125_000
                self.quiet = len(frame) - 1 - loud[-1]
            elif self.speaking:
                self.quiet += len(frame)
            if self.speaking:
                self.heard += frame
                self.heard_at.append(t0)
                if self.quiet * 125_000 >= HANGOVER_NS:
                    await self.turn_ends()

    async def turn_starts(self, at: int) -> None:
        self.speaking, self.heard, self.heard_at, self.started = True, [], [], at
        self.user_item = _id("item")
        barged = self.responding
        await self.send(
            {"type": "input_audio_buffer.speech_started", "item_id": self.user_item}
            | {"audio_start_ms": 0}
        )
        if barged:
            self.note({"event": "barge", "speech_start_ns": at, "cancel_ns": CLOCK.now()})
        await self.cancel()  # an answer playing, or still to come

    async def turn_ends(self) -> None:
        self.speaking = False
        line, how = self.lines.recognise(self.heard)
        await self.send(
            {"type": "input_audio_buffer.speech_stopped", "item_id": self.user_item}
            | {"audio_end_ms": 0}
        )
        await self.send(
            {"type": "input_audio_buffer.committed", "item_id": self.user_item}
            | {"previous_item_id": self.last_item or None}
        )
        content = [{"type": "input_audio", "transcript": line or None}]
        await self.added(
            {"id": self.user_item, "type": "message", "role": "user"} | {"content": content}
        )
        await self.send(
            {
                "type": "conversation.item.input_audio_transcription.completed",
                "item_id": self.user_item,
                "content_index": 0,
                "transcript": line or "(not one of the caller's lines)",
            }
        )
        end = self.speech_end()
        heard = {
            "line": line,
            "distance": round(how, 3) if how < math.inf else None,
            "speech_end_ns": end,
        }
        heard["gate_end_ns"] = self.last_voiced
        since = end + HANGOVER_NS  # so the engine always takes HANGOVER + DELAY from the end
        self.start(self.reply(self.lines.answer(line), "turn", {}, since, heard))

    def speech_end(self) -> int:
        """When the turn's last labelled sample (`speech.label`, as the caller's lines are
        labelled) arrived; the gate's last voiced sample if the turn will not label."""
        try:
            k = speech.label(self.heard)[-1][1] - 1
        except ValueError:
            return self.last_voiced
        return self.heard_at[k // FRAME] + k % FRAME * 125_000

    def start(self, answer: Any) -> None:
        if self.answering is not None and not self.answering.done():
            self.answering.cancel()
        self.answering = asyncio.ensure_future(answer)

    async def cancel(self) -> None:
        if self.answering is not None and not self.answering.done():
            self.answering.cancel()
            await asyncio.gather(self.answering, return_exceptions=True)

    async def reply(
        self,
        what: str,
        trigger: str,
        asked: dict[str, Any],
        since: int,
        heard: dict[str, Any] | None = None,
    ) -> None:
        """Answer DELAY_NS after `since`: a clip, or a call to TOOL (if the target has it)."""
        await asyncio.sleep(max(0, since + DELAY_NS - CLOCK.now()) / 1e9)
        if what == TOOL and TOOL not in self.tools:
            what = SHORT
        rid, item_id = _id("resp"), _id("item")
        response: dict[str, Any] = {
            "id": rid,
            "object": "realtime.response",
            "status": "in_progress",
            "output": [],
            "metadata": asked.get("metadata"),
            "audio": {
                "output": {"format": self.session.get("audio", {}).get("output", {}).get("format")}
            },
        }
        await self.send({"type": "response.created", "response": response})
        self.responding = True
        record = {"event": "answer", "trigger": trigger, "answer": what} | (heard or {})
        status, item = "completed", {}
        try:
            if what == TOOL:
                item = await self.call_tool(rid, item_id)
            else:
                item = await self.speak(rid, item_id, what, record)
        except asyncio.CancelledError:
            status = "cancelled"
            raise
        finally:
            self.responding = False
            self.note(record | {"status": status, "end_ns": CLOCK.now()})
            done = response | {"status": status, "output": [item] if item else []}
            done["usage"] = {"total_tokens": 0, "input_tokens": 0, "output_tokens": 0}
            await asyncio.shield(self.send({"type": "response.done", "response": done}))

    async def call_tool(self, rid: str, item_id: str) -> dict[str, Any]:
        call_id = _id("call")
        item = {"id": item_id, "object": "realtime.item", "type": "function_call"}
        item |= {"status": "in_progress", "name": TOOL, "call_id": call_id, "arguments": ""}
        where = {"response_id": rid, "output_index": 0}
        await self.send({"type": "response.output_item.added", "item": item} | where)
        await self.added(item)
        args = {"item_id": item_id, "call_id": call_id} | where
        await self.send({"type": "response.function_call_arguments.delta", "delta": "{}"} | args)
        await self.send(
            {"type": "response.function_call_arguments.done", "name": TOOL, "arguments": "{}"}
            | args
        )
        item |= {"status": "completed", "arguments": "{}"}
        await self.send({"type": "response.output_item.done", "item": item} | where)
        return item

    async def speak(
        self, rid: str, item_id: str, clip: str, record: dict[str, Any]
    ) -> dict[str, Any]:
        item: dict[str, Any] = {"id": item_id, "object": "realtime.item", "type": "message"}
        item |= {"role": "assistant", "status": "in_progress", "content": []}
        where = {"response_id": rid, "item_id": item_id, "output_index": 0, "content_index": 0}
        await self.send(
            {"type": "response.output_item.added", "item": item, "response_id": rid}
            | {"output_index": 0}
        )
        await self.added(item)
        part = {"type": "audio", "transcript": ""}
        await self.send({"type": "response.content_part.added", "part": part} | where)
        pcm, step = self.lines.clips[clip], 8 * DELTA_MS
        t0 = CLOCK.now()
        record |= {"clip": clip, "first_audio_ns": t0}
        for k, i in enumerate(range(0, len(pcm), step)):
            await asyncio.sleep(max(0, t0 + k * DELTA_MS * 1_000_000 - LEAD_NS - CLOCK.now()) / 1e9)
            delta = base64.b64encode(self.encode(pcm[i : i + step])).decode()
            await self.send({"type": "response.output_audio.delta", "delta": delta} | where)
        await self.send({"type": "response.output_audio.done"} | where)
        await self.send(
            {"type": "response.output_audio_transcript.done", "transcript": clip} | where
        )
        part = {"type": "audio", "transcript": clip}
        await self.send({"type": "response.content_part.done", "part": part} | where)
        item |= {"status": "completed", "content": [{"type": "output_audio", "transcript": clip}]}
        await self.send(
            {"type": "response.output_item.done", "item": item, "response_id": rid}
            | {"output_index": 0}
        )
        return item


def serve(out: Path, port: int = PORT, ready: Path | None = None) -> None:
    """Serve sessions until killed; log to out/realtime.jsonl; touch `ready` once listening."""
    lines = Lines()
    out.mkdir(parents=True, exist_ok=True)
    log = out / "realtime.jsonl"

    async def connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            request = await _handshake(reader, writer)
        except asyncio.IncompleteReadError, KeyError, ConnectionError:
            writer.close()
            return
        s = Session(writer, lines, log)
        s.note({"event": "connect", "request": request.split(" ")[1], "at_ns": CLOCK.now()})
        await s.send({"type": "session.created", "session": s.session | {"id": s.id}})
        try:
            while True:
                opcode, data = await _frame(reader)
                if opcode == 8:
                    break
                if opcode == 9:
                    writer.write(_pack(10, data))
                elif opcode == 1:
                    await s.handle(json.loads(data))
        except asyncio.IncompleteReadError, ConnectionError:
            pass
        finally:
            await s.cancel()
            s.close()
            s.note({"event": "close", "at_ns": CLOCK.now()})
            writer.close()

    async def main() -> None:
        server = await asyncio.start_server(connection, "0.0.0.0", port)
        if ready:
            await asyncio.to_thread(ready.touch)
        async with server:
            await server.serve_forever()

    asyncio.run(main())


def conditions() -> dict[str, Any]:
    """The mock engine as a run's conditions record it."""
    return {
        "mock": "rtpbench.realtime",
        "hangover_ms": HANGOVER_NS / 1e6,
        "delay_ms": DELAY_NS / 1e6,
        "lead_ms": LEAD_NS / 1e6,
        "clips": [SHORT, LONG],
    }


def _cells(parts: list[tuple[float, ...]]) -> list[str]:
    """p50 [p5, p95] of each column."""
    from rtpbench import analyze

    out = []
    for k in range(len(parts[0])):
        v = [p[k] for p in parts]
        q = [analyze._pct(v, x) for x in (0.5, 0.05, 0.95)]
        out.append(f"{q[0]:.0f} [{q[1]:.0f}, {q[2]:.0f}]")
    return out


def decompose(out: Path) -> str:
    """Turn latency and greeting time against the mock engine, split where it heard and
    answered, per profile. Turns (the latency calls): uplink (caller's labelled end on the wire to
    the end of speech as heard here), engine (to the first audio sent; HANGOVER_NS + DELAY_NS by
    design) and downlink (to the agent's first speech on the wire, webrtcvad). Greeting (the
    `greeting` case calls): 200 OK to the target's request for a greeting, the engine's DELAY_NS,
    first audio to the agent's speech on the wire."""
    from rtpbench import analyze, cases, speechcal

    records = [json.loads(line) for line in (out / "realtime.jsonl").read_text().splitlines()]
    answers = [r for r in records if r.get("event") == "answer" and "first_audio_ns" in r]
    heard = sorted(
        (r["speech_end_ns"], r["first_audio_ns"]) for r in answers if "speech_end_ns" in r
    )
    asked = sorted((r["asked_ns"], r["first_audio_ns"]) for r in answers if "asked_ns" in r)
    turns: dict[str, list[tuple[float, ...]]] = {}
    for path in sorted(out.glob("*/*/latency/caller.json")):
        for t in speechcal.turns(path.parent, ("webrtcvad",)):
            if t["webrtcvad_ms"] is None:
                continue
            end = t["end_ns"]
            onset = end + round(t["webrtcvad_ms"] * 1e6)
            # the end as heard here: after the caller's on the wire, give or take label noise
            if got := [(e, a) for e, a in heard if end - 500_000_000 <= e < onset and a < onset]:
                e, a = got[-1]
                parts = (t["webrtcvad_ms"], (e - end) / 1e6, (a - e) / 1e6, (onset - a) / 1e6)
                turns.setdefault(path.parts[-4], []).append(parts)
    greetings: dict[str, list[tuple[float, ...]]] = {}
    for path in sorted(out.glob("*/*/greeting/caller.json")):
        w = cases.load(path.parent)
        ok = w.find(cases._is_2xx_invite, sent=False)
        onset = w.speech_after(ok[0]) if ok else None
        if ok and onset and (got := [(q, a) for q, a in asked if ok[0] - 5e9 < q and a < onset]):
            q, a = got[-1]
            parts = ((onset - ok[0]) / 1e6, (q - ok[0]) / 1e6, (a - q) / 1e6, (onset - a) / 1e6)
            greetings.setdefault(path.parts[-4], []).append(parts)
    text = ""
    if turns:
        head = ["profile", "turns", "wire latency", "uplink", "engine", "downlink"]
        rows = [[p, str(len(v)), *_cells(v)] for p, v in turns.items()]
        text += (
            "Turn latency on the mock engine, split where it heard the end of the caller's speech "
            "and sent its first audio (one clock with the captures), ms, p50 [p5, p95]: uplink and "
            f"downlink are the target's; the engine waits {HANGOVER_NS / 1e6:.0f} ms of silence "
            f"and answers {DELAY_NS / 1e6:.0f} ms later by design. Uplink carries the caller's "
            "label error (±17 ms), downlink the onset error bar of the profile and codec.\n\n"
            + analyze._table(head, rows)
        )
    if greetings:
        head = ["profile", "calls", "200 OK to speech", "to the request", "engine", "downlink"]
        rows = [[p, str(len(v)), *_cells(v)] for p, v in greetings.items()]
        text += (
            "\nGreeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the "
            "target's request for a greeting (negative: asked before answering), the engine's "
            f"{DELAY_NS / 1e6:.0f} ms, and from its first audio to the agent's speech on the wire "
            "(webrtcvad onset bar).\n\n" + analyze._table(head, rows)
        )
    return text


# --- what reached the caller of the audio sent here ---

PAUSE = 800  # 100 ms below the gate: a pause between stretches of speech
PIECE = 8000  # at most 1 s of speech aligned as one piece
SEARCH = 480  # how far a piece may sit from the one before it, 60 ms
SHIFT = 40  # 5 ms: a piece moved by less is a resampler's fraction of a sample, not a timing change
TAPS = 31  # a filter of ±4 ms explains any resampler's or band filter's change to a piece


def pieces(pcm: list[int]) -> list[tuple[int, int]]:
    """The speech in `pcm` as [start, end) sample spans between pauses, split to at most PIECE."""
    spans: list[list[int]] = []
    for i, s in enumerate(pcm):
        if abs(s) >= GATE:
            if spans and i - spans[-1][1] < PAUSE:
                spans[-1][1] = i + 1
            else:
                spans.append([i, i + 1])
    out = []
    for a, b in spans:
        n = -(-(b - a) // PIECE)
        out += [(a + (b - a) * k // n, a + (b - a) * (k + 1) // n) for k in range(n)]
    return out


def sent(clip: list[int], fmt: str | None) -> list[float]:
    """A clip as this engine sends it in `fmt`, at 8 kHz: G.711 decoded again, or the 24 kHz
    interpolation through an ideal 8 kHz converter (none of this engine's resampling counted
    against a target)."""
    import numpy as np

    law = {"audio/pcmu": g711.PCMU, "audio/pcma": g711.PCMA}.get(fmt or "")
    if law is not None:
        return [float(s) for s in g711.decode(law, g711.encode(law, clip))]
    return [float(s) for s in _to8k(np, np.frombuffer(_upsample(clip), dtype="<i2"))]


def _to8k(np: Any, pcm: Any) -> Any:
    """24 kHz samples through an ideal 8 kHz converter."""
    spectrum = np.fft.rfft(np.asarray(pcm, dtype=np.float64))
    spectrum[len(pcm) // 6 + 1 :] = 0  # above 4 kHz
    return np.fft.irfft(spectrum, len(pcm))[::3]


def _lag(np: Any, ref: Any, rx: Any) -> int:
    """Offset of `ref` in `rx` (no shorter) that correlates best."""
    n = 1 << (len(ref) + len(rx) - 1).bit_length()
    c = np.fft.irfft(np.fft.rfft(rx, n) * np.conj(np.fft.rfft(ref, n)), n)
    return int(np.argmax(c[: len(rx) - len(ref) + 1]))


def heard(ref: Sequence[float], rx: Sequence[float], ok: Sequence[bool]) -> dict[str, Any] | None:
    """What a path did to `ref` (8 kHz), received as `rx` from where it may start up to 1.5 s
    late, `ok` false for samples the network lost. Each piece of speech is aligned on its own,
    near the one before: gain (dB, least squares), what no linear filter of ±TAPS explains (dB
    below the audio; inf if unchanged), 3.4-4 kHz against 300-3400 Hz relative to `ref`'s (dB),
    the moves of 5 ms or more between pieces (ms, positive later), whether every sample is
    unchanged, where in `rx` `ref` starts (the median piece's offset), and its voiced 20 ms with
    nothing like them nearby in `rx`, by what came instead. None if under half the speech could
    be aligned."""
    import numpy as np

    r_all, x_all, m_all = np.asarray(ref), np.asarray(rx, dtype=np.float64), np.asarray(ok)
    spans = pieces([round(s) for s in ref])
    if not spans or len(x_all) < len(r_all) + 12000:
        return None
    lag = _lag(np, r_all[:16000], x_all[:28000])
    xs, rs, lags, band, fit = [], [], [], np.zeros((2, 2)), np.zeros(2)
    placed: list[tuple[int, int, int]] = []
    for a, b in spans:
        r = r_all[a:b]
        lo = max(0, lag + a - SEARCH)
        found = lo + _lag(np, r, x_all[lo : lag + b + SEARCH]) - a
        x, m = x_all[a + found : b + found], m_all[a + found : b + found]
        if m.mean() < 0.8:
            continue
        if np.sum(x[m] * r[m]) < 0.5 * np.sqrt(np.sum(x[m] ** 2) * np.sum(r[m] ** 2)):
            continue
        lag = found
        lags.append(found)
        placed.append((a, b, found))
        xs.append(x[m])
        rs.append(r[m])
        if m.all():
            f = np.fft.rfftfreq(b - a, 1 / 8000)
            mid, hi = (f >= 300) & (f < 3400), f >= 3400
            for k, v in enumerate((x, r)):
                p = np.abs(np.fft.rfft(v * np.hanning(b - a))) ** 2
                band[k] += p[mid].sum(), p[hi].sum()
            # least squares filter from r to x (normal equations: r's autocorrelation, r by x)
            rp = np.pad(r, TAPS)
            c = np.correlate(rp, x, "valid")
            acf = np.correlate(np.pad(r, (0, 2 * TAPS)), r, "valid")
            i = np.arange(2 * TAPS + 1)
            explained = float(np.sum(c * np.linalg.solve(acf[abs(i[:, None] - i)], c)))
            fit += explained, float(np.sum(x * x)) - explained
    if sum(map(len, rs)) < 0.5 * sum(b - a for a, b in spans):
        return None
    x, r = np.concatenate(xs), np.concatenate(rs)
    g = float(np.sum(x * r) / np.sum(r * r))
    unchanged = bool(np.array_equal(x, r))
    steps = np.diff(lags)
    # each voiced 20 ms of `ref` looked for within ±25 ms of its piece; where none matches, what
    # came in its place: next to nothing, the 20 ms before it again, or something else
    missing = {"frames": 0, "silence": 0, "repeat": 0, "other": 0}
    for a, b, found in placed:
        for f0 in range(a, b - PACKET + 1, PACKET):
            r, pos = r_all[f0 : f0 + PACKET], f0 + found
            if (
                np.sum(r * r) < PACKET * (GATE / 2) ** 2
                or not m_all[max(0, pos - 400) : pos + 560].all()
            ):
                continue
            missing["frames"] += 1
            seg = x_all[max(0, pos - 200) : pos + 360]
            c = np.correlate(seg, r, "valid")
            e = np.convolve(seg * seg, np.ones(PACKET), "valid")
            if np.max(c / np.sqrt(e * np.sum(r * r) + 1e-9)) >= 0.5:
                continue
            x, before = x_all[pos : pos + PACKET], x_all[pos - PACKET : pos]
            if np.sum(x * x) < 1e-3 * g * g * np.sum(r * r):
                missing["silence"] += 1
            elif np.sum(x * before) >= 0.9 * np.sqrt(np.sum(x * x) * np.sum(before**2)):
                missing["repeat"] += 1
            else:
                missing["other"] += 1
    return {
        "gain_db": 20 * math.log10(abs(g)),
        "left_db": math.inf
        if unchanged
        else 10 * math.log10(fit[0] / fit[1])
        if fit.all()
        else None,
        "band_db": 10 * math.log10(band[0, 1] * band[1, 0] / (band[0, 0] * band[1, 1]))
        if band.all()
        else None,
        "moves_ms": [float(s) / 8 for s in steps if abs(s) >= SHIFT],
        "unchanged": unchanged,
        "at": int(np.median(lags)),
        "missing": missing,
    }


def _audio_cells(hs: list[dict[str, Any]]) -> list[str]:
    """unchanged, distortion, moved, gain and 3.4-4 kHz over `heard` results."""
    from rtpbench import cases

    left = [h["left_db"] for h in hs if h["left_db"] is not None]
    bands = [h["band_db"] for h in hs if h["band_db"] is not None]
    moved = [h for h in hs if h["moves_ms"]]
    largest = max((abs(m) for h in moved for m in h["moves_ms"]), default=0)
    return [
        str(sum(h["unchanged"] for h in hs)),
        cases._spread(left, ".1f").replace("inf", "exact") if left else "",
        f"{len(moved)}, up to {largest:.0f} ms" if moved else "0",
        cases._spread([h["gain_db"] for h in hs], "+.1f"),
        cases._spread(bands, "+.1f") if bands else "",
    ]


def downlink(out: Path) -> str:
    """The engine's completed answers as the caller received them in the latency and barge-in
    calls (`heard`), per profile."""
    from rtpbench import analyze, cases

    records = [json.loads(line) for line in (out / "realtime.jsonl").read_text().splitlines()]
    formats = {r["session"]: r["format"] for r in records if r.get("format")}
    answers = [
        r
        for r in records
        if r.get("event") == "answer" and r.get("clip") and r.get("status") == "completed"
    ]
    lines = Lines()
    refs: dict[tuple[str, str | None], list[float]] = {}
    by: dict[str, list[dict[str, Any]]] = {}
    for path in sorted(out.glob("*/*/*/caller.json")):
        if path.parent.name not in ("latency", "barge-in"):
            continue
        st = cases.load(path.parent, path.parts[-4]).audio
        if st is None:
            continue
        times = [t for t in st.times if t is not None]
        ok = [t is not None for t in st.times for _ in range(160)]
        for a in answers:
            if not times[0] <= a["first_audio_ns"] <= times[-1]:
                continue
            k = next(
                i for i, t in enumerate(st.times) if t is not None and t >= a["first_audio_ns"]
            )
            key = a["clip"], formats.get(a["session"])
            if key not in refs:
                refs[key] = sent(lines.clips[key[0]], key[1])
            if (h := heard(refs[key], st.pcm[k * 160 :], ok[k * 160 :])) is not None:
                by.setdefault(path.parts[-4], []).append(h)
    if not by:
        return ""
    rows = [[p, str(len(hs)), *_audio_cells(hs)] for p, hs in by.items()]
    head = [
        "profile",
        "answers",
        "unchanged",
        "distortion, dB",
        "moved",
        "gain, dB",
        "3.4-4 kHz, dB",
    ]
    return (
        "The mock engine's answers as the caller received them (completed answers in the "
        "latency and barge-in calls), median [min, max] over answers. Each piece of speech is "
        "aligned with what the mock sent; for 24 kHz audio, that is its interpolation through an "
        "ideal 8 kHz converter, so the mock's own resampling is not counted. Samples in packets "
        "the network lost are left out. unchanged: answers with every sample as sent. "
        "distortion: the audio against what no linear filter of ±4 ms explains; a resampler or "
        "band filter would leave G.711's own, about 37 dB. moved: answers where a piece came out "
        "5 ms or more later or earlier than the one before (a pause lengthened or shortened, "
        "audio inserted or dropped), and the largest move. gain: least squares. 3.4-4 kHz: that "
        "band against 300-3400 Hz, relative to what was sent.\n\n" + analyze._table(head, rows)
    )


def recording(out: Path, session: str) -> tuple[list[float], list[int], list[int], float] | None:
    """What a session received (`Session.keep`), at 8 kHz: samples, the arrival time of the
    append each sample came in, the 24 kHz samples if it came as pcm16 (else empty), and the
    median audio per append, ms. None without a recording or with appends in more than one
    format."""
    import numpy as np

    idx = out / "realtime" / f"{session}.idx"
    if not idx.exists():
        return None
    rows = [line.split() for line in idx.read_text().splitlines()]
    if not rows or len({r[2] for r in rows}) != 1:
        return None
    fmt, raw = rows[0][2], (out / "realtime" / f"{session}.raw").read_bytes()
    per = 6 if fmt == "pcm16" else 1  # bytes per 8 kHz sample
    starts, n = [], 0
    for r in rows:
        starts += [int(r[0])] * (int(r[1]) // per)
        n += int(r[1])
    each = statistics.median(int(r[1]) / per / 8 for r in rows)
    if fmt == "pcm16":
        pcm24 = np.frombuffer(raw[: n // 2 * 2], dtype="<i2")
        return [float(s) for s in _to8k(np, pcm24)], starts, pcm24.tolist(), each
    law = g711.PCMU if fmt == "pcmu" else g711.PCMA
    return [float(s) for s in g711.decode(law, raw[:n])], starts, [], each


def uplink(out: Path) -> str:
    """The caller's lines in the latency and barge-in calls as this engine received them
    (`heard` against what the caller sent, from its capture), per profile."""
    import numpy as np

    from rtpbench import analyze, cases

    records = [json.loads(line) for line in (out / "realtime.jsonl").read_text().splitlines()]
    sessions = [r["session"] for r in records if r.get("event") == "connect"]
    got = {s: rec for s in sessions if (rec := recording(out, s)) is not None}
    by: dict[str, list[dict[str, Any]]] = {}
    for path in sorted(out.glob("*/*/*/caller.json")):
        if path.parent.name not in ("latency", "barge-in"):
            continue
        w = cases.load(path.parent, path.parts[-4])
        up = [(t, p) for t, p in w.up if (p.pt, p.ssrc) == (w.log["pt"], w.log["ssrc"])]
        if not up:
            continue
        st = analyze.stream(up, w.log["pt"])
        for turn in w.log["turns"]:
            for spans in (turn.get("prompt_speech"), turn["speech"]):
                if not spans:
                    continue
                a, b = st.index(w.log["seq0"], spans[0][0]), st.index(w.log["seq0"], spans[-1][1])
                said = st.time(a, True)
                if said is None:
                    continue
                rec = next((r for r in got.values() if r[1][0] <= said <= r[1][-1]), None)
                if rec is None:
                    continue
                pcm, starts, pcm24, each = rec
                k = max(0, int(np.searchsorted(starts, said)) - 1600)  # from 200 ms before
                rx = pcm[k : k + b - a + 24000]
                h = heard([float(s) for s in st.pcm[a:b]], rx, [True] * len(rx))
                if h is None:
                    continue
                at = k + h["at"]
                if pcm24:
                    x = np.asarray(pcm24[3 * at : 3 * (at + b - a)], dtype=np.float64)
                    f = np.fft.rfftfreq(len(x), 1 / 24000)
                    p = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
                    mid = p[(f >= 300) & (f < 3400)].sum()
                    h["above_db"] = 10 * math.log10(p[f >= 4000].sum() / mid)
                    h["full"] = int(np.sum(np.abs(x) >= 32767))
                else:
                    x = np.asarray(pcm[at : at + b - a])
                    h["full"] = int(np.sum(np.abs(x) >= 32000))
                h["append_ms"] = each
                by.setdefault(path.parts[-4], []).append(h)
    if not by:
        return ""
    rows = []
    for profile, hs in by.items():
        above = [h["above_db"] for h in hs if "above_db" in h]
        full = [h["full"] for h in hs if h["full"]]
        miss = {k: sum(h["missing"][k] for h in hs) for k in hs[0]["missing"]}
        lost = miss["silence"] + miss["repeat"] + miss["other"]
        kinds = ", ".join(f"{miss[k]} {k}" for k in ("silence", "repeat", "other") if miss[k])
        rows.append(
            [
                profile,
                str(len(hs)),
                *_audio_cells(hs),
                cases._spread(above, "+.1f") if above else "",
                f"{len(full)}, up to {max(full)} samples" if full else "0",
                f"{100 * lost / max(1, miss['frames']):.1f}%" + (f": {kinds}" if kinds else ""),
                cases._spread([h["append_ms"] for h in hs], ".0f"),
            ]
        )
    head = [
        "profile",
        "lines",
        "unchanged",
        "distortion, dB",
        "moved",
        "gain, dB",
        "3.4-4 kHz, dB",
        "above 4 kHz, dB",
        "full scale",
        "missing 20 ms",
        "appends, ms",
    ]
    return (
        "The caller's lines in the latency and barge-in calls as the mock engine received them, "
        "aligned piece by piece with what the caller sent (its own capture, before the network), "
        "median [min, max] over lines; the columns as for the engine's audio above. Lost packets "
        "are the target's to fill: what it filled them with counts as distortion, and what it "
        "left out as moved. above 4 kHz: energy above 4 kHz against 300-3400 Hz in 24 kHz audio "
        "(the caller sends none). full scale: lines with samples at full scale. missing 20 ms: the "
        "caller's voiced 20 ms with nothing like them within 25 ms in what the engine got, and "
        "what came in their place: silence, the 20 ms before again (repeat), or other (also "
        "the next audio, where a packet was left out: see moved). appends: the audio each "
        "append carried, the median of each call's.\n\n" + analyze._table(head, rows)
    )
