"""The held-out detector table from the unpacked detector archive: per bar, how many turns of
seeds 6-10 fall below and above the bar in the checked-out `src/rtpbench/cases.py` (p5..p95 of
seeds 1-5). The archive holds one calibration per seed, kind, profile and codec.

    uv run --extra vad python results/baseline/heldout.py pub
"""

import json
import sys
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Any

from rtpbench import bargein, cases, g711

PT = {"pcmu": g711.PCMU, "pcma": g711.PCMA}
Value = Callable[[dict[str, Any]], float | None]
TABLES: dict[str, tuple[dict[tuple[str, int], cases.Bar], str, Value]] = {
    "onset": (cases.ONSET, "speech-s*", lambda r: r.get("webrtcvad_ms")),
    "first onset": (cases.ONSET_FIRST, "speech-s*", lambda r: r.get("webrtcvad_first_ms")),
    "stop": (
        cases.STOP,
        "barge-s*",
        lambda r: r["measured_ms"]["wire/gate"] if bargein._stopped(r, "wire/gate") else None,
    ),
}


def main() -> None:
    pub = Path(sys.argv[1])
    print("| bar | profile | codec | shipped | turns | below | above | outside |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for name, (bars, pattern, value) in TABLES.items():
        tally: defaultdict[tuple[str, str], list[int]] = defaultdict(lambda: [0, 0, 0])
        for f in pub.glob(f"{pattern}/*/turns.jsonl"):
            profile, codec = f.parent.name.rsplit("-", 1)
            bar = bars[profile, PT[codec]]
            for r in map(json.loads, f.read_text().splitlines()):
                if (v := value(r)) is None or "truth_ms" not in r:
                    continue
                error = v - r["truth_ms"]
                t = tally[profile, codec]
                t[0] += 1
                t[1] += error < bar.lo
                t[2] += error > bar.hi
        for profile in ("clean", "lte", "lte-bad"):
            for codec in PT:
                bar = bars[profile, PT[codec]]
                turns, below, above = tally[profile, codec]
                print(
                    f"| {name} | {profile} | {codec.upper()} | [{bar.lo:+.1f}, {bar.hi:+.1f}] "
                    f"| {turns} | {below} | {above} | {(below + above) / turns:.0%} |"
                )


if __name__ == "__main__":
    main()
