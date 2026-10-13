"""Conformance cases: scripted calls with a verdict and timings with error bars.

A case is a caller script (a `Session` driven step by step, with `Script` media), a check that
reads only the caller's capture and log, and reference-agent behaviours: one that should pass and
at least one that should fail. Against the reference agent each case runs once per behaviour,
which proves the case itself; against a real target it runs once.

Every timing carries the error bar of the way it is measured, from the calibrations. SIP and RTP
events are capture times (`rtpbench calibrate`: wire timing within 0.41 ms on a clean network);
agent speech onsets are webrtcvad's (`rtpbench calibrate --speech`, p5..p95 per codec).
"""

import json
import re
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Any, NamedTuple

from rtpbench import analyze, detect, g711, pcap, rtp, sip, speech, speechcal
from rtpbench.agent import Behaviour
from rtpbench.caller import Media, Session, speech_utterances

CODECS = (g711.PCMU, g711.PCMA)
QUIET_NS = 1_500_000_000  # agent silence that ends what it was saying
GREETING_WAIT_S = 10.0
GREETING_MAX_MS = 2000  # a caller left in silence longer than this starts saying "hello?"
REPLY_WAIT_S = 15.0
BYE_AFTER_NS = 1_000_000_000  # into the agent's speech
CANCEL_AFTER_S = 0.2  # after the first provisional response
MEDIA_GRACE_MS = 500  # RTP sent before the agent handled a request may still be on its way
WATCH_S = 2.0  # listen after the call ends for media that should have stopped
HOLD_S = 3.0
RESUME_MS = 1000
CLOCK_MS = 40  # RTP timestamp gap vs arrival gap across a pause (two packets of jitter)
_SIP = re.compile(rb"(SIP/2\.0 \d{3} |[A-Z]+ \S+ SIP/2\.0\r\n)")


class Bar(NamedTuple):
    """measured - truth lies within [lo, hi] ms."""

    lo: float
    hi: float
    source: str


WIRE = Bar(-0.41, 0.41, "capture times; wire timing max abs error, clean (calibrate)")
ONSET = {
    g711.PCMU: Bar(-3.8, 32.9, "webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech)"),
    g711.PCMA: Bar(-88.1, 24.3, "webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech)"),
}


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

    def __init__(self, pt: int) -> None:
        super().__init__(pt)
        self.queue: list[tuple[str, bytes, list[tuple[int, int]]]] = []
        self.said: list[dict[str, Any]] = []
        self.bursts: list[list[int]] = []
        self.muted = False  # send nothing (call inactive)

    def idle(self) -> bytes | None:
        return None if self.muted else self.silence

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
            return bool(self.queue or self.audio)

    def speech_after(self, t_ns: int) -> int | None:
        with self.lock:
            return next((on for on, _ in self.bursts if on > t_ns), None)

    def quiet(self, ns: int = QUIET_NS) -> bool:
        with self.lock:
            return time.time_ns() - self.agent_last >= ns


Dial = Callable[..., Session]


def greeting(dial: Dial, seed: int) -> dict[str, Any]:
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


def _talking(s: Session, m: Script, seed: int) -> int | None:
    """When the agent started talking: its greeting, or else its reply to a question."""
    t0 = time.time_ns()
    if s.wait(lambda: s.remote_bye or m.speech_after(t0) is not None, GREETING_WAIT_S):
        return m.speech_after(t0)
    m.say(*speech_utterances(seed)[0])
    s.wait(lambda: s.remote_bye or not m.busy(), 30)
    t1 = time.time_ns()
    s.wait(lambda: s.remote_bye or m.speech_after(t1) is not None, REPLY_WAIT_S)
    return m.speech_after(t1)


def bye(dial: Dial, seed: int) -> dict[str, Any]:
    """Get the agent talking, BYE a second into it, then watch for media."""
    s = dial()
    s.answer()
    m = Script(s.pt)
    s.start(m.source, m.on_packet)
    if (onset := _talking(s, m, seed)) is not None:
        s.wait(lambda: s.remote_bye or time.time_ns() >= onset + BYE_AFTER_NS, 5)
    s.hangup()
    s.wait(lambda: False, WATCH_S)
    return s.meta(seed, s.remote_bye) | {"said": m.said}


def cancel(dial: Dial, seed: int) -> dict[str, Any]:
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


def hold(dial: Dial, seed: int) -> dict[str, Any]:
    """Once the agent is quiet: hold (sendonly), resume, hold (inactive), resume; 3 s each."""
    s = dial()
    s.answer()
    m = Script(s.pt)
    s.start(m.source, m.on_packet)
    s.wait(lambda: s.remote_bye, 1.0)
    s.wait(lambda: s.remote_bye or m.quiet(), 20)
    for offer in ("sendonly", "sendrecv", "inactive", "sendrecv"):
        if s.remote_bye:
            break
        m.muted = offer == "inactive"
        s.reinvite(offer)
        s.wait(lambda: s.remote_bye, HOLD_S)
    s.hangup()
    return s.meta(seed, s.remote_bye) | {"said": m.said}


@dataclass
class Wire:
    """One case call as the caller's capture saw it, plus the logs."""

    log: dict[str, Any]  # caller.json
    agent: dict[str, Any] | None  # agent.json, from the reference agent only
    msgs: list[tuple[int, bool, sip.Message]]  # capture time, sent by the caller, message
    up: analyze.Timed  # RTP the caller sent
    down: analyze.Timed  # RTP the caller received

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

    def truth(self, kind: str) -> tuple[int, int] | None:
        """Labelled first and last sample of the reference agent's `kind` reply, as captured."""
        turns = self.agent["turns"] if self.agent else []
        turn = next((u for u in turns if u.get("kind") == kind), None)
        if (st := self.audio) is None or turn is None or self.agent is None:
            return None
        a0 = self.agent["seq0"]
        return speechcal._truth(st, [(st.index(a0, a), st.index(a0, b)) for a, b in turn["speech"]])


def load(run: Path) -> Wire:
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
    return Wire(log, agent, msgs, up, down)


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
    r.timings.append(Timing("200 OK to agent speech", ms, ONSET[w.log["pt"]], truth_ms))
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
        r.checks.append(Check("CANCEL sent while ringing", None, "no provisional response first"))
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


# answers to a hold offer that honour it (RFC 3264 6.1: inactive is fine for sendonly)
HOLD_ANSWERS = {"sendonly": ("recvonly", "inactive"), "inactive": ("inactive",)}


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
        offer = sip.parse_sdp(held.body).direction
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
        (u0, p0), (u1, p1) = before[-1], after[0]
        ms = (u1 - answers[1]) / 1e6
        r.timings.append(Timing(f"resume from {offer}: 2xx to agent RTP", ms, WIRE))
        r.checks.append(
            Check(f"resume from {offer}: agent RTP within {RESUME_MS} ms", ms <= RESUME_MS)
        )
        drift = ((p1.ts - p0.ts) & 0xFFFFFFFF) / 8 - (u1 - u0) / 1e6
        r.timings.append(Timing(f"resume from {offer}: RTP clock drift", drift, WIRE))
        same = p1.ssrc == p0.ssrc and p1.seq == (p0.seq + 1) & 0xFFFF and abs(drift) <= CLOCK_MS
        detail = f"ssrc {p0.ssrc:#x}->{p1.ssrc:#x}, seq {p0.seq}->{p1.seq}, clock {drift:+.0f} ms"
        r.checks.append(Check(f"resume from {offer}: same RTP stream", same, detail))
    return r


@dataclass(frozen=True)
class Case:
    """A caller script, its check, and the reference agent behaviours that pass and fail it."""

    script: Callable[[Dial, int], dict[str, Any]]
    check: Callable[[Wire], Result]
    good: Behaviour
    bad: dict[str, Behaviour]

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
}


def run(name: str, uri: str, seed: int) -> dict[str, Any]:
    """The caller side of a case; its log (with the error if the call failed)."""
    calls: list[Session] = []

    def dial(**options: Any) -> Session:
        calls.append(Session(uri, CODECS, **options))
        return calls[-1]

    try:
        return {"case": name} | CASES[name].script(dial, seed)
    except sip.SipError as e:
        log = calls[0].meta(seed, False) if calls else {"seed": seed}
        return {"case": name, "error": str(e)} | log


def judge(run: Path) -> Result:
    """The case's verdict from a run directory."""
    w = load(run)
    if "error" in w.log:
        return Result([Check("call completed", False, w.log["error"])])
    return CASES[w.log["case"]].check(w)


def _row(r: Result) -> list[str]:
    failed = "; ".join(
        f"{c.name}{f' ({c.detail})' if c.detail else ''}" for c in r.checks if not c.ok
    )
    timings = "<br>".join(f"{t.name}: {t}" for t in r.timings) or "-"
    return [r.verdict, timings, failed or "-"]


def summarize(runs: list[tuple[str, str | None, Path]]) -> tuple[str, list[dict[str, Any]], bool]:
    """Markdown summary, per-run records, and whether every reference behaviour got the verdict
    it should (good: pass, bad: fail)."""
    records, rows, proven = [], [], True
    for name, behaviour, path in runs:
        r = judge(path)
        rec: dict[str, Any] = {"case": name, "behaviour": behaviour, "run": path.name}
        rec |= {"verdict": r.verdict} | asdict(r)
        records.append(rec)
        if behaviour is None:
            rows.append([name, *_row(r)])
            continue
        want = "pass" if behaviour == "good" else "fail"
        proven &= r.verdict == want
        errors = [t.error() for t in r.timings if t.truth_ms is not None]
        rows.append([name, behaviour, want, *_row(r), ", ".join(errors) or "-"])
    if runs and runs[0][1] is not None:
        head = ["case", "agent", "expected", "result", "timings, ms (error bar)", "failed checks"]
        out = analyze._table([*head, "measured - truth, ms"], rows)
        out += f"\nEvery case {'proven' if proven else 'NOT proven'}: good passes, bad fails.\n"
    else:
        out = analyze._table(["case", "result", "timings, ms (error bar)", "failed checks"], rows)
    bars = {b for r in records for t in r["timings"] for b in [Bar(*t["bar"])]}
    out += "\nError bars: true value = measured - error, error within\n\n"
    out += "".join(f"- [{b.lo:+.1f}, {b.hi:+.1f}] ms: {b.source}\n" for b in sorted(bars))
    return out, records, proven
