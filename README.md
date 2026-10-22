# rtpbench

Wire-level latency and conformance tests for voice agents over SIP/RTP.

rtpbench calls a voice agent over SIP, captures the RTP on both ends, and measures turn latency,
barge-in and SIP behaviour from the packets themselves, on clean and impaired networks
(`tc netem`). Every measurement carries an error bar calibrated against a reference agent that
logs the truth, and every case is proven against that agent, passing and failing, before it
judges yours.

Status: early development.

## What it found

Three open-source ways to put the OpenAI Realtime API on a SIP call, through 21 cases, with and
without a carrier in front, on a mock engine that holds the AI engine's share of each turn fixed:

| | [LiveKit](https://github.com/livekit/sip) | [AI Voice Connector CE](https://github.com/OpenSIPS/opensips-ai-voice-connector-ce) | Asterisk + [AVA](https://github.com/hkjarral/AVA-AI-Voice-Agent-for-Asterisk) |
| --- | --- | --- | --- |
| cases failed of 21 | 6, and 1 inconclusive | 7, and 2 inconclusive | 4, and 3 inconclusive |
| turn latency, clean, p50 | 1833 ms | 1511 ms | 1588 ms |
| its own media path per turn, p50 | 335 ms | 9 ms | 88 ms |
| stops for an interruption, clean, p50 | 306 ms | 24 ms | never |

- LiveKit keeps sending audio to a held caller in every kind of hold, AI Voice Connector CE when
  held with `c=0.0.0.0`, and both answer a re-INVITE that changes codec with the old codec. AVA
  sends RTP only while it speaks, so whether its media resumes after a hold cannot be judged.
- Most of LiveKit's extra latency is its own media path: 326 ms per turn more than AI Voice
  Connector CE's.
- LiveKit's RTP falls 20 ms behind its own timestamps 4 s into every call, so a receiver needs a
  21 ms jitter buffer for it on a clean network; AI Voice Connector CE's needs 1.1 ms.
- AI Voice Connector CE delivers the engine's speech sample for sample. LiveKit re-encodes it on
  the way, through its WebRTC room, and in 6% of answers stretches or cuts a pause by 20-40 ms.
- AVA, as its golden configuration ships, cuts the last 0.8 s of every answer, and it never
  stops for an interruption: it keeps the caller's audio from the engine while it speaks. Over
  AudioSocket under packet loss, the engine sometimes got silence instead of the caller, so 5 more
  cases fail now and then.
- AI Voice Connector CE's main branch fixed 4 of the 11 cases it failed in the baseline (a failed
  transfer no longer hangs up on the caller; compact headers, a bare `a=ssrc` and SIP over TCP
  are taken). It still refuses an INVITE without SDP and answers no re-INVITE without one.

The details, commands, conditions and raw runs are in [the baseline](results/baseline),
[AI Voice Connector CE at b95f5af](results/aivc-b95f5af) and [Asterisk + AVA](results/ava),
and every call's timeline on [the results site](https://jjaroztegi.github.io/rtpbench/).

Common ways of measuring turn latency have errors of their own: measured inside the agent, a turn
misses the network (80 ms on an LTE path); an energy rule on a recording reads turns long, by
87-110 ms at the median. Each method against the truth: [metrology](results/metrology).

## Quick start

Needs Linux (WSL2 works), Docker 28 or later with Compose, and
[uv](https://docs.astral.sh/uv/).

```sh
uv run rtpbench calibrate --profiles clean --turns 5      # how exactly this host times the wire
uv run --extra vad rtpbench cases                         # prove every case against the reference agent
uv run --extra vad rtpbench target livekit --mock         # a bundled target, no AI account needed
uv run --extra vad rtpbench target sip:agent@host         # your agent, the same way
```

From a fresh clone the first three take about 1, 14 and 11 minutes, building or pulling about
2.5 GB of Docker images on first use.

Each run writes `results/<timestamp>/` with the captures, `summary.md` and, for cases,
`report.html`: a timeline of every call's SIP, speech and RTP. `rtpbench index` links every run
under `results/` from `results/index.html`; `rtpbench COMMAND --help` lists a command's options,
defaults and valid names.

## Documentation

- [Calibration](docs/calibration.md): error bars, clock steps, network profiles and their sources
- [Conformance cases](docs/cases.md): what each case checks
- [Targets, your own agent, the mock engine and the carrier](docs/targets.md)
- [CI](docs/ci.md): pass or fail your agent's run against a policy

## Development

```sh
uv sync
uv run ruff format && uv run ruff check --fix
uv run mypy
uv run pytest
```

## Licence

Apache-2.0, except `targets/aivc/opensips.cfg`, derived from AI Voice Connector CE's example and
under its GPL-3.0-or-later, and `targets/ava/ai-agent.yaml`, derived from AVA's golden OpenAI
configuration and under its MIT licence.
