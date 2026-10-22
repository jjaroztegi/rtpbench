"""AVA's answers, RTP pacing and the caller's lines, from the latency and barge-in calls of the
unpacked direct sets. Per set:

- the answers the mock cancelled because it heard the caller over them (`barge` in its log);
- per profile, over these calls: `late`, the median of `analyze.pacing`'s p99 of how much later
  than its timestamps the packets arrived (a set's summary gives it over all of its cases'
  calls); the lines the caller said (a barge-in turn has two, its prompt and its interjection),
  split by whether the line began while the agent was sending, each with how many of them the
  mock heard (a turn of its ended with the line); the interjections and how many the agent
  stopped for;
- on a clean network, the answers of the latency calls (the agent's RTP, split where it was
  silent for 0.5 s): their packets, and the loudest of the last three packets (RMS of 20 ms,
  dBFS; -inf is digital silence);
- for each interjection the agent stopped for, the times that bear on why, in seconds from the
  call's INVITE (the origin of a report's timeline).

    uv run --extra vad python results/ava/answers.py ava-audiosocket-direct ...
"""

import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any

import numpy as np

from rtpbench import analyze, bargein, cases, g711, realtime, rtp, speechcal
from rtpbench.voice import GATE

PROFILES = ("clean", "lte", "lte-bad")
SILENT_NS = 500_000_000  # RTP silent this long ends an answer
ANSWER_MIN = 50  # packets (1 s): ExternalMedia opens a call with one silent packet
HEARD_NS = 500_000_000  # the mock's turn ends within this of the end of the line it heard


def answers(down: analyze.Timed) -> list[analyze.Timed]:
    out: list[analyze.Timed] = []
    for t, p in down:
        if p.pt in g711.NAMES:
            if out and t - out[-1][-1][0] <= SILENT_NS:
                out[-1].append((t, p))
            else:
                out.append([(t, p)])
    return [a for a in out if len(a) >= ANSWER_MIN]


def level(p: rtp.Packet) -> float:
    pcm = g711.decode(p.pt, p.payload)
    rms = math.sqrt(sum(s * s for s in pcm) / len(pcm))
    return 20 * math.log10(rms / 32768) if rms else -math.inf


def lines(w: cases.Wire) -> dict[tuple[int, str], tuple[int, int]]:
    """When each line of the caller began and ended, as its own capture saw it, by turn and
    kind (the labelled speech, as a report's timeline draws it)."""
    up = [(t, p) for t, p in w.up if (p.pt, p.ssrc) == (w.log["pt"], w.log["ssrc"])]
    st = analyze.stream(up, w.log["pt"])
    out = {}
    for k, turn in enumerate(w.log["turns"]):
        for kind in ("prompt_speech", "speech"):
            if spans := turn.get(kind):
                marks = [(st.index(w.log["seq0"], a), st.index(w.log["seq0"], b)) for a, b in spans]
                if edges := speechcal._truth(st, marks):
                    out[k, kind] = edges
    return out


def stopped_for(
    out: Path,
    run: Path,
    w: cases.Wire,
    turn: dict[str, Any],
    span: tuple[int, int],
    records: list[dict[str, Any]],
) -> str:
    """The times around an interjection after which the agent's answer ended."""
    t0 = w.msgs[0][0]
    a, b = span

    def s(t: int) -> str:
        return f"{(t - t0) / 1e9:.3f}"

    stop = a + round(turn["measured_ms"]["wire/gate"] * 1e6)
    sent = next(x for x in answers(w.down) if x[0][0] <= a <= x[-1][0])
    over = next(
        (r for r in records if r.get("first_audio_ns", a + 1) <= a <= r.get("end_ns", a - 1)), None
    )
    got = next((r for r in records if a <= r.get("speech_end_ns", 0) <= b + HEARD_NS), None)
    rows = [
        f"interjection {turn['clip']} (caller speech, labelled): {s(a)} to {s(b)}",
        f"agent speech ended (gate): {s(stop)}, {turn['measured_ms']['wire/gate']:.0f} ms in",
        f"agent RTP of the answer it was in: {s(sent[0][0])} to {s(sent[-1][0])}",
    ]
    if over:
        rows.append(
            f"mock's answer {over['answer']}: first audio {s(over['first_audio_ns'])}, "
            f"ended {s(over['end_ns'])} ({over['status']})"
        )
    if recording := realtime.recording(out, (over or got or {}).get("session", "")):
        pcm, starts, _, _ = recording
        voiced = starts[np.abs(pcm) >= GATE]
        if len(voiced := voiced[voiced >= a]):
            rows.append(
                f"mock's first voiced audio from the interjection on arrived: {s(voiced[0])}"
            )
    if got:
        rows.append(f"mock's turn heard (as {got['line']}): speech ended {s(got['speech_end_ns'])}")
    return f"  stopped for, {run.relative_to(out)}, turn {turn['turn']}:\n    " + "\n    ".join(
        rows
    )


def main() -> None:
    for out in map(Path, sys.argv[1:]):
        records = [json.loads(line) for line in (out / "realtime.jsonl").read_text().splitlines()]
        heard = [r["speech_end_ns"] for r in records if r.get("trigger") == "turn"]
        print(
            f"{out.name}: answers cancelled for the caller's voice: "
            f"{sum(r['event'] == 'barge' for r in records)}"
        )
        for profile in PROFILES:
            late, packets, quiet, events = [], [], [], []
            said = {False: [0, 0], True: [0, 0]}  # began outside / during an answer: lines, heard
            interjections = stopped = 0
            runs = sorted(
                c.parent
                for c in (out / profile).glob("*/*/caller.json")
                if c.parent.name in ("latency", "barge-in")
            )
            for run in runs:
                w = cases.load(run, profile)
                if paced := analyze.pacing(w.down):
                    late.append(paced[1])
                spoken = answers(w.down)
                if profile == "clean" and run.name == "latency":
                    packets += [len(a) for a in spoken]
                    quiet += [max(level(p) for _, p in a[-3:]) for a in spoken]
                spans = lines(w)
                for a, b in spans.values():
                    during = any(x[0][0] <= a <= x[-1][0] for x in spoken)
                    said[during][0] += 1
                    said[during][1] += any(a <= h <= b + HEARD_NS for h in heard)
                if run.name == "barge-in":
                    turns = [json.loads(s) for s in (run / "turns.jsonl").read_text().splitlines()]
                    interjections += len(turns)
                    for turn in turns:
                        if bargein._stopped(turn, "wire/gate"):
                            stopped += 1
                            events.append(
                                stopped_for(
                                    out, run, w, turn, spans[turn["turn"], "speech"], records
                                )
                            )
            print(
                f"  {profile}: {len(runs)} calls, late p99 "
                f"{f'{statistics.median(late):.1f}' if late else 'n/a'} ms; lines said: "
                f"{said[False][0]} outside an answer, {said[False][1]} heard; "
                f"{said[True][0]} during one, {said[True][1]} heard; "
                f"{interjections} interjections, {stopped} stopped"
            )
            if packets:
                print(
                    f"  clean latency answers: {len(packets)}, {min(packets)}-{max(packets)} "
                    f"packets; last three: loudest {min(quiet):.1f} to {max(quiet):.1f} dBFS"
                )
            if events:
                print(*events, sep="\n")


if __name__ == "__main__":
    main()
