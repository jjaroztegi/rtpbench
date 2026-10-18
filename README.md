# rtpbench

Wire-level latency and conformance tests for voice agents over SIP/RTP.

rtpbench calls a voice agent over SIP, captures the RTP on both ends, and measures turn latency,
barge-in and SIP behaviour from the packets themselves, on clean and impaired networks
(`tc netem`). Every measurement carries an error bar calibrated against a reference agent that
logs the truth, and every case is proven against that agent, passing and failing, before it
judges yours.

Status: early development.

## What it found

Two open-source SIP connectors for the OpenAI Realtime API, through 21 cases, with and without a
carrier in front, on a mock engine that holds the AI engine's share of each turn fixed:

| | [LiveKit](https://github.com/livekit/sip) | [AI Voice Connector CE](https://github.com/OpenSIPS/opensips-ai-voice-connector-ce) |
| --- | --- | --- |
| cases failed of 21 | 7 | 12, and 1 inconclusive |
| turn latency, clean, p50 | 1833 ms | 1512 ms |
| the connector's own media path per turn, p50 | 335 ms | 11 ms |
| stops for an interruption, clean, p50 | 306 ms | 24 ms |

- Neither handles hold correctly: both keep sending audio to a held caller, and both answer a
  re-INVITE that changes codec with the old codec.
- Most of LiveKit's extra latency is its own media path: 324 ms per turn more than AI Voice
  Connector CE's.
- LiveKit's RTP falls 20 ms behind its own timestamps 4 s into every call, so a receiver needs a
  21 ms jitter buffer for it on a clean network; AI Voice Connector CE's needs 1.2 ms.
- AI Voice Connector CE fails every signalling variation a carrier sends (compact headers, a bare
  `a=ssrc`, an INVITE without SDP), hangs up on the caller when a transfer fails, and as
  configured in its example takes SIP over UDP only, so an INVITE over 1300 bytes is refused.

The details, commands, conditions and raw runs are in [the baseline](results/baseline), and every
call's timeline on [the results site](https://jjaroztegi.github.io/rtpbench/).

Common ways of measuring turn latency have errors of their own: measured inside the agent, a turn
misses the network (80 ms on an LTE path); an energy rule on a recording reads every turn about
90 ms long. Each method against the truth: [metrology](results/metrology).

## Quick start

Needs Linux (WSL2 works), Docker 28 or later with Compose, and
[uv](https://docs.astral.sh/uv/).

```sh
uv run rtpbench calibrate --profiles clean --turns 5      # how exactly this host times the wire
uv run --extra vad rtpbench cases                         # prove every case against the reference agent
uv run --extra vad rtpbench target livekit --mock         # a bundled target, no AI account needed
sudo .venv/bin/rtpbench cases sip:agent@host              # your agent (after uv sync --extra vad)
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
- [Targets, the mock engine and the carrier](docs/targets.md)

## Development

```sh
uv sync
uv run ruff format && uv run ruff check --fix
uv run mypy
uv run pytest
```

## Licence

Apache-2.0, except `targets/aivc/opensips.cfg`, derived from AI Voice Connector CE's example and
under its GPL-3.0-or-later.
