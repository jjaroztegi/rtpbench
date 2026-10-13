# rtpbench

Wire-level latency and conformance tests for voice agents over SIP/RTP.

rtpbench calls a voice agent over SIP, captures the RTP, and measures turn latency and barge-in
timing from the packets themselves, with and without controlled network impairment.

Status: early development. What works today is the calibration: proving how far the measured
turn latency is from a delay injected by a reference agent.

## Calibrate

Needs Linux (or WSL2), Docker with Compose, and [uv](https://docs.astral.sh/uv/).

```sh
uv run rtpbench calibrate            # 7 network profiles x 20 turns, about 10 minutes
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

## Network profiles

netem settings per direction, on the router, RTP only (SIP is never impaired). `delay`, `jitter`,
`loss` and `mobile` are synthetic stimuli for the calibrations. `lte` and `lte-bad` stand for a
mobile caller's path, and every number in them has a source:

| profile | netem | source |
| --- | --- | --- |
| `lte` | `delay 40ms 3ms distribution normal loss gemodel 0.505% 50% rate 100mbit` | 1% loss, the VoLTE (QCI 1) target per radio link ([3GPP TR 26.989](https://www.3gpp.org/ftp/Specs/archive/26_series/26.989/) 5.1.1.6.1), in bursts of 2 packets (3GPP VoLTE delay/error profiles 7-10, [EVS-7c S4-141392](https://www.3gpp.org/ftp/tsg_sa/WG4_CODEC/EVS_Permanent_Documents/) Annex D); jitter sd 3 ms (commercial LTE in mobility, [Elnashar et al.](https://arxiv.org/abs/1810.02968), fig. 6); 40 ms one way (LTE uplink p99, [Nielsen et al.](https://arxiv.org/abs/1909.03875), fig. 4) |
| `lte-bad` | `delay 36ms 30ms distribution normal loss gemodel 3.2% 48% rate 100mbit` | 3GPP delay/error profile 8, VoLTE logs in challenging radio conditions (EVS-7c Annex D): 6.2% loss in runs of 2.1 packets; delay above the floor mean 45 ms, sd 26, p95 90. netem delivers mean 48, sd 23, p95 88 (5000 packets) |

`rate` keeps packets in order, as a radio bearer delivers them: independent netem jitter of sd
26 ms reorders 30% of packets, the profile 8 trace 3%. netem cannot give the trace's
packet-to-packet correlation (0.95; 0.43 here).

## Conformance cases

```sh
uv run --extra vad rtpbench cases          # every case against the reference agent (Docker)
sudo .venv/bin/rtpbench cases sip:agent@host   # the same cases against your agent
```

Each case ([`cases.py`](src/rtpbench/cases.py)) is a scripted call with a verdict (pass, fail
or inconclusive) and timings, each with the error bar of how it is measured, from the
calibrations above. Without a URI, every case runs against the reference agent once with a
behaviour that should pass it and once with each behaviour that should fail it, so the case
itself is proven; the command fails if any verdict is not the expected one. With a URI, the
cases call your agent from this machine (after `uv sync --extra vad`; capturing needs root).
The run writes `summary.md`, `results.json` and `report.html`: one table per profile and, per
call, a timeline of the SIP messages, speech and RTP of both sides on one time axis, all from the
caller's capture. `rtpbench report DIR` judges a run again and rewrites them.

`--profiles clean,lte,lte-bad --runs 10` repeats every call ten times under each profile (repeat
k uses seed + k - 1). Verdicts are then counted ("pass 10/10"); a case whose verdict changes
between repeats reads "flips: pass 7, fail 3" and the reference command fails. Timings read
median [min, max] over the repeats. The report draws the first repeat of each call and every
repeat whose verdict differs from it.

`--lines DIR` gives the caller its own `prompt.wav` (a question) and `transfer.wav` (asking for
a person) in the agent's language; the corpus is used otherwise.

| case | what passes |
| --- | --- |
| `greeting` | the agent speaks first, within 2 s of its 200 OK |
| `bye` | caller hangs up at least a second into the agent's speech (its greeting, or its reply to a question), while it is audible: 2xx to BYE, agent RTP stops within 500 ms |
| `cancel` | caller cancels a ringing INVITE: 2xx to CANCEL, 487 to the INVITE, no RTP after |
| `hold` | hold (sendonly, then inactive) and resume by re-INVITE: answers honour the offer, no agent RTP while held, RTP back within 1 s as the same stream (SSRC, next seq, timestamps kept time) |
| `dtmf-rfc4733` | once the agent's greeting is over the caller presses 5 (RFC 4733): telephone-event negotiated, the agent says something within 5 s |
| `dtmf-info` | the same by SIP INFO (`application/dtmf-relay`): 2xx, the agent says something within 5 s |
| `refer` | the caller asks for a person; rtpbench plays the transferee (202, NOTIFY sipfrag 100 then 200, without calling the target): REFER with a SIP or tel Refer-To, both NOTIFYs answered 2xx, the agent hangs up within 10 s |
| `timer` | session timers offered (90 s, caller refreshes) and refreshed once at half time, then not again: the 2xx takes them (Session-Expires, `refresher=uac`, Require: timer), the refresh gets 2xx with media undisturbed, the agent ends the session by BYE between 45 and 90 s after the refresh (RFC 4028) |

## Targets

```sh
export OPENAI_API_KEY=...                 # see targets/aivc/compose.yaml
uv run --extra vad rtpbench target aivc   # about 12 minutes
```

A target is a voice agent that runs in Docker next to the reference stack, so the caller reaches
it through the same netem router (`--profiles`, `--runs` as for the cases). `rtpbench target NAME` brings it up and, from
the caller container, runs every case, a turn-latency call (12 turns) and a barge-in call
(10 turns) against it, with the English caller lines in [`corpus/lines/en`](corpus/README.md).
`summary.md` holds the case verdicts, then turn latency and barge-in over every turn of every
repeat per profile (with the spread of the per-run medians and stop rates, and the error bar
of each); `report.html` the case timelines; `target.log` the target's own logs.

| target | what |
| --- | --- |
| [`aivc`](targets/aivc) | [OpenSIPS AI Voice Connector CE](https://github.com/OpenSIPS/opensips-ai-voice-connector-ce) at a pinned commit, OpenSIPS 3.6 (images pinned by digest), openai flavor as upstream's example sets it, plus a transfer target. Needs `OPENAI_API_KEY`; `OPENAI_URL` points it at another Realtime endpoint (e.g. Azure OpenAI `wss://<resource>.openai.azure.com/openai/v1/realtime?model=<deployment>`) |

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
