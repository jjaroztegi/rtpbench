"""Scripted caller: speaks fixed-length synthetic turns over a real SIP call."""

import random
import secrets
import socket
import time
from typing import Any

from rtpbench import g711, sip
from rtpbench.rtp import FRAME, PTIME_NS, Receiver, Sender
from rtpbench.voice import GATE, RATE, voice

LEAD_SECONDS = 1.0
UTTERANCE_RANGE = (0.8, 1.6)
GAP_SECONDS = 2.8  # longest delay (1.3 s) + response (0.8 s) + room for netem


def script(turns: int, seed: int) -> tuple[list[int], list[int]]:
    """PCM for the whole call, and the sample index where each turn's speech ends."""
    rng = random.Random(seed)
    pcm, ends = [0] * round(LEAD_SECONDS * RATE), []
    for _ in range(turns):
        pcm += voice(rng.uniform(*UTTERANCE_RANGE), f0=140)
        ends.append(len(pcm))
        pcm += [0] * round(GAP_SECONDS * RATE)
    return pcm, ends


def parse_uri(uri: str) -> tuple[str, int]:
    hostport = uri.split("@", 1)[-1].split(";", 1)[0].removeprefix("sip:")
    host, _, port = hostport.partition(":")
    return host, int(port or 5060)


def call(uri: str, turns: int = 20, seed: int = 1) -> dict[str, Any]:
    """Place the call; return where each turn's speech ended (packet and sample)."""
    peer = parse_uri(uri)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(peer)
    local_ip = sock.getsockname()[0]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 0))
    rtp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rtp.bind(("0.0.0.0", 0))
    dialog = sip.Dialog(sock, peer, uri, local_ip)
    ok = dialog.invite(sip.sdp(local_ip, rtp.getsockname()[1], [g711.PCMU, g711.PCMA]))
    ip, port, pts = sip.parse_sdp(ok.body)
    pt = next(p for p in pts if p in g711.NAMES)

    pcm, ends = script(turns, seed)
    audio = g711.encode(pt, pcm)
    gate = g711.gate(pt, GATE)
    silence = bytes([g711.SILENCE[pt]]) * FRAME
    frames = [audio[i : i + FRAME].ljust(FRAME, silence[:1]) for i in range(0, len(audio), FRAME)]
    seq0, ssrc = secrets.randbelow(1 << 16), secrets.randbelow(1 << 32)
    last = []
    for end in ends:  # last sample the gate calls active, as the agent will see it
        m = gate.search(audio[end - RATE : end][::-1])
        assert m is not None
        idx = end - 1 - m.start()
        last.append({"end_seq": (seq0 + idx // FRAME) & 0xFFFF, "end_off": idx % FRAME})

    start = time.time_ns() + PTIME_NS
    sender = Sender(
        rtp,
        (ip, port),
        pt,
        lambda n, _t: frames[n] if n < len(frames) else silence,
        start,
        seq0,
        ssrc,
    )
    receiver = Receiver(rtp, lambda _a, _p: None)
    sender.start()
    receiver.start()
    hangup_ns = start + len(frames) * PTIME_NS
    remote_bye = False
    while (left := hangup_ns - time.time_ns()) > 0:
        msg = dialog.recv(min(left / 1e9, 0.5))
        if msg is None:
            continue
        if msg.status == 200 and msg.cseq_method == "INVITE":
            dialog.ack()
        elif msg.method:
            dialog.reply(msg)
            if remote_bye := msg.method == "BYE":
                break
    sender.stop.set()
    receiver.stop.set()
    sender.join()
    receiver.join()
    if not remote_bye:
        dialog.bye()
    meta = {"pt": pt, "ssrc": ssrc, "seq0": seq0, "seed": seed, "remote_bye": remote_bye}
    return meta | {"turns": last}
