import asyncio
import base64
import json
import os
import random
import secrets
import struct
import threading
import time
from pathlib import Path
from typing import Any

import pytest

from rtpbench import g711, realtime, speech, voice
from rtpbench.clock import CLOCK

LINES = speech.CORPUS / "lines" / "en"


class Client:
    """The client side of the mock's WebSocket, as a target speaks it."""

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        self.reader, self.writer = reader, writer

    @classmethod
    async def connect(cls, port: int, path: str) -> Client:
        reader, writer = await asyncio.open_connection("127.0.0.1", port)
        key = base64.b64encode(os.urandom(16)).decode()
        writer.write(
            f"GET {path} HTTP/1.1\r\nHost: x\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode()
        )
        head = await reader.readuntil(b"\r\n\r\n")
        assert head.startswith(b"HTTP/1.1 101")
        return cls(reader, writer)

    async def send(self, event: dict[str, Any]) -> None:
        data, mask = json.dumps(event).encode(), secrets.token_bytes(4)
        n = len(data)
        head = struct.pack("!BB", 0x81, 0x80 | (n if n < 126 else 126 if n < 1 << 16 else 127))
        head += b"" if n < 126 else struct.pack("!H" if n < 1 << 16 else "!Q", n)
        self.writer.write(head + mask + bytes(c ^ mask[i % 4] for i, c in enumerate(data)))
        await self.writer.drain()

    async def recv(self) -> dict[str, Any]:
        _, data = await realtime._frame(self.reader)
        event: dict[str, Any] = json.loads(data)
        return event

    async def until(self, kind: str, seen: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        while (e := await self.recv())["type"] != kind:
            if seen is not None:
                seen.append(e)
        return e


@pytest.fixture(scope="module")
def engine(tmp_path_factory: pytest.TempPathFactory) -> tuple[int, Path]:
    out = tmp_path_factory.mktemp("realtime")
    port = 20000 + secrets.randbelow(20000)
    ready = out / "ready"
    threading.Thread(target=realtime.serve, args=(out, port, ready), daemon=True).start()
    deadline = time.monotonic() + 20
    while not ready.exists():
        assert time.monotonic() < deadline
        time.sleep(0.05)
    return port, out


def test_lines_are_told_apart_and_answered() -> None:
    lines = realtime.Lines()
    for name in ("transfer", "prompt-03", "turn-05", "interrupt-01"):
        heard = g711.decode(
            g711.PCMA, g711.encode(g711.PCMA, speech.read_wav(LINES / f"{name}.wav"))
        )
        assert lines.recognise(heard)[0] == name
    assert lines.answer("transfer") == realtime.TOOL
    assert lines.answer("prompt-03") == realtime.LONG
    assert lines.answer("") == realtime.SHORT
    cough = speech.read_wav(speech.CORPUS / "cough-man-0.wav")
    assert lines.answer(lines.recognise(cough)[0]) == realtime.SHORT


def test_lines_are_told_apart_through_packet_loss() -> None:
    """Bursts of lost 20 ms packets, as on lte-bad, either dropped (the rest moves up) or
    concealed (the last packet again at half level), at another level than the line's own."""
    lines, rng = realtime.Lines(), random.Random(7)
    for name in ("transfer", "prompt-05", "turn-11", "turn-01"):
        pcm = g711.decode(g711.PCMA, g711.encode(g711.PCMA, speech.read_wav(LINES / f"{name}.wav")))
        for conceal, gain in ((False, 0.5), (True, 2.0)):
            level = [max(-32768, min(32767, round(s * gain))) for s in pcm]
            heard, bad, last = [], False, [0] * 160
            for i in range(0, len(level), 160):
                bad = rng.random() < (0.52 if bad else 0.032)
                if not bad:
                    heard += (last := level[i : i + 160])
                elif conceal:
                    heard += [s // 2 for s in last]
            assert lines.recognise(heard)[0] == name


async def _aivc(port: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """As AI Voice Connector CE: G.711, a greeting asked for, then the transfer line."""
    c = await Client.connect(port, "/v1/realtime?model=mock")
    assert (await c.recv())["type"] == "session.created"
    fmt = {"type": "audio/pcma"}
    tools = [{"type": "function", "name": realtime.TOOL}]
    session = {"audio": {"input": {"format": fmt}, "output": {"format": fmt}}, "tools": tools}
    await c.send({"type": "session.update", "session": session})
    await c.send({"type": "response.create", "response": {"instructions": "greet"}})
    greeting: list[dict[str, Any]] = []
    done = await c.until("response.done", greeting)
    assert done["response"]["status"] == "completed"
    # the caller asks for a person, in 20 ms packets as RTP brings them, then silence
    pcm = speech.read_wav(LINES / "transfer.wav") + [0] * 16000
    audio = g711.encode(g711.PCMA, pcm)
    for i in range(0, len(audio), 160):
        chunk = base64.b64encode(audio[i : i + 160]).decode()
        await c.send({"type": "input_audio_buffer.append", "audio": chunk})
    turn: list[dict[str, Any]] = []
    await c.until("response.done", turn)
    c.writer.close()
    return greeting, turn


def test_answers_as_the_real_api_does(engine: tuple[int, Path]) -> None:
    port, out = engine
    t0 = CLOCK.now()
    greeting, turn = asyncio.run(_aivc(port))
    kinds = [e["type"] for e in greeting]
    assert kinds[:3] == ["session.updated", "response.created", "response.output_item.added"]
    assert "response.output_audio.delta" in kinds
    assert kinds.index("response.output_audio.delta") > kinds.index("response.content_part.added")
    kinds = [e["type"] for e in turn]
    assert kinds[0] == "input_audio_buffer.speech_started"
    assert "input_audio_buffer.speech_stopped" in kinds
    call = next(e for e in turn if e["type"] == "response.function_call_arguments.done")
    assert call["name"] == realtime.TOOL
    item = next(e for e in turn if e["type"] == "response.output_item.done")["item"]
    assert (item["type"], item["name"], item["arguments"]) == ("function_call", realtime.TOOL, "{}")
    records = [json.loads(line) for line in (out / "realtime.jsonl").read_text().splitlines()]
    answer = next(r for r in records if r.get("trigger") == "turn")
    assert (answer["line"], answer["answer"]) == ("transfer", realtime.TOOL)
    assert t0 < answer["speech_end_ns"] < answer["end_ns"]
    assert answer["end_ns"] - answer["speech_end_ns"] >= realtime.HANGOVER_NS + realtime.DELAY_NS


async def _barge(port: int) -> list[dict[str, Any]]:
    """As LiveKit: 24 kHz PCM16, a long question, then speech while the answer plays."""
    c = await Client.connect(port, "/openai/v1/realtime?model=mock")
    fmt = {"type": "audio/pcm", "rate": 24000}
    session = {"audio": {"input": {"format": fmt}, "output": {"format": fmt}}}
    await c.send({"type": "session.update", "session": session})

    async def say(pcm: list[int]) -> None:  # 8 kHz to 24 kHz, 100 ms chunks, unpaced
        up = b"".join(struct.pack("<3h", s, s, s) for s in pcm)
        for i in range(0, len(up), 4800):
            chunk = base64.b64encode(up[i : i + 4800]).decode()
            await c.send({"type": "input_audio_buffer.append", "audio": chunk})

    await say(speech.read_wav(LINES / "prompt-02.wav") + [0] * 8800)
    seen: list[dict[str, Any]] = []
    await c.until("response.output_audio.delta", seen)
    await say(speech.read_wav(LINES / "interrupt-01.wav")[:4000])  # cut in, half a second
    seen.append(await c.until("response.done", seen))
    c.writer.close()
    return seen


def test_speech_while_answering_cancels_the_answer(engine: tuple[int, Path]) -> None:
    port, out = engine
    events = asyncio.run(_barge(port))
    done = [e for e in events if e["type"] == "response.done"]
    assert done[-1]["response"]["status"] == "cancelled"
    records = [json.loads(line) for line in (out / "realtime.jsonl").read_text().splitlines()]
    answer = [r for r in records if r.get("answer") == realtime.LONG][-1]
    assert (answer["line"], answer["status"]) == ("prompt-02", "cancelled")
    assert any(r["event"] == "barge" for r in records)


def test_heard_measures_the_path_and_leaves_lost_packets_out() -> None:
    pause = [0] * 2400
    ref = voice.voice(1.0, 140) + pause + voice.voice(1.0, 180)
    sent = [float(s) for s in ref]
    # half the level, 20 ms of the pause dropped, one packet of the second stretch lost
    rx = [0] * 300 + [round(s / 2) for s in ref[:8000] + pause[160:] + ref[10400:]]
    ok = [True] * len(rx)
    lost = 300 + 8000 + 2240 + 4000
    rx[lost : lost + 160] = [0] * 160
    ok[lost : lost + 160] = [False] * 160
    rx += [0] * 12000
    ok += [True] * 12000
    h = realtime.heard(sent, rx, ok)
    assert h is not None
    assert h["gain_db"] == pytest.approx(-6.02, abs=0.01)
    assert h["moves_ms"] == [-20.0]
    assert h["left_db"] > 60
    assert not h["unchanged"]
    # G.711 alone leaves the distortion the summary quotes as its own
    law = g711.decode(g711.PCMU, g711.encode(g711.PCMU, ref)) + [0] * 12000
    h = realtime.heard(sent, law, [True] * len(law))
    assert h is not None
    assert 34 < h["left_db"] < 40
    assert h["moves_ms"] == []
