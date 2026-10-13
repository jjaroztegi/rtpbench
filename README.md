# rtpbench

Wire-level latency and conformance tests for voice agents over SIP/RTP.

rtpbench calls a voice agent over SIP, captures the RTP, and measures turn latency and barge-in
timing from the packets themselves, with and without controlled network impairment.

Status: early development. What works today is the calibration: proving how far the measured
turn latency is from a delay injected by a reference agent.

## Calibrate

Needs Linux (or WSL2), Docker with Compose, and [uv](https://docs.astral.sh/uv/).

```sh
uv run rtpbench calibrate            # 5 network profiles x 20 turns, about 7 minutes
uv run rtpbench calibrate --profiles clean --turns 5
```

Three containers: `caller | router | agent`. The caller places a real SIP call and speaks
scripted synthetic turns. The reference agent answers each turn after a random delay it chooses
and logs, placed to the sample. The router applies `tc netem` (to RTP only) for the profiles in
[`bench.py`](src/rtpbench/bench.py). Both endpoints run `tcpdump`; every timestamp comes from a
capture, and all containers share one kernel clock.

The run writes `results/<timestamp>/` with the pcaps, per-turn records (`*/turns.jsonl`), the
conditions (`conditions.json`) and `summary.md`: the error of each measurement method against
the injected delay and against the truth, and what the gap between them is made of (agent
scheduling error, network delay, loss, reordering). The methods are described in
[`analyze.py`](src/rtpbench/analyze.py).

### Speech detection

```sh
uv run --extra vad rtpbench calibrate --speech   # clean and mobile x PCMU and PCMA, ~40 minutes
```

The same call with real speech: the reference agent replies with clips from
[`corpus/`](corpus/README.md) and the caller speaks them too. Speech boundaries are labelled on
each clean clip ([`speech.py`](src/rtpbench/speech.py)); the summary gives, per detector
([`detect.py`](src/rtpbench/detect.py)), how far detected onsets and offsets are from the labels
on the caller's capture. `--replies DIR` makes the agent reply with your own WAVs instead.

### Barge-in

```sh
uv run --extra vad rtpbench calibrate --barge-in   # clean and mobile, PCMA, ~35 minutes
```

The caller cuts into each long reply with an interruption, a backchannel or a cough; the
reference agent stops (a hard cut, a known delay after it hears the caller) or carries on, as a
script both ends share says ([`bargein.py`](src/rtpbench/bargein.py)). The summary gives the
stop time error per detector and timing method, and whether rtpbench told stops from carry-ons.

## Development

```sh
uv sync
uv run ruff format && uv run ruff check --fix
uv run mypy
uv run pytest
```

## Licence

Apache-2.0
