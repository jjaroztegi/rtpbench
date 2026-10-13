# rtpbench

Wire-level latency and conformance tests for voice agents over SIP/RTP.

rtpbench calls a voice agent over SIP, captures the RTP, and measures turn latency and barge-in
timing from the packets themselves, with and without controlled network impairment.

Status: early development. What works today: calibrations that prove how far each measurement
is from the truth a reference agent logs; 11 conformance cases, each proven against that agent
on clean and impaired paths; and a first open-source target with [results](#results).

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
| `refer-fail` | as `refer`, but the final NOTIFY reports `486 Busy Here`: the agent takes the call back (RFC 5589 6.3): no BYE for 10 s, and it speaks within 5 s of the failure NOTIFY |
| `codec-pcmu` | the caller offers PCMU alone: answered 2xx with PCMU alone (RFC 3264 6.1: the answer's formats come from the offer) and the agent's RTP is PCMU |
| `codec-pcma` | the same with PCMA |
| `timer` | session timers offered (90 s, caller refreshes) and refreshed once at half time, then not again: the 2xx takes them (Session-Expires, `refresher=uac`, Require: timer), the refresh gets 2xx with media undisturbed, the agent ends the session by BYE between 45 and 90 s after the refresh (RFC 4028) |

## Targets

```sh
export OPENAI_API_KEY=...                 # see targets/aivc/compose.yaml
uv run --extra vad rtpbench target aivc   # about 12 minutes
```

A target is a voice agent that runs in Docker next to the reference stack, so the caller reaches
it through the same netem router (`--profiles`, `--runs` as for the cases). `rtpbench target NAME` brings it up and, from
the caller container, runs every case, a turn-latency call (12 turns) and a barge-in call
(10 turns) against it (`--only` picks among them: case names, `latency`, `barge-in`), with the
English caller lines in [`corpus/lines/en`](corpus/README.md).
`summary.md` holds the case verdicts, then turn latency and barge-in over every turn of every
repeat per profile (with the spread of the per-run medians and stop rates, and the error bar
of each); `report.html` the case timelines; `target.log` the target's own logs.

| target | what |
| --- | --- |
| [`aivc`](targets/aivc) | [OpenSIPS AI Voice Connector CE](https://github.com/OpenSIPS/opensips-ai-voice-connector-ce) at a pinned commit, OpenSIPS 3.6 (images pinned by digest), openai flavor as upstream's example sets it, plus a transfer target. Needs `OPENAI_API_KEY`; `OPENAI_URL` points it at another Realtime endpoint (e.g. Azure OpenAI `wss://<resource>.openai.azure.com/openai/v1/realtime?model=<deployment>`) |

## Results

First published results, 2026-10-13: the reference agent and
[OpenSIPS AI Voice Connector CE](https://github.com/OpenSIPS/opensips-ai-voice-connector-ce),
every call repeated 10 times under each network profile. Summaries, per-call records and the HTML
reports (with a timeline per call) are in [`results/first`](results/first); the captures are not
published.

```sh
uv run --extra vad rtpbench cases --profiles clean,lte,lte-bad --runs 10           # reference agent
uv run --extra vad rtpbench target aivc --profiles clean,lte,lte-bad --runs 10     # needs OPENAI_API_KEY
```

Conditions: WSL2 Ubuntu 24.04 (kernel 6.18.54.1), Docker 29.8.2;
python:3.14.8-slim and tcpdump 4.99.5 in the containers. Calls placed at commit 461a75e (the codec
cases at 6cb5866), judged at 144b4ee. Repeat k used seed k. Each profile of each target ran as
its own process, six at once. AI Voice Connector CE at 09e14d0 with OpenSIPS 3.6.9, openai flavor
as in upstream's example, engine Azure OpenAI `gpt-realtime-2.1` (2026-07-07)
through `OPENAI_URL`; the agent's latency includes the engine's.

### Cases

A cell is the verdict over 10 repeats and, for the agent, the case's main timing as median
[min, max] in ms with its error bar: (−24/+88) means the true value lies between 24 ms below
and 88 ms above the measured one. The
reference agent column covers every behaviour of the case, the one that should pass and each
one that should fail, under clean, `lte` and `lte-bad`.

| case | reference agent | AIVC CE, clean | AIVC CE, lte | AIVC CE, lte-bad | why AIVC CE fails |
| --- | --- | --- | --- | --- | --- |
| `greeting` | proven 30/30 | **flips** pass 7, fail 3; 1387 [1131, 5812] (−24/+88) | **flips** pass 6, fail 4; 1406 [1184, 2699] (−25/+88) | **flips** pass 7, fail 3; 1300 [1195, 4643] (−35/+97) | greets after 2 s in 10 of 30 calls (it opens its AI session after answering) |
| `bye` | proven 30/30 | pass 10/10; last RTP −9 [−20, 1] after the BYE (±0.4) | pass 10/10; 37 [−23, 43] | pass 10/10; 47 [4, 65] | |
| `cancel` | proven 30/30 | inconclusive 10/10 | inconclusive 10/10 | inconclusive 10/10 | answers 2 ms after its 100 Trying, so there is no ringing to cancel |
| `hold` | proven 30/30 | fail 10/10 | fail 10/10 | fail 10/10 | answers an `inactive` offer `recvonly` (RFC 3264 6.1) |
| `dtmf-rfc4733` | proven 30/30 | fail 10/10 | fail 10/10 | fail 10/10 | no telephone-event in the answer |
| `dtmf-info` | proven 30/30 | fail 10/10 | fail 10/10 | fail 10/10 | INFO never answered (487 after 40 s) |
| `refer` | proven 30/30 | pass 10/10; NOTIFY to BYE 1550 [631, 3128] (±0.4) | pass 10/10; 2040 [1357, 3045] | pass 10/10; 2237 [1079, 3568] | |
| `refer-fail` | proven 30/30 | fail 10/10 | fail 10/10 | fail 10/10 | hangs up after the 486 sipfrag instead of taking the call back (RFC 5589 6.3) |
| `codec-pcmu` | proven 30/30 | pass 10/10 | pass 10/10 | pass 10/10 | |
| `codec-pcma` | proven 30/30 | pass 10/10 | pass 10/10 | pass 10/10 | |
| `timer` | proven 30/30 | fail 10/10 | fail 10/10 | fail 10/10 | no session timers in the 2xx |

Reference agent speech timings against its truth, clean (median [min, max] over 10 repeats,
ms): greeting +9.3 [−0.6, +29.5]; DTMF reaction +9.6 [−0.6, +49.5] (RFC 4733) and +17.9
[−1.8, +48.3] (INFO); retake after a failed transfer +15.3 [−5.4, +47.5]. That is 4 of 40
outside the PCMU bar (−3.8..+32.9, a p5..p95 range).

### Turn latency and barge-in, AIVC CE

Turn latency: the caller's labelled end of speech to the agent's first speech (webrtcvad), 12
turns per call, every turn of every repeat.

| profile | answered | p5 | p50 | p95 | per-run medians | error bar |
| --- | --- | --- | --- | --- | --- | --- |
| clean | 120/120 | 795 | 1109 | 4682 | 1000 .. 2281 | −24 / +88 |
| lte | 120/120 | 833 | 1209 | 3656 | 1050 .. 1839 | −25 / +88 |
| lte-bad | 120/120 | 905 | 1206 | 4753 | 1057 .. 2802 | −35 / +97 |

Barge-in: whether the agent stopped within 2 s of the caller cutting in, and its stop time (gate)
when it did; 10 turns per call.

| profile | interruption stopped | stop time p50 [p5, p95] | backchannel stopped | cough stopped | error bar |
| --- | --- | --- | --- | --- | --- |
| clean | 51/51 | 287 [−66, 560] | 21/25 | 1/24 | +0 / +72 |
| lte | 49/50 | 368 [205, 801] | 24/25 | 0/24 | +0 / +72 |
| lte-bad | 51/51 | 404 [64, 764] | 24/25 | 0/24 | +0 / +119 |

So AI Voice Connector CE, behind this engine, answers a turn in about 1.1-1.2 s at the median
on every profile, with a long tail (p95 3.7-4.8 s). It stops for real interruptions in ~0.3-0.4
s, but also for most backchannels ("uh-huh", "okay"): 69 of 75. Impairment moves its stop time
by about 100 ms, and none of its case verdicts. Its greeting is the one verdict that flips between
runs.

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
