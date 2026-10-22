"""AVA's answers, RTP pacing and the caller's lines, from the latency and barge-in calls of the
unpacked direct sets. Per set:

- the answers the mock cancelled because it heard the caller over them (`barge` in its log);
- per profile, over these calls: `late`, the median of `analyze.pacing`'s p99 of how much later
  than its timestamps the packets arrived (a set's summary gives it over all of its cases'
  calls); the lines the caller said (a barge-in turn has two, its prompt and its interjection),
  how many began while the agent was sending, and how many turns the mock heard; the
  interjections and how many the agent stopped for;
- on a clean network, the answers of the latency calls (the agent's RTP, split where it was
  silent for 0.5 s): their packets, and the loudest of the last three packets (RMS of 20 ms,
  dBFS; -inf is digital silence).

    uv run --extra vad python results/ava/answers.py ava-audiosocket-direct ...
"""

import json
import math
import statistics
import sys
from pathlib import Path

from rtpbench import analyze, bargein, cases, g711, rtp

PROFILES = ("clean", "lte", "lte-bad")
SILENT_NS = 500_000_000  # RTP silent this long ends an answer
ANSWER_MIN = 50  # packets (1 s): ExternalMedia opens a call with one silent packet


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


def lines(w: cases.Wire) -> list[int]:
    """When each line of the caller began, as its own capture saw it."""
    up = [(t, p) for t, p in w.up if (p.pt, p.ssrc) == (w.log["pt"], w.log["ssrc"])]
    st = analyze.stream(up, w.log["pt"])
    out = []
    for turn in w.log["turns"]:
        for spans in (turn.get("prompt_speech"), turn["speech"]):
            if spans and (t := st.time(st.index(w.log["seq0"], spans[0][0]), True)) is not None:
                out.append(t)
    return out


def main() -> None:
    for out in map(Path, sys.argv[1:]):
        records = [json.loads(line) for line in (out / "realtime.jsonl").read_text().splitlines()]
        heard = [r["speech_end_ns"] for r in records if r.get("trigger") == "turn"]
        print(
            f"{out.name}: answers cancelled for the caller's voice: "
            f"{sum(r['event'] == 'barge' for r in records)}"
        )
        for profile in PROFILES:
            late, packets, quiet = [], [], []
            said = during = reached = interjections = stopped = 0
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
                starts = lines(w)
                said += len(starts)
                during += sum(any(a[0][0] <= t <= a[-1][0] for a in spoken) for t in starts)
                reached += sum(w.up[0][0] <= t <= w.up[-1][0] for t in heard)
                if run.name == "barge-in":
                    turns = [json.loads(s) for s in (run / "turns.jsonl").read_text().splitlines()]
                    interjections += len(turns)
                    stopped += sum(bargein._stopped(r, "wire/gate") for r in turns)
            print(
                f"  {profile}: {len(runs)} calls, late p99 {statistics.median(late):.1f} ms; "
                f"{said} lines said, {during} during an answer, {reached} turns heard; "
                f"{interjections} interjections, {stopped} stopped"
            )
            if packets:
                print(
                    f"  clean latency answers: {len(packets)}, {min(packets)}-{max(packets)} "
                    f"packets; last three: loudest {min(quiet):.1f} to {max(quiet):.1f} dBFS"
                )


if __name__ == "__main__":
    main()
