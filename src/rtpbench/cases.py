"""Conformance cases: scripted calls with a verdict and timings with error bars.

A case is a caller script (a `Session` driven step by step, with `Script` media), a check that
reads only the caller's capture and log, and reference-agent behaviours: one that should pass and
at least one that should fail. Against the reference agent each case runs once per behaviour,
which proves the case itself; against a real target it runs once.

Every timing carries the error bar of the way it is measured, from the calibrations. SIP and RTP
events are capture times (`rtpbench calibrate`: wire timing within 0.41 ms on a clean network);
agent speech onsets are webrtcvad's (`rtpbench calibrate --speech`, p5..p95 per codec).
"""

import itertools
import json
import re
import statistics
import struct
import time
from collections import Counter
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Any, NamedTuple

from rtpbench import analyze, detect, g711, pcap, rtp, sip, speech, speechcal
from rtpbench.agent import BUSY, DIGITS, Behaviour
from rtpbench.caller import Media, Session, speech_utterances

CODECS = (g711.PCMU, g711.PCMA)
QUIET_NS = 1_500_000_000  # agent silence that ends what it was saying
GREETING_WAIT_S = 10.0
GREETING_MAX_MS = 2000  # a caller left in silence longer than this starts saying "hello?"
REPLY_WAIT_S = 15.0
BYE_AFTER_NS = 1_000_000_000  # into the agent's speech
BYE_AUDIBLE_S = 3.0  # then wait this long for a moment the agent is audible
CANCEL_AFTER_S = 0.2  # after the first provisional response
MEDIA_GRACE_MS = 500  # RTP sent before the agent handled a request may still be on its way
WATCH_S = 2.0  # listen after the call ends for media that should have stopped
HOLD_S = 3.0
RESUME_MS = 1000
CLOCK_MS = 40  # RTP clock vs arrival time, before vs after a pause (two packets)
FLOOR_PACKETS = 25  # either side of a pause: the least transit time over 0.5 s, past jitter
SEQ_LOST_MAX = 10  # packets lost in a row where a stream resumes, and it is still the next seq
KEY_MS = 100  # how long the caller holds a key
REFER_WAIT_S = 20.0  # after asking for a person
BYE_WAIT_S = 10.0  # after the transfer is reported done
SIPFRAG = "message/sipfrag;version=2.0"
SESSION_S = 90  # RFC 4028 minimum
TIMER = [("Supported", "timer"), ("Session-Expires", f"{SESSION_S};refresher=uac")]
MEDIA_GAP_MS = 100  # agent RTP paused this long around a refresh: media was disturbed
PTIME_MS = rtp.FRAME / 8
DTMF_MAX_MS = 5000  # an agent that heard the digit says something within this
RETAKE_MAX_MS = 5000  # likewise an agent taking the call back after a failed transfer
REPLY_MAX_MS = 10000  # an agent that heard the question replies by then (AIVC CE slowest: 8.2 s)
_SIP = re.compile(rb"(SIP/2\.0 \d{3} |[A-Z]+ \S+ SIP/2\.0\r\n)")


class Bar(NamedTuple):
    """measured - truth lies within [lo, hi] ms."""

    lo: float
    hi: float
    source: str


LABEL_END = Bar(
    -17.0, 17.0, "caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)"
)
WIRE = Bar(-0.41, 0.41, "capture times; wire timing max abs error, clean (calibrate)")
# speech detection error per netem profile and codec, from the calibrations under that profile;
# a profile without its own calibration (or a target outside the router) takes the clean bar
ONSET = {
    (profile, pt): Bar(lo, hi, f"webrtcvad onset, p5..p95, {g711.NAMES[pt]}, {profile} {how}")
    for profile, pt, lo, hi, how in (
        ("clean", g711.PCMU, -3.8, 32.9, "(calibrate --speech)"),
        ("clean", g711.PCMA, -88.1, 24.3, "(calibrate --speech)"),
        ("lte", g711.PCMU, -3.4, 32.3, "(calibrate --speech --profiles lte)"),
        ("lte", g711.PCMA, -87.6, 25.2, "(calibrate --speech --profiles lte)"),
        ("lte-bad", g711.PCMU, -16.7, 52.5, "(calibrate --speech --profiles lte-bad)"),
        ("lte-bad", g711.PCMA, -96.9, 35.1, "(calibrate --speech --profiles lte-bad)"),
    )
}
STOP = {  # agent stop time on a hard cut, by the gate
    (profile, pt): Bar(lo, hi, f"gate stop time, p5..p95, {g711.NAMES[pt]}, {profile} {how}")
    for profile, pt, lo, hi, how in (
        ("clean", g711.PCMU, -79.2, 0.0, "(calibrate --barge-in --codecs pcmu)"),
        ("clean", g711.PCMA, -71.9, 0.0, "(calibrate --barge-in)"),
        ("lte", g711.PCMU, -71.0, 0.0, "(calibrate --barge-in --codecs pcmu --profiles lte)"),
        ("lte", g711.PCMA, -72.1, 0.0, "(calibrate --barge-in --profiles lte)"),
        (
            "lte-bad",
            g711.PCMU,
            -94.2,
            5.4,
            "(calibrate --barge-in --codecs pcmu --profiles lte-bad)",
        ),
        ("lte-bad", g711.PCMA, -118.8, 0.0, "(calibrate --barge-in --profiles lte-bad)"),
    )
}


def bar(bars: dict[tuple[str, int], Bar], profile: str, pt: int) -> Bar | None:
    """The error bar for this profile and codec, or the clean one."""
    return bars.get((profile, pt)) or bars.get(("clean", pt))


@dataclass
class Timing:
    name: str
    ms: float
    bar: Bar
    truth_ms: float | None = None  # known when the reference agent logged it

    def error(self) -> str:
        """measured - truth, flagged when outside the error bar."""
        if self.truth_ms is None:
            return ""
        e = self.ms - self.truth_ms
        return f"{e:+.1f}" + ("" if self.bar.lo <= e <= self.bar.hi else " (outside the bar)")

    def __str__(self) -> str:  # the true value lies within ms - hi .. ms - lo
        return f"{self.ms:.1f} ms ({-self.bar.hi:+.1f}/{-self.bar.lo:+.1f})"


@dataclass
class Check:
    name: str
    ok: bool | None  # None: the case could not get far enough to tell
    detail: str = ""


@dataclass
class Result:
    checks: list[Check] = field(default_factory=list)
    timings: list[Timing] = field(default_factory=list)

    @property
    def verdict(self) -> str:
        if any(c.ok is False for c in self.checks):
            return "fail"
        return "inconclusive" if any(c.ok is None for c in self.checks) else "pass"


class Script(Media):
    """Caller media for a case: says the clips the script queues, silence otherwise, and keeps
    the agent's speech bursts as the gate hears them (to pace the script, not to measure)."""

    def __init__(self, pt: int, events: int | None = None) -> None:
        super().__init__(pt)
        self.events = events  # telephone-event payload type
        self.keys: list[str] = []  # digits to press
        self.key: dict[str, int] | None = None  # the digit being sent
        self.pressed: list[dict[str, Any]] = []
        self.queue: list[tuple[str, bytes, list[tuple[int, int]]]] = []
        self.said: list[dict[str, Any]] = []
        self.bursts: list[list[int]] = []
        self.muted = False  # send nothing (call inactive)

    def press(self, digit: str) -> None:
        with self.lock:
            self.keys.append(digit)

    def idle(self, n: int) -> bytes | rtp.Frame | None:
        if self.key is None and self.keys and self.events is not None:
            digit = self.keys.pop(0)
            self.key = {"event": DIGITS.index(digit), "ts": n * rtp.FRAME, "dur": 0, "ends": 0}
            self.pressed.append({"digit": digit, "seq_offset": n})
        if (k := self.key) is None or self.events is None:
            return None if self.muted else self.silence
        # RFC 4733: one timestamp per event, duration so far, end bit on the last three
        first = k["dur"] == 0
        k["dur"] = min(k["dur"] + rtp.FRAME, KEY_MS * 8)
        end = k["dur"] == KEY_MS * 8
        k["ends"] += end
        if k["ends"] == 3:
            self.key = None
        payload = struct.pack("!BBH", k["event"], 0x80 * end | 10, k["dur"])
        return rtp.Frame(self.events, payload, k["ts"], first)

    def heard(self, onset: int, end: int) -> None:
        if self.bursts and onset - self.bursts[-1][1] <= analyze.AGENT_GAP_NS:
            self.bursts[-1][1] = max(self.bursts[-1][1], end)
        else:
            self.bursts.append([onset, end])

    def step(self, n: int, tick: int) -> None:
        if self.queue:
            self.said.append(self.play(n, self.queue.pop(0)) | {"tick_ns": tick})

    def say(self, name: str, pcm: list[int]) -> None:
        self.queue.append((name, g711.encode(self.pt, pcm), speech.label(pcm)))

    def busy(self) -> bool:
        with self.lock:
            return bool(self.queue or self.audio or self.keys or self.key)

    def speech_after(self, t_ns: int) -> int | None:
        with self.lock:
            return next((on for on, _ in self.bursts if on > t_ns), None)

    def quiet(self, ns: int = QUIET_NS) -> bool:
        with self.lock:
            return time.time_ns() - self.agent_last >= ns


Dial = Callable[..., Session]
Lines = dict[str, list[int]]  # caller lines by name (prompt, transfer), 8 kHz PCM


def _line(lines: Lines, name: str, seed: int) -> tuple[str, list[int]]:
    """The caller's own line, or else a corpus utterance."""
    return (name, lines[name]) if name in lines else speech_utterances(seed)[0]


def greeting(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    """Answer, listen for the agent's first words and let it finish, hang up."""
    s = dial()
    s.answer()
    m = Script(s.pt)
    s.start(m.source, m.on_packet)
    t0 = time.time_ns()
    if s.wait(lambda: s.remote_bye or m.speech_after(t0) is not None, GREETING_WAIT_S):
        s.wait(lambda: s.remote_bye or m.quiet(), 30)
    s.hangup()
    return s.meta(seed, s.remote_bye) | {"said": m.said}


def _greeting(s: Session, m: Script) -> int | None:
    """When the agent started its greeting, if it greets within GREETING_WAIT_S."""
    t0 = time.time_ns()
    s.wait(lambda: s.remote_bye or m.speech_after(t0) is not None, GREETING_WAIT_S)
    return m.speech_after(t0)


def _settle(s: Session, m: Script) -> None:
    """Let the agent's greeting, if any, start and end: an agent may take a second or two to
    start (one that opens its AI session after answering), so a fixed wait is not enough."""
    _greeting(s, m)
    s.wait(lambda: s.remote_bye or m.quiet(), 30)


def _reply(s: Session, m: Script, seed: int, lines: Lines) -> int | None:
    """Ask a question; when the agent started its reply."""
    m.say(*_line(lines, "prompt", seed))
    s.wait(lambda: s.remote_bye or not m.busy(), 30)
    t1 = time.time_ns()
    s.wait(lambda: s.remote_bye or m.speech_after(t1) is not None, REPLY_WAIT_S)
    return m.speech_after(t1)


def bye(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    """Get the agent talking (its greeting, or else its reply to a question), BYE at least a
    second into it while it is audible, then watch for media. A greeting that ends without such
    a moment gives way to a question."""
    s = dial()
    s.answer()
    m = Script(s.pt)
    s.start(m.source, m.on_packet)

    def into(onset: int) -> bool:
        def audible() -> bool:
            return time.time_ns() >= onset + BYE_AFTER_NS and not m.quiet(analyze.AGENT_GAP_NS)

        return s.wait(lambda: s.remote_bye or audible(), BYE_AFTER_NS / 1e9 + BYE_AUDIBLE_S)

    greeted = _greeting(s, m)
    if greeted is None or not into(greeted):
        s.wait(lambda: s.remote_bye or m.quiet(), 30)
        if (replied := _reply(s, m, seed, lines)) is not None:
            into(replied)
    s.hangup()
    s.wait(lambda: False, WATCH_S)
    return s.meta(seed, s.remote_bye) | {"said": m.said}


def cancel(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    """INVITE, CANCEL it once it rings, then watch for media."""
    s = dial()
    if s.wait(lambda: s.final is not None or s.ringing, 32) and s.final is None:
        if not s.wait(lambda: s.final is not None, CANCEL_AFTER_S):
            s.cancel()
        s.wait(lambda: s.final is not None, 32)
    if s.final is not None and s.final.status < 300:  # answered after all: end it properly
        s.hangup()
    s.wait(lambda: False, WATCH_S)
    return s.meta(seed, s.remote_bye)


def hold(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    """After the greeting: hold (sendonly), resume, hold (inactive), resume; 3 s each."""
    held: list[tuple[str, str | None]] = [("sendonly", None), ("inactive", None)]
    return _hold(dial, seed, [o for h in held for o in (h, ("sendrecv", None))])


def hold_zero(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    """After the greeting: hold the RFC 2543 way (c=0.0.0.0, no direction attribute; RFC 3264
    8.4: an agent MUST be able to receive it, and then sends nothing), resume; 3 s each."""
    return _hold(dial, seed, [("", "0.0.0.0"), ("sendrecv", None)])


def _hold(dial: Dial, seed: int, offers: list[tuple[str, str | None]]) -> dict[str, Any]:
    s = dial()
    s.answer()
    m = Script(s.pt)
    s.start(m.source, m.on_packet)
    _settle(s, m)
    for direction, conn in offers:
        if s.remote_bye:
            break
        m.muted = direction == "inactive"
        s.reinvite(direction, conn=conn)
        s.wait(lambda: s.remote_bye, HOLD_S)
    s.hangup()
    return s.meta(seed, s.remote_bye) | {"said": m.said}


def _dtmf(dial: Dial, seed: int, lines: Lines, info: bool) -> dict[str, Any]:
    """After the greeting, press 5 (RFC 4733 if negotiated, or SIP INFO) and listen."""
    s = dial(dtmf=not info)
    s.answer()
    m = Script(s.pt, s.dtmf)
    s.start(m.source, m.on_packet)
    _settle(s, m)
    t = time.time_ns()
    if info:
        signal = f"Signal=5\r\nDuration={KEY_MS}\r\n".encode()
        s.request("INFO", signal, content_type="application/dtmf-relay")
    elif s.dtmf is not None:
        m.press("5")
        s.wait(lambda: s.remote_bye or not m.busy(), 5)
    if s.wait(lambda: s.remote_bye or m.speech_after(t) is not None, DTMF_MAX_MS / 1000 + 3):
        s.wait(lambda: s.remote_bye or m.quiet(), 30)
    s.hangup()
    return s.meta(seed, s.remote_bye) | {"pressed": m.pressed}


def dtmf_rfc4733(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    return _dtmf(dial, seed, lines, info=False)


def dtmf_info(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    return _dtmf(dial, seed, lines, info=True)


def refer(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    """After the greeting, ask for a person; be the transferee to its REFER: 202, NOTIFY
    sipfrag 100 Trying, call the Refer-To target (the operator answers), NOTIFY its final
    response; wait for the agent to hang up."""
    return _refer(dial, seed, lines)


def refer_fail(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    """As `refer`, but the operator is busy, so the final NOTIFY reports 486 Busy Here. Then
    listen for the agent taking the call back."""
    return _refer(dial, seed, lines, [BUSY])


def _refer(
    dial: Dial, seed: int, lines: Lines, headers: list[tuple[str, str]] | None = None
) -> dict[str, Any]:
    s = dial()
    s.answer()
    m = Script(s.pt)
    s.start(m.source, m.on_packet)
    _settle(s, m)
    m.say(*_line(lines, "transfer", seed))
    s.wait(lambda: s.remote_bye or not m.busy(), 30)
    transfer: dict[str, Any] = {}
    if s.wait(lambda: any(r.method == "REFER" for r in s.requests), REFER_WAIT_S):
        ref = next(r for r in s.requests if r.method == "REFER")
        event = [("Event", "refer")]
        trying = [*event, ("Subscription-State", "active;expires=60")]
        s.request("NOTIFY", b"SIP/2.0 100 Trying\r\n", trying, SIPFRAG)
        # RFC 3515 2.4.2 / RFC 3892: the transferee INVITEs the Refer-To URI, Referred-By copied
        by = [("Referred-By", v) for v in [ref.get("referred-by")] if v]
        t = dial(to=sip.uri_of(ref.get("refer-to")), headers=[*by, *(headers or [])])
        both = (s, t)
        _pump(both, lambda: t.final is not None, 64 * sip.T1)
        frag = t.final.first.removeprefix("SIP/2.0 ") if t.final else "408 Request Timeout"
        transfer = {"uri": t.dialog.target, "call_id": t.dialog.call_id, "final": frag}
        final = [*event, ("Subscription-State", "terminated;reason=noresource")]  # RFC 5589
        s.request("NOTIFY", f"SIP/2.0 {frag}\r\n".encode(), final, SIPFRAG)
        if t.final is not None and t.final.status < 300:
            tm = Media(t.pt)
            t.start(tm.source, tm.on_packet)
        _pump(both, lambda: s.remote_bye, BYE_WAIT_S)
        if t.media:
            t.hangup()
    s.hangup()
    return s.meta(seed, s.remote_bye) | {"said": m.said, "transfer": transfer}


def _pump(calls: tuple[Session, ...], cond: Callable[[], bool], timeout: float) -> bool:
    """`Session.wait` over several calls at once."""
    deadline = time.monotonic() + timeout
    while not cond():
        if time.monotonic() >= deadline:
            return False
        for c in calls:
            c.pump(0.01)
    return True


def _codec(dial: Dial, seed: int, lines: Lines, pt: int) -> dict[str, Any]:
    """Offer one G.711 law only; listen to the agent's greeting (or its reply to a question)."""
    s = dial(codecs=(pt,))
    s.answer()
    m = Script(s.pt)
    s.start(m.source, m.on_packet)
    if _greeting(s, m) is None:
        _reply(s, m, seed, lines)
    s.wait(lambda: s.remote_bye, 1.0)
    s.hangup()
    return s.meta(seed, s.remote_bye) | {"offered": [pt], "said": m.said}


def codec_pcmu(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    return _codec(dial, seed, lines, g711.PCMU)


def codec_pcma(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    return _codec(dial, seed, lines, g711.PCMA)


def timer(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    """Offer session timers (90 s, refresher=uac), refresh once at half time, then stop
    refreshing and wait for the agent to end the expired session."""
    s = dial(headers=[*TIMER, ("Min-SE", str(SESSION_S))])
    ok = s.answer()
    m = Script(s.pt)
    s.start(m.source, m.on_packet)
    expires = ok.get("session-expires")
    interval = int(expires.split(";")[0]) if expires else 0
    if interval:
        s.wait(lambda: s.remote_bye, interval / 2)
        if not s.remote_bye:
            s.reinvite(headers=[("Supported", "timer"), ("Session-Expires", expires)])
        s.wait(lambda: s.remote_bye, interval + 5)
    else:
        s.wait(lambda: s.remote_bye, 2.0)
    s.hangup()
    return s.meta(seed, s.remote_bye)


def _carried(
    dial: Dial,
    seed: int,
    lines: Lines,
    mutation: str | None = None,
    midway: Callable[[Session, Script], Any] | None = None,
) -> dict[str, Any]:
    """Through what a carrier sends: after the greeting (and `midway`, if given) ask a question
    and listen for the reply. `mutation` asks the carrier for one, in an X-Mutation header it
    removes."""
    s = dial(headers=[("X-Mutation", mutation)] if mutation else None)
    s.answer()
    m = Script(s.pt)
    s.start(m.source, m.on_packet)
    _settle(s, m)
    if midway and not s.remote_bye:
        midway(s, m)
    _reply(s, m, seed, lines)
    s.wait(lambda: s.remote_bye, 1.0)
    s.hangup()
    return s.meta(seed, s.remote_bye) | {"said": m.said}


def compact_headers(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    return _carried(dial, seed, lines, "compact-headers")


def sdp_ssrc(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    return _carried(dial, seed, lines, "sdp-ssrc")


def late_offer(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    return _carried(dial, seed, lines, "late-offer")


def ptime_30(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    return _carried(dial, seed, lines, "ptime-30")


def ssrc_change(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    """The caller's stream becomes a new RTP source before the question (the carrier relays
    it as it comes)."""
    return _carried(dial, seed, lines, midway=lambda s, m: s.switch())


def reinvite(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    """A session refresh before the question: re-INVITE with the same SDP (RFC 4028 sends one
    every half interval; carriers typically every 15 min)."""
    return _carried(dial, seed, lines, midway=lambda s, m: s.reinvite())


def reinvite_nosdp(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    """A re-INVITE without SDP before the question (RFC 3261 14.1: the 2xx offers, the ACK
    answers), as PBXs send one to move or audit the media."""
    return _carried(dial, seed, lines, midway=lambda s, m: s.reinvite(offer=False))


def codec_change(dial: Dial, seed: int, lines: Lines) -> dict[str, Any]:
    """Before the question a re-INVITE offers the other G.711 law alone; on its 2xx the caller
    speaks and listens in it (a leg moved to another gateway, a transfer to another trunk)."""

    def change(s: Session, m: Script) -> None:
        law = g711.PCMU if s.pt == g711.PCMA else g711.PCMA
        resp = s.reinvite(pt=law)
        if resp is not None and resp.status < 300:
            m.recodec(law)

    return _carried(dial, seed, lines, midway=change)


@dataclass
class Wire:
    """One case call as the caller's capture saw it, plus the logs."""

    log: dict[str, Any]  # caller.json
    agent: dict[str, Any] | None  # agent.json, from the reference agent only
    msgs: list[tuple[int, bool, sip.Message]]  # capture time, sent by the caller, message
    up: analyze.Timed  # RTP the caller sent
    down: analyze.Timed  # RTP the caller received
    profile: str = "clean"  # netem profile, for the error bars

    def onset(self) -> Bar:
        """Error bar of the agent's speech onsets."""
        b = bar(ONSET, self.profile, self.log["pt"])
        assert b is not None  # every codec has a clean bar
        return b

    def find(
        self, pred: Callable[[sip.Message], bool], sent: bool, after: int | None = None
    ) -> tuple[int, sip.Message] | None:
        """First message sent (or received) after `after` matching `pred`."""
        return next(
            (
                (t, m)
                for t, out, m in self.msgs
                if out == sent and (after is None or t > after) and pred(m)
            ),
            None,
        )

    @cached_property
    def audio(self) -> analyze.Stream | None:
        pkts = [(t, p) for t, p in self.down if p.pt == self.log.get("pt")]
        return analyze.stream(pkts, self.log["pt"]) if pkts else None

    @cached_property
    def speech(self) -> list[tuple[int, int]]:
        """Agent speech (webrtcvad) as [onset, end] capture times."""
        st = self.audio
        if st is None:
            return []
        spans = [(st.time(a, True), st.time(b - 1, False)) for a, b in detect.webrtc(st.pcm)]
        return [(a, b) for a, b in spans if a is not None and b is not None]

    def speech_after(self, t: int) -> int | None:
        return next((a for a, _ in self.speech if a > t), None)

    def said(self) -> tuple[int, int] | None:
        """First and last labelled sample of the caller's last line, as captured (from the
        stream it was said on)."""
        pkts = [(t, p) for t, p in self.up if (p.pt, p.ssrc) == (self.log["pt"], self.log["ssrc"])]
        if not pkts or not self.log.get("said"):
            return None
        st, s0 = analyze.stream(pkts, self.log["pt"]), self.log["seq0"]
        spans = self.log["said"][-1]["speech"]
        return speechcal._truth(st, [(st.index(s0, a), st.index(s0, b)) for a, b in spans])

    def truth(self, kind: str) -> tuple[int, int] | None:
        """Labelled first and last sample of the reference agent's `kind` reply, as captured;
        None unless the stream arrived as the agent sent it (a carrier that rewrote its SSRC
        may have renumbered it too)."""
        turns = self.agent["turns"] if self.agent else []
        turn = next((u for u in turns if u.get("kind") == kind), None)
        if (st := self.audio) is None or turn is None or self.agent is None:
            return None
        if any(p.ssrc != self.agent["ssrc"] for _, p in self.down if p.pt == self.log["pt"]):
            return None
        a0 = self.agent["seq0"]
        return speechcal._truth(st, [(st.index(a0, a), st.index(a0, b)) for a, b in turn["speech"]])


def load(run: Path, profile: str = "clean") -> Wire:
    log = json.loads((run / "caller.json").read_text())
    agent_path = run / "agent.json"
    agent = json.loads(agent_path.read_text()) if agent_path.exists() else None
    msgs: list[tuple[int, bool, sip.Message]] = []
    up: analyze.Timed = []
    down: analyze.Timed = []
    me, port = "", log.get("rtp_port")
    for g in pcap.read(run / "caller.pcap"):
        if _SIP.match(g.payload):
            msg = sip.parse(g.payload)
            if msg.get("call-id") != log.get("call_id"):
                continue
            me = me or g.src  # the caller sends the first message, its INVITE
            msgs.append((g.t_ns, g.src == me, msg))
        elif port in (g.sport, g.dport) and (p := rtp.parse(g.payload)) is not None:
            (up if g.sport == port else down).append((g.t_ns, p))
    return Wire(log, agent, msgs, up, down, profile)


def _is_2xx_invite(m: sip.Message) -> bool:
    return 200 <= m.status < 300 and m.cseq_method == "INVITE"


def check_greeting(w: Wire) -> Result:
    r = Result()
    ok = w.find(_is_2xx_invite, sent=False)
    r.checks.append(Check("call answered", ok is not None))
    if ok is None:
        return r
    onset = w.speech_after(ok[0])
    r.checks.append(Check("agent speaks first", onset is not None))
    if onset is None:
        return r
    ms = (onset - ok[0]) / 1e6
    truth = w.truth("greeting")
    truth_ms = None if truth is None else (truth[0] - ok[0]) / 1e6
    r.timings.append(Timing("200 OK to agent speech", ms, w.onset(), truth_ms))
    r.checks.append(Check(f"agent speaks within {GREETING_MAX_MS} ms", ms <= GREETING_MAX_MS))
    return r


def _final(method: str) -> Callable[[sip.Message], bool]:
    return lambda m: m.status >= 200 and m.cseq_method == method


def check_bye(w: Wire) -> Result:
    r = Result()
    bye = w.find(lambda m: m.method == "BYE", sent=True)
    if bye is None:
        r.checks.append(Check("caller hung up", None, "the agent hung up first"))
        return r
    t = bye[0]
    talking = any(a <= t <= b + analyze.AGENT_GAP_NS for a, b in w.speech)
    r.checks.append(Check("agent was talking at the BYE", talking or None))
    ok = w.find(_final("BYE"), sent=False)
    r.checks.append(
        Check("BYE answered 2xx", ok is not None and ok[1].status < 300, ok[1].first if ok else "")
    )
    if ok:
        r.timings.append(Timing("BYE to its response", (ok[0] - t) / 1e6, WIRE))
    if w.down:
        ms = (w.down[-1][0] - t) / 1e6
        r.timings.append(Timing("BYE to the agent's last RTP", ms, WIRE))
        r.checks.append(Check(f"agent RTP stops within {MEDIA_GRACE_MS} ms", ms <= MEDIA_GRACE_MS))
    return r


def check_cancel(w: Wire) -> Result:
    r = Result()
    cancel = w.find(lambda m: m.method == "CANCEL", sent=True)
    if cancel is None:
        ringing = w.find(lambda m: m.cseq_method == "INVITE" and m.status < 200, sent=False)
        final = w.find(_final("INVITE"), sent=False)
        detail = "no provisional response first"
        if ringing and final:
            ms = (final[0] - ringing[0]) / 1e6
            detail = f"final response {ms:.0f} ms after the first provisional, before a CANCEL"
        r.checks.append(Check("CANCEL sent while ringing", None, detail))
        return r
    t = cancel[0]
    ok = w.find(_final("CANCEL"), sent=False)
    r.checks.append(
        Check(
            "CANCEL answered 2xx", ok is not None and ok[1].status < 300, ok[1].first if ok else ""
        )
    )
    final = w.find(_final("INVITE"), sent=False)
    if final is None:
        r.checks.append(Check("INVITE ended 487", False, "no final response"))
    elif final[1].status < 300 and ok is not None and final[0] < ok[0]:
        r.checks.append(Check("INVITE ended 487", None, "answered before the CANCEL arrived"))
    else:
        r.checks.append(Check("INVITE ended 487", final[1].status == 487, final[1].first))
        r.timings.append(
            Timing("CANCEL to the INVITE's final response", (final[0] - t) / 1e6, WIRE)
        )
    late = [u for u, _ in w.down if u > t + MEDIA_GRACE_MS * 1_000_000]
    r.checks.append(Check("no agent RTP after the CANCEL", not late, f"{len(late)} packets"))
    return r


def _final_to(req: sip.Message) -> Callable[[sip.Message], bool]:
    return lambda m: m.branch == req.branch and m.cseq_method == req.method and m.status >= 200


def _floor(pkts: analyze.Timed, ts0: int) -> float:
    """Least arrival time minus RTP time (ms, timestamps relative to `ts0`) over `pkts`: the
    sender's clock against the capture's, with the path's base delay and without its jitter.
    Comparing it across a pause shows whether the RTP clock kept time; one packet each side
    would carry two packets' jitter."""
    return min(u / 1e6 - analyze.signed(p.ts - ts0, 32) / 8 for u, p in pkts)


# answers to a hold offer that honour it (RFC 3264 6.1: inactive is fine for sendonly; 8.4 asks
# nothing of the answer to c=0.0.0.0, only that the answerer sends nothing)
HOLD_ANSWERS = {
    "sendonly": ("recvonly", "inactive"),
    "inactive": ("inactive",),
    "c=0.0.0.0": sip.DIRECTIONS,
}


def check_hold(w: Wire) -> Result:
    """Per hold and resume: 2xx with an answer that honours the offer, no agent RTP while held,
    RTP back within 1 s of the resume, and the same RTP stream: SSRC, next seq, timestamps that
    kept time (RFC 3550 5.1)."""
    r = Result()
    sent: dict[str, tuple[int, sip.Message]] = {}
    for t, out, m in w.msgs:
        if out and m.method == "INVITE":
            sent.setdefault(m.branch, (t, m))
    reinvites = list(sent.values())[1:]
    if len(reinvites) < 2:
        r.checks.append(Check("hold and resume sent", None, "the call ended first"))
        return r
    for (t_hold, held), (t_back, back) in zip(reinvites[::2], reinvites[1::2], strict=False):
        sdp = sip.parse_sdp(held.body)
        offer = "c=0.0.0.0" if sdp.ip == "0.0.0.0" else sdp.direction
        answers = []
        for t, req, want in ((t_hold, held, HOLD_ANSWERS[offer]), (t_back, back, ("sendrecv",))):
            what = f"{offer} hold" if req is held else f"resume from {offer}"
            resp = w.find(_final_to(req), sent=False)
            ok = resp is not None and resp[1].status < 300
            r.checks.append(Check(f"{what}: 2xx", ok, resp[1].first if resp else "no response"))
            if resp is None or not ok:
                return r
            r.timings.append(Timing(f"{what}: re-INVITE to 2xx", (resp[0] - t) / 1e6, WIRE))
            got = sip.parse_sdp(resp[1].body).direction
            r.checks.append(Check(f"{what}: answer {' or '.join(want)}", got in want, got))
            answers.append(resp[0])
        grace = MEDIA_GRACE_MS * 1_000_000
        during = [u for u, _ in w.down if answers[0] + grace < u < t_back]
        r.checks.append(Check(f"{offer} hold: no agent RTP", not during, f"{len(during)} packets"))
        if during:
            continue  # it never paused, so there is no resume to time
        before = [(u, p) for u, p in w.down if u < t_back]
        after = [(u, p) for u, p in w.down if u > t_back]
        if not after or not before:
            r.checks.append(Check(f"resume from {offer}: agent RTP again", False))
            continue
        # by sequence, not arrival: the edges of the pause may arrive reordered
        p0, p1 = analyze.by_seq(before)[-1][1], analyze.by_seq(after)[0][1]
        ms = (after[0][0] - answers[1]) / 1e6
        r.timings.append(Timing(f"resume from {offer}: 2xx to agent RTP", ms, WIRE))
        r.checks.append(
            Check(f"resume from {offer}: agent RTP within {RESUME_MS} ms", ms <= RESUME_MS)
        )
        drift = _floor(before[-FLOOR_PACKETS:], p0.ts) - _floor(after[:FLOOR_PACKETS], p0.ts)
        r.timings.append(Timing(f"resume from {offer}: RTP clock drift", drift, WIRE))
        lost = (p1.seq - p0.seq - 1) & 0xFFFF  # packets missing at the resume
        same = p1.ssrc == p0.ssrc and lost <= SEQ_LOST_MAX and abs(drift) <= CLOCK_MS
        detail = f"ssrc {p0.ssrc:#x}->{p1.ssrc:#x}, seq {p0.seq}->{p1.seq}, clock {drift:+.0f} ms"
        r.checks.append(Check(f"resume from {offer}: same RTP stream", same, detail))
    return r


def _reaction(w: Wire, r: Result, t: int) -> Result:
    """The agent's first speech after a digit at `t`."""
    onset = w.speech_after(t)
    r.checks.append(
        Check(
            f"agent reacts within {DTMF_MAX_MS} ms",
            onset is not None and onset - t <= DTMF_MAX_MS * 1e6,
        )
    )
    if onset is not None:
        truth = w.truth("dtmf")
        truth_ms = None if truth is None else (truth[0] - t) / 1e6
        r.timings.append(Timing("digit to agent speech", (onset - t) / 1e6, w.onset(), truth_ms))
    return r


def check_dtmf_rfc4733(w: Wire) -> Result:
    """telephone-event in the answer; the agent reacts to the digit (timed from the first
    packet with the end bit)."""
    r = Result()
    ok = w.find(_is_2xx_invite, sent=False)
    pt = sip.parse_sdp(ok[1].body).dtmf if ok else None
    r.checks.append(Check("telephone-event negotiated", pt is not None))
    end = next(
        (t for t, p in w.up if p.pt == pt and len(p.payload) >= 4 and p.payload[1] & 0x80), None
    )
    if pt is None or end is None:
        return r
    return _reaction(w, r, end)


def check_dtmf_info(w: Wire) -> Result:
    """INFO answered 2xx; the agent reacts to the digit (timed from the INFO)."""
    r = Result()
    info = w.find(lambda m: m.method == "INFO", sent=True)
    if info is None:
        r.checks.append(Check("INFO sent", None))
        return r
    resp = w.find(_final_to(info[1]), sent=False)
    r.checks.append(
        Check(
            "INFO answered 2xx",
            resp is not None and resp[1].status < 300,
            resp[1].first if resp else "no response",
        )
    )
    if resp:
        r.timings.append(Timing("INFO to its response", (resp[0] - info[0]) / 1e6, WIRE))
    return _reaction(w, r, info[0])


def check_refer(w: Wire) -> Result:
    """A REFER with a SIP or tel Refer-To, both NOTIFYs answered 2xx (the subscription outlives
    a BYE, RFC 5057), and the agent hangs up within 10 s of the final NOTIFY."""
    r = Result()
    if (last := _transfer(w, r)) is None:
        return r
    bye = w.find(lambda m: m.method == "BYE", sent=False)
    in_time = bye is not None and bye[0] - last <= BYE_WAIT_S * 1e9
    r.checks.append(Check(f"agent hangs up within {BYE_WAIT_S:.0f} s", in_time))
    if bye:
        r.timings.append(Timing("final NOTIFY to agent BYE", (bye[0] - last) / 1e6, WIRE))
    return r


def check_refer_fail(w: Wire) -> Result:
    """As `check_refer` up to the NOTIFYs; then, the transfer having failed, the agent takes the
    call back (RFC 5589 6.3: the transferor resumes the session): no BYE for 10 s, and speech
    that starts within 5 s of the failure NOTIFY."""
    r = Result()
    if (last := _transfer(w, r)) is None:
        return r
    bye = w.find(lambda m: m.method == "BYE", sent=False)
    keeps = bye is None or bye[0] - last > BYE_WAIT_S * 1e9
    detail = "" if bye is None else f"BYE {(bye[0] - last) / 1e6:.0f} ms after it"
    r.checks.append(Check(f"agent keeps the call for {BYE_WAIT_S:.0f} s", keeps, detail))
    onset = w.speech_after(last)
    spoke = onset is not None and onset - last <= RETAKE_MAX_MS * 1e6
    r.checks.append(Check(f"agent speaks within {RETAKE_MAX_MS} ms", spoke and keeps))
    if onset is not None and (bye is None or onset < bye[0]):
        truth = w.truth("retake")
        truth_ms = None if truth is None else (truth[0] - last) / 1e6
        ms = (onset - last) / 1e6
        r.timings.append(Timing("failure NOTIFY to agent speech", ms, w.onset(), truth_ms))
    return r


def _transfer(w: Wire, r: Result) -> int | None:
    """The REFER and the NOTIFYs that report on it; when the last NOTIFY went (the REFER's time
    if none did), or None without a REFER."""
    ref = w.find(lambda m: m.method == "REFER", sent=False)
    r.checks.append(Check("agent transfers (REFER)", ref is not None))
    if ref is None:
        return None
    said = w.said()
    if said:
        r.timings.append(Timing("end of the request to REFER", (ref[0] - said[1]) / 1e6, LABEL_END))
    target = sip.uri_of(ref[1].get("refer-to"))
    r.checks.append(
        Check("Refer-To is a SIP or tel URI", target.startswith(("sip:", "sips:", "tel:")), target)
    )
    sent: dict[str, tuple[int, sip.Message]] = {}  # first copy of each NOTIFY
    for t, out, m in w.msgs:
        if out and m.method == "NOTIFY":
            sent.setdefault(m.branch, (t, m))
    notifies = list(sent.values())
    for _, n in notifies:
        resp = w.find(_final_to(n), sent=False)
        what = n.body.decode(errors="replace").strip()
        r.checks.append(
            Check(
                f"NOTIFY ({what}) answered 2xx",
                resp is not None and resp[1].status < 300,
                resp[1].first if resp else "no response",
            )
        )
    return notifies[-1][0] if notifies else ref[0]


def check_codec(w: Wire) -> Result:
    """The offer had one G.711 law: answered 2xx with that format alone (RFC 3264 6.1: the
    answer's formats MUST come from the offer), and the agent's RTP carries it."""
    r = Result()
    pt = w.log["offered"][0]
    name = g711.NAMES[pt]
    ok = w.find(_is_2xx_invite, sent=False)
    r.checks.append(Check(f"{name}-only offer answered 2xx", ok is not None))
    if ok is None:
        return r
    answer = sip.parse_sdp(ok[1].body).pts
    r.checks.append(Check(f"answer has {name} alone", answer == [pt], " ".join(map(str, answer))))
    got = sorted({p.pt for _, p in w.down})
    detail = " ".join(map(str, got)) or "no agent RTP"
    r.checks.append(Check(f"agent RTP is {name}", got == [pt], f"payload types {detail}"))
    return r


def check_timer(w: Wire) -> Result:
    """RFC 4028: the 2xx takes the timer (Session-Expires, refresher=uac kept, Require: timer);
    the refresh is answered 2xx with media undisturbed; the agent, not refreshed again, sends
    BYE after half the interval and before it expires."""
    r = Result()
    ok = w.find(_is_2xx_invite, sent=False)
    expires = ok[1].get("session-expires") if ok else ""
    r.checks.append(Check("Session-Expires in the 2xx", bool(expires), "timers not supported"))
    if not ok or not expires:
        return r
    interval = int(expires.split(";")[0])
    kept = sip.param(expires, "refresher") == "uac" and "timer" in ok[1].get("require")
    r.checks.append(Check("refresher=uac kept, Require: timer", kept, expires))
    invites: dict[str, tuple[int, sip.Message]] = {}
    for t, out, m in w.msgs:
        if out and m.method == "INVITE":
            invites.setdefault(m.branch, (t, m))
    refresh = list(invites.values())[1:2]
    if not refresh:
        r.checks.append(Check("refresh sent", None, "the call ended first"))
        return r
    if (resp_t := _refreshed(w, r, refresh[0])) is None:
        return r
    bye = w.find(lambda m: m.method == "BYE", sent=False)
    after = None if bye is None else (bye[0] - resp_t) / 1e9
    in_window = after is not None and interval / 2 < after <= interval
    r.checks.append(
        Check(f"agent ends the session in ({interval / 2:.0f}, {interval}] s", in_window)
    )
    if bye:
        r.timings.append(Timing("refresh 2xx to agent BYE", (bye[0] - resp_t) / 1e6, WIRE))
    return r


def _refreshed(w: Wire, r: Result, sent: tuple[int, sip.Message]) -> int | None:
    """A refresh re-INVITE: answered 2xx (sendrecv) with the agent's media undisturbed; when
    the 2xx came, or None if it did not."""
    t, req = sent
    resp = w.find(_final_to(req), sent=False)
    good = resp is not None and resp[1].status < 300
    r.checks.append(Check("refresh answered 2xx", good, resp[1].first if resp else "no response"))
    if not resp or not good:
        return None
    r.timings.append(Timing("refresh re-INVITE to 2xx", (resp[0] - t) / 1e6, WIRE))
    got = sip.parse_sdp(resp[1].body).direction
    r.checks.append(Check("refresh answer sendrecv", got == "sendrecv", got))
    # on the sender's clock, so that network jitter and loss do not read as a disturbance: time
    # its RTP clock skipped between packets, and how far its clock moved against arrival times
    byes = [u for u, _, m in w.msgs if m.method == "BYE" and u > resp[0]]
    end = min([resp[0] + 2_000_000_000, *byes])
    near = [(u, p) for u, p in w.down if t - 1e9 <= u <= end]
    ssrcs = len({p.ssrc for _, p in near})
    skipped = max(
        (
            analyze.signed(b.ts - a.ts, 32) / 8 - analyze.signed(b.seq - a.seq, 16) * PTIME_MS
            for a, b in itertools.pairwise(p for _, p in near)
        ),
        default=0.0,
    )
    pre, post = [x for x in near if x[0] < t], [x for x in near if x[0] > resp[0]]
    shift = _floor(post, near[0][1].ts) - _floor(pre, near[0][1].ts) if pre and post else 0
    detail = f"clock skipped {skipped:.0f} ms, moved {shift:+.0f} ms, {ssrcs} SSRC"
    # and it goes on: a stream that stops leaves no gap between the packets it did send
    goes_on = bool(post) and end - post[-1][0] <= MEDIA_GRACE_MS * 1e6
    if not goes_on:
        stop = (post[-1][0] if post else resp[0]) - resp[0]
        detail = f"agent RTP stops {stop / 1e6:.0f} ms after the 2xx"
    calm = ssrcs == 1 and goes_on and skipped <= MEDIA_GAP_MS and abs(shift) <= MEDIA_GAP_MS
    r.checks.append(Check("media undisturbed by the refresh", calm, detail))
    return resp[0]


def check_carried(w: Wire) -> Result:
    """Whatever the carrier did, the call works: answered 2xx, and the agent replies to a
    question asked after it within 10 s (so each side hears the other)."""
    r = Result()
    r.checks.append(Check("call answered 2xx", w.find(_is_2xx_invite, sent=False) is not None))
    return _replies(w, r)


def check_ssrc_change(w: Wire) -> Result:
    """As `check_carried`, the caller's audio having switched to a new RTP source first."""
    r = Result()
    ssrcs = {p.ssrc for _, p in w.up if p.pt == w.log["pt"]}
    r.checks.append(Check("caller's RTP switched source", len(ssrcs) == 2 or None, f"{len(ssrcs)}"))
    return _replies(w, r)


def check_reinvite(w: Wire) -> Result:
    """A refresh re-INVITE with unchanged SDP: 2xx sendrecv, agent media undisturbed (as for
    `timer`); then the agent still replies to a question within 10 s."""
    r = Result()
    invites: dict[str, tuple[int, sip.Message]] = {}
    for t, out, m in w.msgs:
        if out and m.method == "INVITE":
            invites.setdefault(m.branch, (t, m))
    refresh = list(invites.values())[1:2]
    if not refresh:
        r.checks.append(Check("refresh sent", None, "the call ended first"))
        return r
    if not refresh[0][1].body:  # the 2xx offers (RFC 3261 14.1), overlapping the session (14.2)
        resp = w.find(_final_to(refresh[0][1]), sent=False)
        first = w.find(_is_2xx_invite, sent=False)
        before = set(sip.parse_sdp(first[1].body).pts) if first else set()
        got = sip.parse_sdp(resp[1].body).pts if resp else []
        detail = " ".join(map(str, got)) or "no SDP"
        r.checks.append(Check("2xx offers the call's codec", bool(before & set(got)), detail))
    if _refreshed(w, r, refresh[0]) is None:
        return r
    return _replies(w, r)


def check_codec_change(w: Wire) -> Result:
    """A re-INVITE offering the other G.711 law alone: 2xx with that law alone (RFC 3264 6.1),
    agent RTP in it from then on, and the agent replies to a question asked in it within 10 s."""
    r = Result()
    invites: dict[str, tuple[int, sip.Message]] = {}
    for t, out, m in w.msgs:
        if out and m.method == "INVITE":
            invites.setdefault(m.branch, (t, m))
    change = list(invites.values())[1:2]
    if not change:
        r.checks.append(Check("codec change sent", None, "the call ended first"))
        return r
    law = sip.parse_sdp(change[0][1].body).pts[0]
    name = g711.NAMES[law]
    resp = w.find(_final_to(change[0][1]), sent=False)
    ok = resp is not None and resp[1].status < 300
    r.checks.append(Check(f"{name} re-INVITE answered 2xx", ok, resp[1].first if resp else ""))
    if resp is None or not ok:
        return r
    answer = sip.parse_sdp(resp[1].body).pts
    r.checks.append(Check(f"answer has {name} alone", answer == [law], " ".join(map(str, answer))))
    after = {p.pt for u, p in w.down if u > resp[0] + MEDIA_GRACE_MS * 1e6}
    detail = "payload types " + (" ".join(map(str, sorted(after))) or "none")
    r.checks.append(Check(f"agent RTP is {name} after it", after == {law}, detail))
    return _replies(w, r)


def _replies(w: Wire, r: Result) -> Result:
    """The agent's reply to the caller's question: speech within REPLY_MAX_MS of its end."""
    said = w.said()
    if said is None:
        r.checks.append(Check("question asked", None, "the call ended first"))
        return r
    onset = w.speech_after(said[1])
    in_time = onset is not None and onset - said[1] <= REPLY_MAX_MS * 1e6
    r.checks.append(Check(f"agent replies within {REPLY_MAX_MS} ms", in_time))
    if onset is not None:
        truth = w.truth("reply")
        truth_ms = None if truth is None else (truth[0] - said[1]) / 1e6
        ms = (onset - said[1]) / 1e6
        r.timings.append(Timing("end of the question to agent speech", ms, w.onset(), truth_ms))
    return r


@dataclass(frozen=True)
class Case:
    """A caller script, its check, and the reference agent behaviours that pass and fail it."""

    script: Callable[[Dial, int, Lines], dict[str, Any]]
    check: Callable[[Wire], Result]
    good: Behaviour
    bad: dict[str, Behaviour]
    # "carrier": only through the carrier (it applies what the case tests); "direct": never
    # through it (it would hide what the case tests); else either way
    route: str = ""

    def behaviours(self) -> dict[str, Behaviour]:
        return {"good": self.good} | self.bad


CASES = {
    "greeting": Case(
        greeting,
        check_greeting,
        Behaviour(greet_s=0.8),
        {"late": Behaviour(greet_s=3.0), "silent": Behaviour()},
    ),
    "bye": Case(
        bye,
        check_bye,
        Behaviour(greet_s=0.5, greeting="long"),
        {"linger": Behaviour(greet_s=0.5, greeting="long", linger_s=3.0)},
    ),
    "cancel": Case(
        cancel,
        check_cancel,
        Behaviour(ring_s=3.0),
        {"answers": Behaviour(ring_s=3.0, cancel=False)},
    ),
    "hold": Case(
        hold,
        check_hold,
        Behaviour(),
        {"ignore": Behaviour(hold=False), "clock": Behaviour(clock=False)},
    ),
    "dtmf-rfc4733": Case(
        dtmf_rfc4733, check_dtmf_rfc4733, Behaviour(dtmf_s=0.8), {"deaf": Behaviour()}
    ),
    "dtmf-info": Case(dtmf_info, check_dtmf_info, Behaviour(dtmf_s=0.8), {"deaf": Behaviour()}),
    "refer": Case(
        refer,
        check_refer,
        Behaviour(refer_s=1.5),
        {
            "stays": Behaviour(refer_s=1.5, transfer="stay"),
            "early": Behaviour(refer_s=1.5, transfer="early"),
        },
    ),
    "refer-fail": Case(
        refer_fail,
        check_refer_fail,
        Behaviour(refer_s=1.5, retake_s=0.8),
        {
            "hangs-up": Behaviour(refer_s=1.5, transfer="always"),
            "silent": Behaviour(refer_s=1.5),
        },
    ),
    "codec-pcmu": Case(
        codec_pcmu,
        check_codec,
        Behaviour(greet_s=0.5),
        {"pcma-anyway": Behaviour(greet_s=0.5, codec=g711.PCMA)},
        route="direct",  # rtpengine transcodes a wrong-law answer to the offered law
    ),
    "codec-pcma": Case(
        codec_pcma,
        check_codec,
        Behaviour(greet_s=0.5),
        {"pcmu-anyway": Behaviour(greet_s=0.5, codec=g711.PCMU)},
        route="direct",
    ),
    "timer": Case(
        timer,
        check_timer,
        Behaviour(timer=True),
        {"unsupported": Behaviour(), "no-expiry": Behaviour(timer=True, expire=False)},
    ),
    # what a carrier sends; the agent greets and answers the caller's question
    "compact-headers": Case(
        compact_headers,
        check_carried,
        Behaviour(greet_s=0.5, reply_s=1.0),
        {"long-names": Behaviour(greet_s=0.5, reply_s=1.0, compact=False)},
        route="carrier",
    ),
    "sdp-ssrc": Case(
        sdp_ssrc,
        check_carried,
        Behaviour(greet_s=0.5, reply_s=1.0),
        {"strict": Behaviour(greet_s=0.5, reply_s=1.0, lenient_sdp=False)},
        route="carrier",
    ),
    "late-offer": Case(
        late_offer,
        check_carried,
        Behaviour(greet_s=0.5, reply_s=1.0),
        {"rejects": Behaviour(greet_s=0.5, reply_s=1.0, late_offer=False)},
        route="carrier",
    ),
    "ptime-30": Case(
        ptime_30,
        check_carried,
        Behaviour(greet_s=0.5, reply_s=1.0),
        {"20ms-only": Behaviour(greet_s=0.5, reply_s=1.0, any_ptime=False)},
        route="carrier",
    ),
    "ssrc-change": Case(
        ssrc_change,
        check_ssrc_change,
        Behaviour(greet_s=0.5, reply_s=1.0),
        {"first-ssrc": Behaviour(greet_s=0.5, reply_s=1.0, any_ssrc=False)},
    ),
    "reinvite": Case(
        reinvite,
        check_reinvite,
        Behaviour(greet_s=0.5, reply_s=1.0),
        {"one-way": Behaviour(greet_s=0.5, reply_s=1.0, refresh=False)},
    ),
    "reinvite-nosdp": Case(
        reinvite_nosdp,
        check_reinvite,
        Behaviour(greet_s=0.5, reply_s=1.0),
        {"no-offer": Behaviour(greet_s=0.5, reply_s=1.0, reoffer=False)},
    ),
    "hold-zero": Case(
        hold_zero,
        check_hold,
        Behaviour(),
        {"ignores-address": Behaviour(zero_hold=False)},
    ),
    "codec-change": Case(
        codec_change,
        check_codec_change,
        Behaviour(greet_s=0.5, reply_s=1.0),
        {"stale": Behaviour(greet_s=0.5, reply_s=1.0, recodec=False)},
        route="direct",  # rtpengine transcodes a stale answer to the offered law
    ),
}


def names(carrier: bool) -> list[str]:
    """The cases to run by default with or without the carrier."""
    skip = "direct" if carrier else "carrier"
    return [name for name, case in CASES.items() if case.route != skip]


def run(
    name: str, uri: str, seed: int, lines: Path | None = None, proxy: str | None = None
) -> dict[str, Any]:
    """The caller side of a case; its log (with the error if the call failed). `lines`: a
    directory with the caller's own prompt.wav and transfer.wav (else corpus utterances).
    `proxy`: where calls to other URIs (a transfer's) go, else to their own host."""
    said = {p.stem: speech.read_wav(p) for p in sorted(lines.glob("*.wav"))} if lines else {}
    calls: list[Session] = []

    def dial(to: str | None = None, **options: Any) -> Session:
        codecs = options.pop("codecs", CODECS)
        calls.append(Session(to or uri, codecs, proxy=proxy if to else None, **options))
        return calls[-1]

    try:
        return {"case": name} | CASES[name].script(dial, seed, said)
    except sip.SipError as e:
        log = calls[0].meta(seed, False) if calls else {"seed": seed}
        return {"case": name, "error": str(e)} | log


def judge(run: Path, profile: str = "clean") -> Result:
    """The case's verdict from a run directory."""
    w = load(run, profile)
    if "error" in w.log:
        return Result([Check("call completed", False, w.log["error"])])
    return CASES[w.log["case"]].check(w)


class Run(NamedTuple):
    """One case call of a results directory."""

    profile: str  # netem profile
    repeat: int
    case: str
    behaviour: str | None  # the reference agent's; None for a real target
    run: str  # its directory, relative to the results directory


Group = tuple[str, str, str | None]  # profile, case, behaviour


def groups(records: list[dict[str, Any]]) -> dict[Group, list[dict[str, Any]]]:
    """Records by profile, case and behaviour, repeats in order."""
    out: dict[Group, list[dict[str, Any]]] = {}
    for rec in records:
        out.setdefault((rec["profile"], rec["case"], rec["behaviour"]), []).append(rec)
    return out


def expected(behaviour: str | None) -> str | None:
    return None if behaviour is None else "pass" if behaviour == "good" else "fail"


def verdicts(recs: list[dict[str, Any]]) -> str:
    """The verdict (with how many repeats gave it), or the mix when it flips between repeats."""
    count = Counter(r["verdict"] for r in recs)
    if len(count) > 1:
        return "flips: " + ", ".join(f"{v} {n}" for v, n in count.most_common())
    v = recs[0]["verdict"]
    return v if len(recs) == 1 else f"{v} {len(recs)}/{len(recs)}"


def _spread(v: list[float], fmt: str) -> str:
    """One value, or the median [min, max] over repeats."""
    if len(v) == 1:
        return format(v[0], fmt)
    return f"{format(statistics.median(v), fmt)} [{format(min(v), fmt)}, {format(max(v), fmt)}]"


def timings(recs: list[dict[str, Any]]) -> list[tuple[str, str]]:
    """Each timing's name and value over the repeats, with its error bar: true value within
    value - hi .. value - lo."""
    by: dict[str, tuple[list[float], Bar]] = {}
    for r in recs:
        for t in r["timings"]:
            by.setdefault(t["name"], ([], Bar(*t["bar"])))[0].append(t["ms"])
    n = len(recs) > 1
    return [
        (
            name,
            f"{_spread(v, '.1f')} ms ({-b.hi:+.1f}/{-b.lo:+.1f})" + (f" n={len(v)}" if n else ""),
        )
        for name, (v, b) in by.items()
    ]


def failures(recs: list[dict[str, Any]]) -> list[str]:
    """Checks that failed or could not tell: with the detail for one run, else how many runs
    and the first one's detail."""
    count: Counter[str] = Counter()
    detail: dict[str, str] = {}
    for r in recs:
        for c in r["checks"]:
            if not c["ok"]:
                count[c["name"]] += 1
                detail.setdefault(c["name"], c["detail"])
    if len(recs) == 1:
        return [f"{c} ({detail[c]})" if detail[c] else c for c in count]
    return [
        f"{c} ({k}/{len(recs)}{': ' + detail[c] if detail[c] else ''})" for c, k in count.items()
    ]


def errors(recs: list[dict[str, Any]]) -> list[str]:
    """measured - truth of each timing whose truth the reference agent knows, over the repeats,
    and how many fell outside the error bar."""
    by: dict[str, list[tuple[float, bool]]] = {}
    for r in recs:
        for t in r["timings"]:
            if t["truth_ms"] is not None:
                e, b = t["ms"] - t["truth_ms"], Bar(*t["bar"])
                by.setdefault(t["name"], []).append((e, b.lo <= e <= b.hi))
    out = []
    for es in by.values():
        outside = sum(not ok for _, ok in es)
        note = f" ({outside}/{len(es)} outside the bar)" if outside else ""
        out.append(_spread([e for e, _ in es], "+.1f") + note)
    return out


def proven(records: list[dict[str, Any]]) -> bool:
    """Every reference behaviour got the verdict it should in every repeat."""
    return all(r["verdict"] == expected(r["behaviour"]) for r in records if r["behaviour"])


def summarize(out: Path, runs: list[Run]) -> tuple[str, list[dict[str, Any]], bool]:
    """Markdown summary per profile (repeats grouped), per-run records, and whether every
    reference behaviour got the verdict it should (good: pass, bad: fail) in every repeat."""
    records = []
    for run in runs:
        r = judge(out / run.run, run.profile)
        records.append(run._asdict() | {"verdict": r.verdict} | asdict(r))
    reference = bool(records) and records[0]["behaviour"] is not None
    head = ["case", "agent", "expected"] if reference else ["case"]
    head += ["result", "timings, ms (error bar)", "failed checks"]
    head += ["measured - truth, ms"] if reference else []
    rows: dict[str, list[list[str]]] = {}
    for (profile, case, behaviour), recs in groups(records).items():
        row = [case, behaviour or "", expected(behaviour) or ""] if reference else [case]
        row += [verdicts(recs), "<br>".join(f"{n}: {v}" for n, v in timings(recs)) or "-"]
        row += ["; ".join(failures(recs)) or "-"]
        row += [", ".join(errors(recs)) or "-"] if reference else []
        rows.setdefault(profile, []).append(row)
    text = "".join(f"### {p}\n\n{analyze._table(head, r)}\n" for p, r in rows.items())
    if reference:
        repeats = max(r["repeat"] for r in records)
        ok = proven(records)
        text += f"Every case {'proven' if ok else 'NOT proven'} over {repeats} repeat(s): "
        text += "good passes, bad fails.\n"
    bars = {b for r in records for t in r["timings"] for b in [Bar(*t["bar"])]}
    text += "\nError bars: true value = measured - error, error within\n\n"
    text += "".join(f"- [{b.lo:+.1f}, {b.hi:+.1f}] ms: {b.source}\n" for b in sorted(bars))
    return text, records, proven(records)
