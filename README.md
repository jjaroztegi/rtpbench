# rtpbench

Wire-level latency and conformance tests for voice agents over SIP/RTP.

rtpbench calls a voice agent over SIP, captures the RTP, and measures turn latency and barge-in
timing from the packets themselves, with and without controlled network impairment.

Status: early development. What works today: calibrations that prove how far each measurement
is from the truth a reference agent logs; 17 conformance cases, each proven against that agent
on clean and impaired paths, six of them what real trunks send, applied by a
[carrier](#carrier) between the caller and the agent; and a first open-source target with
[results](#results) direct and [through the carrier](#results-through-a-carrier).

## Calibrate

Needs Linux (or WSL2), Docker 28 or later with Compose, and [uv](https://docs.astral.sh/uv/).

```sh
uv run rtpbench calibrate            # 7 network profiles x 20 turns, about 10 minutes
uv run rtpbench calibrate --profiles clean --turns 5
```

Three containers: `caller | router | agent`. The caller places a real SIP call and speaks
scripted synthetic turns. The reference agent answers each turn after a random delay it chooses
and logs, placed to the sample. The router applies `tc netem` (to RTP only) for the profiles in
[`bench.py`](src/rtpbench/bench.py). Both endpoints run `tcpdump`; every timestamp comes from a
capture, and all containers share one kernel clock. Captures stamp the wall clock, which time
sync may step; senders schedule on the monotonic clock, so a step makes no gap in the audio, and
each run logs the steps it saw (`clock_steps` in `conditions.json`). Summaries and reports mark
what was timed across one ([`clock.py`](src/rtpbench/clock.py)).

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

The transfer target is `sip:operator@operator`, an `operator` service on the agent's side of the
router that rings for a second, answers and says a few words (or answers 486 when the transferee
asks it to be busy, for `refer-fail`). The transferee's INVITE goes through the router (and the
carrier, with `--carrier`) like any other call. Against a URI, `--proxy HOST` says where the
transferee sends it; by default it goes to the Refer-To host.

| case | what passes |
| --- | --- |
| `greeting` | the agent speaks first, within 2 s of its 200 OK |
| `bye` | caller hangs up at least a second into the agent's speech (its greeting, or its reply to a question), while it is audible: 2xx to BYE, agent RTP stops within 500 ms |
| `cancel` | caller cancels a ringing INVITE: 2xx to CANCEL, 487 to the INVITE, no RTP after |
| `hold` | hold (sendonly, then inactive) and resume by re-INVITE: answers honour the offer, no agent RTP while held, RTP back within 1 s as the same stream (SSRC, next seq, timestamps kept time) |
| `dtmf-rfc4733` | once the agent's greeting is over the caller presses 5 (RFC 4733): telephone-event negotiated, the agent says something within 5 s |
| `dtmf-info` | the same by SIP INFO (`application/dtmf-relay`): 2xx, the agent says something within 5 s |
| `refer` | the caller asks for a person and is the transferee: 202, NOTIFY sipfrag 100, a real call to the Refer-To target (the operator below, which answers), NOTIFY with its final response: REFER with a SIP or tel Refer-To, both NOTIFYs answered 2xx, the agent hangs up within 10 s |
| `refer-fail` | as `refer`, but the operator is busy, so the final NOTIFY reports `486 Busy Here`: the agent takes the call back (RFC 5589 6.3): no BYE for 10 s, and it speaks within 5 s of the failure NOTIFY |
| `codec-pcmu` | the caller offers PCMU alone: answered 2xx with PCMU alone (RFC 3264 6.1: the answer's formats come from the offer) and the agent's RTP is PCMU |
| `codec-pcma` | the same with PCMA |
| `timer` | session timers offered (90 s, caller refreshes) and refreshed once at half time, then not again: the 2xx takes them (Session-Expires, `refresher=uac`, Require: timer), the refresh gets 2xx with media undisturbed, the agent ends the session by BYE between 45 and 90 s after the refresh (RFC 4028) |
| `ssrc-change` | after the greeting the caller's audio becomes a new RTP source (new SSRC, seq and timestamps, as when media is switched upstream; RFC 3550 8): the agent replies to a question asked after it within 10 s |
| `reinvite` | after the greeting, a session refresh: re-INVITE with the same SDP (RFC 4028): 2xx `sendrecv`, the agent's media goes on undisturbed, and it replies to a question within 10 s |
| `reinvite-nosdp` | after the greeting, a re-INVITE without SDP, as PBXs send to move or audit media (RFC 3261 14.1): the 2xx offers the call's codec (14.2: MUST overlap), the caller answers in the ACK, the agent's media goes on undisturbed, and it replies to a question within 10 s |
| `hold-zero` | hold the RFC 2543 way: re-INVITE with `c=0.0.0.0` and no direction attribute, then resume (RFC 3264 8.4: an agent MUST be able to receive it, and then sends no RTP): 2xx, no agent RTP while held, RTP back within 1 s as the same stream (without the carrier only) |
| `codec-change` | after the greeting, a re-INVITE offers the other G.711 law alone and the caller switches to it on the 2xx: the answer has that law alone, the agent's RTP switches, and it replies to a question within 10 s (without the carrier only, as the codec cases) |

What a carrier sends (with `--carrier` only; the carrier applies it, the call is otherwise the
same): the call is answered and the agent replies to a question within 10 s.

| case | what reaches the agent |
| --- | --- |
| `compact-headers` | `f:`, `t:`, `i:`, `c:` for From, To, Call-ID, Content-Type (RFC 3261 7.3.3: MUST accept both forms) |
| `sdp-ssrc` | an offer with `a=ssrc:<id>` and no attribute (invalid per RFC 5576 10; reported from softphones) |
| `late-offer` | an INVITE without SDP: the agent offers in its 2xx and the ACK answers (RFC 3261 13.2.1; the default of Cisco CUCM trunks) |
| `ptime-30` | the caller's audio in 30 ms packets, offered `a=ptime:30` (RFC 3551 4.2: receivers SHOULD accept 0-200 ms) |

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
| [`aivc`](targets/aivc) | [OpenSIPS AI Voice Connector CE](https://github.com/OpenSIPS/opensips-ai-voice-connector-ce) at a pinned commit, OpenSIPS 3.6 (images pinned by digest), openai flavor as upstream's example sets it, plus a transfer target (`transfer_to`, the operator). Needs `OPENAI_API_KEY`; `OPENAI_URL` points it at another Realtime endpoint (e.g. Azure OpenAI `wss://<resource>.openai.azure.com/openai/v1/realtime?model=<deployment>`); `OPENAI_REASONING_EFFORT=` (empty) for a model without reasoning, such as gpt-realtime-1.5, as upstream's docs say |
| [`livekit`](targets/livekit) | [LiveKit](https://github.com/livekit/livekit) server and [SIP bridge](https://github.com/livekit/sip) (images pinned by digest) as livekit/sip's compose runs them, and a [LiveKit Agents](https://github.com/livekit/agents) worker on the OpenAI Realtime model through Azure OpenAI (`with_azure`, as LiveKit's Azure docs set it), given AIVC CE's instructions, welcome message, voice and tool descriptions, and a cold transfer to the operator. Needs `AZURE_OPENAI_ENDPOINT` (`https://<resource>.openai.azure.com`), `AZURE_OPENAI_API_KEY`; `AZURE_OPENAI_DEPLOYMENT` names the deployment (default `gpt-realtime-2.1`) |

### Mock engine

```sh
uv run --extra vad rtpbench target livekit --mock   # no AI engine, no key
```

`--mock` puts a deterministic stand-in for the OpenAI Realtime API (GA protocol) where the
target expects its engine ([`realtime.py`](src/rtpbench/realtime.py), [`mock/`](mock)), and
points the target's engine variables at it; the targets' own code is unchanged. It hears the
caller with the reference agent's energy gate, ends a turn after 1 s of silence, tells which of
the caller's lines was said from its energy envelope, and 1.5 s after the turn's labelled end
answers with a fixed clip (a long one to a long question) or, to the transfer line, with a call
to the transfer tool. Speech while it answers cancels the answer. It logs when it heard the end
of each turn and when it sent the first audio, on the captures' clock, so `summary.md` splits
turn latency and greeting time into the target's uplink, the engine's fixed share and the
target's downlink. What it cannot stand in for is the model: what it understands, when it
decides to transfer or stop for a backchannel.

## Carrier

```sh
uv run rtpbench calibrate --carrier --profiles clean --turns 20
uv run --extra vad rtpbench cases --carrier
uv run --extra vad rtpbench target aivc --carrier
```

`--carrier` puts a carrier between the router and the agent, as a trunk puts an SBC in front
of a PBX ([`carrier/`](carrier)): OpenSIPS 3.6 as a stateful proxy that hides the topology (the
agent sees the carrier's Via, Contact and Call-ID) and rtpengine 12.5 anchoring the media of both
legs, images pinned. The caller's leg crosses the netem router; the carrier-agent leg does not.
Every call also captures both carrier legs (`carrier.pcap`), and the calibration summary adds the
carrier's own transit time per packet.

The codec cases and `codec-change` run without the carrier only: when the agent answers with a law the caller
did not offer, rtpengine gives the caller the offered law and transcodes between the two, so
through it the case would test the carrier, not the agent.
`hold-zero` runs without the carrier only too: rtpengine passes the `c=0.0.0.0` offer on
with `a=sendonly` added, so through it the case tests a `sendonly` hold, which `hold` already
covers.

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
python:3.14.8-slim and tcpdump 4.99.5 in the containers. Calls placed at commit b08f2c3 (the codec
cases at ae4f22b), judged at dd46f39. Repeat k used seed k. Each profile of each target ran as
its own process, six at once. AI Voice Connector CE at 09e14d0 with OpenSIPS 3.6.9, openai flavor
as in upstream's example, engine Azure OpenAI `gpt-realtime-2.1` (2026-07-07)
through `OPENAI_URL`; the agent's latency includes the engine's.

Re-running these commands today does not give byte-identical captures: since #27 the refer cases
end with a final NOTIFY whose `Subscription-State` is `terminated;reason=noresource` (plain
`terminated` before). The published runs judged again at 6f6bcc3 give the same verdicts and
timings.

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

## Results through a carrier

2026-10-14: the reference agent and AI Voice Connector CE behind the [carrier](#carrier), every
call repeated 10 times under each network profile. The exception is the three signalling
mutations against AI Voice Connector CE, on clean only: SIP is never impaired, so the other
profiles cannot change what reaches the agent. Summaries, per-call records and reports are in
[`results/carrier`](results/carrier); the captures are not published.

```sh
uv run --extra vad rtpbench cases --carrier --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench cases --only ssrc-change,reinvite --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench target aivc --carrier --profiles clean,lte,lte-bad --runs 10 \
  --only greeting,bye,cancel,hold,dtmf-rfc4733,dtmf-info,refer,refer-fail,timer,ptime-30,ssrc-change,reinvite
uv run --extra vad rtpbench target aivc --carrier --profiles clean --runs 10 \
  --only compact-headers,sdp-ssrc,late-offer
uv run rtpbench calibrate --carrier --profiles clean,lte,lte-bad --turns 50
```

Conditions are those of the first results, plus OpenSIPS 3.6.9 and rtpengine 12.5.1.31 in the
carrier. Calls were placed at commit 9677e36, except the reference agent through the carrier,
placed at ba5f743: the same code with a larger capture buffer. A run at 9677e36 was voided when
the carrier's capture dropped a packet. Each profile ran as its own process.

The carrier does not change how exactly rtpbench times the wire. Through it, wire timing stays
exact against truth on all three profiles (0.00 ms), so the ±0.4 ms bar stands. Its own transit
per packet is 0.07-0.11 ms at the median and 0.13-0.22 ms at p95, with single packets up to
14 ms.

### What a carrier sends

The reference agent column covers both behaviours of each case, under clean, `lte` and `lte-bad`.
For AI Voice Connector CE, a passing cell gives the time from the end of the caller's question to
the agent's reply, as median [min, max] in ms with its error bar.

| case | what reaches the agent | reference agent | AIVC CE, clean | AIVC CE, lte | AIVC CE, lte-bad | why AIVC CE fails |
| --- | --- | --- | --- | --- | --- | --- |
| `compact-headers` | `f:` `t:` `i:` `c:` for From, To, Call-ID, Content-Type | proven 60/60 | **fail** 10/10 | | | 500 Server Internal Error |
| `sdp-ssrc` | an offer with `a=ssrc:<id>` and no attribute | proven 60/60 | **fail** 10/10 | | | no response at all: the caller gives up after 32 s |
| `late-offer` | an INVITE without SDP | proven 60/60 | **fail** 10/10 | | | 500 Server Internal Error |
| `ptime-30` | the caller's audio in 30 ms packets | proven 60/60 | pass 10/10; 1047 [978, 1138] (−24/+88) | pass 10/10; 1139 [1028, 4458] (−25/+88) | pass 10/10; 1159 [1020, 6025] (−35/+97) | |
| `ssrc-change` | the caller's audio from a new RTP source mid-call | proven 60/60, and 60/60 direct | pass 10/10; 1004 [958, 1150] (−24/+88) | pass 10/10; 1080 [970, 2263] (−25/+88) | pass 10/10; 1120 [1015, 1447] (−35/+97) | |
| `reinvite` | a session refresh (re-INVITE, same SDP) | proven 60/60, and 60/60 direct | pass 10/10; 1049 [948, 4609] (−24/+88) | pass 10/10; 1155 [1002, 3191] (−25/+88) | pass 10/10; 1156 [1009, 1256] (−35/+97) | |

### Everything else through the carrier

The carrier changes none of the reference agent's verdicts in the other cases. Every behaviour
is proven under every profile (690/690 calls); the codec cases run without the carrier
([why](#carrier)). AI Voice Connector CE gets the verdicts of the first results, with two single
flips, both from the model rather than the carrier:
- `refer` on clean: once, no REFER and no reply in 20 s, although the engine's transcript shows
  it heard the request.
- `bye` on `lte-bad`: once inconclusive, the agent silent at the BYE.

Its unanswered SIP INFO now ends in the carrier's own 408 after about 30 s.

So AI Voice Connector CE takes in its stride what a carrier does to the media: 30 ms packets, a
new RTP source mid-call, a session refresh. It fails every signalling variation at the first
message. Compact header names and a bare `a=ssrc` each have one public report behind them. An
INVITE without SDP is what Cisco Unified CM trunks send by default.

## Results with two agents

2026-10-14: [LiveKit](#targets) and AI Voice Connector CE through every case, each call repeated
10 times under each network profile, with and without the [carrier](#carrier), both on the same
engine; AI Voice Connector CE also on a second engine for the calls that depend on the model. The
reference agent proved every case again at the same commit. Signalling mutations ran on clean
only (SIP is never impaired). Summaries, per-call records and reports are in
[`results/two-targets`](results/two-targets); captures are not published.

```sh
uv run --extra vad rtpbench cases [--carrier] --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench target livekit --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench target aivc --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench target livekit --carrier --profiles clean,lte,lte-bad --runs 10 \
  --only greeting,bye,cancel,hold,dtmf-rfc4733,dtmf-info,refer,refer-fail,timer,ptime-30,ssrc-change,reinvite,reinvite-nosdp
uv run --extra vad rtpbench target livekit --carrier --profiles clean --runs 10 \
  --only compact-headers,sdp-ssrc,late-offer
# the same two for aivc, and AI Voice Connector CE on gpt-realtime-1.5:
OPENAI_REASONING_EFFORT= uv run --extra vad rtpbench target aivc --profiles clean,lte,lte-bad --runs 10 \
  --only latency,barge-in,greeting,refer,refer-fail,dtmf-rfc4733,dtmf-info
```

Engine: Azure OpenAI `gpt-realtime-2.1` (2026-07-07) for both targets and `gpt-realtime-1.5`
(2026-02-23) for AI Voice Connector CE's second run. 2.1
is AI Voice Connector CE's default and that of the maintained Realtime SDKs; LiveKit Agents
defaults to the older `gpt-realtime` alias, so its model is set explicitly. On 1.5, AI Voice
Connector CE runs with `reasoning_effort` empty, as its docs say for models without reasoning
(with the default, 1.5 rejects the session setup and the caller hears noise).

Configuration, stated plainly:
- Both targets transfer to rtpbench's operator (`sip:operator@operator`), which answers, or is
  busy for `refer-fail`. AI Voice Connector CE's `transfer_to` pointed at a dummy host in the
  earlier results, where the caller only reported the transfer.
- LiveKit's agent is ours (upstream has no SIP + Realtime compose), on LiveKit's documented
  `with_azure` and cold transfer, with AI Voice Connector CE's instructions, greeting, voice and
  tool descriptions. LiveKit converts the call audio for the engine; AI Voice Connector CE passes
  G.711 through.

Conditions: WSL2 Ubuntu 24.04 (kernel 6.18.54.1, 8 vCPUs), Docker 29.8.2; calls placed at
commit bf0e87b from a clean clone, each profile of each target its own process, six at a time
(AI Voice Connector CE on 1.5 three at a time). Two things about the host:
- Load: the six-stack runs kept the load average at 13-23 on 8 vCPUs. Turn latency was measured
  again with one stack alone (3 runs, clean, 2.1), the "alone" rows below.
- Clock: the VM's wall clock stepped back 25-80 ms about every 30 s during these runs (host time
  sync; not fixable from the guest). An interval that spans a step reads short by the step.
  7-14% of latency turns spanned one; without them the medians move by 40 ms at most.

### Cases

Reference: calls with the expected verdict over every behaviour and profile. Targets: verdicts
over the three profiles, 10 repeats each (signalling mutations: clean only).

| case | reference, direct | reference, carrier | LiveKit, direct | LiveKit, carrier | AIVC CE, direct | AIVC CE, carrier |
| --- | --- | --- | --- | --- | --- | --- |
| `greeting` | 90/90 | 90/90 | flips: pass 27, fail 3 | flips: pass 20, fail 10 | flips: pass 24, fail 6 | flips: pass 19, fail 11 |
| `bye` | 60/60 | 60/60 | pass 30/30 | flips: pass 29, inconclusive 1 | flips: pass 28, inconclusive 2 | flips: pass 29, inconclusive 1 |
| `cancel` | 60/60 | 60/60 | pass 30/30 | pass 30/30 | inconclusive 30/30 | flips: inconclusive 29, fail 1 |
| `hold` | 89/90 | 90/90 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 |
| `dtmf-rfc4733` | 60/60 | 60/60 | **fail** 30/30 | flips: fail 26, pass 4 | **fail** 30/30 | **fail** 30/30 |
| `dtmf-info` | 60/60 | 60/60 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 |
| `refer` | 90/90 | 90/90 | flips: pass 29, fail 1 | flips: pass 29, fail 1 | pass 30/30 | flips: pass 28, fail 2 |
| `refer-fail` | 90/90 | 90/90 | pass 30/30 | flips: pass 28, fail 2 | **fail** 30/30 | **fail** 30/30 |
| `codec-pcmu` | 60/60 | – | pass 30/30 | – | pass 30/30 | – |
| `codec-pcma` | 60/60 | – | pass 30/30 | – | pass 30/30 | – |
| `timer` | 90/90 | 90/90 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 |
| `compact-headers` | – | 60/60 | – | pass 10/10 | – | **fail** 10/10 |
| `sdp-ssrc` | – | 60/60 | – | pass 10/10 | – | **fail** 10/10 |
| `late-offer` | – | 60/60 | – | **fail** 10/10 | – | **fail** 10/10 |
| `ptime-30` | – | 60/60 | – | pass 30/30 | – | pass 30/30 |
| `ssrc-change` | 60/60 | 60/60 | pass 30/30 | flips: pass 29, fail 1 | pass 30/30 | flips: pass 28, fail 2 |
| `reinvite` | 60/60 | 60/60 | pass 30/30 | flips: pass 29, fail 1 | flips: pass 29, fail 1 | pass 30/30 |
| `reinvite-nosdp` | 60/60 | 60/60 | pass 30/30 | flips: pass 29, fail 1 | **fail** 30/30 | **fail** 30/30 |
| `hold-zero` | 60/60 | – | **fail** 30/30 | – | **fail** 30/30 | – |
| `codec-change` | 60/60 | – | **fail** 30/30 | – | **fail** 30/30 | – |

- `hold`, reference direct: the one miss (lte-bad, 1 of 10 good-agent calls) is a clock step
  inside the call: two packets "arrived" 38-58 ms before the agent's own capture sent them.
  Run again under `lte-bad` (`--only hold --runs 10`), every behaviour was proven, 30/30
  ([`reference-hold-rerun`](results/two-targets/reference-hold-rerun)).
- Both fail `hold-zero` and `codec-change` the same way: they keep sending to a `c=0.0.0.0`
  hold, and answer a codec change with the old codec (RFC 3264 6.1).
- LiveKit rings, so `cancel` runs and passes (487); answers a hold `sendrecv` and keeps sending;
  reacts to no digit (its default agent
  does not handle DTMF; INFO gets 405); takes the call back after a failed transfer; accepts
  compact headers and a bare `a=ssrc`; rejects an INVITE without SDP with `400` (late offer is
  behind a feature flag).
- AI Voice Connector CE fails what it failed before, plus `reinvite-nosdp` (no response; the
  transaction ends 487), and keeps every passing verdict.
- Flips are the model's: a late greeting, no REFER, no reply within 10 s; LiveKit's 4 `dtmf-rfc4733`
  passes through the carrier are speech that happened to fall within 5 s of the digit.

### Turn latency and barge-in

Turn latency (ms): the caller's labelled end of speech to the agent's first speech, 12 turns per
call; bar: the true value lies between the first and second number around the measured one.

| target | engine | profile | runs | answered | p50 | p95 | run medians | bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LiveKit | 2.1 | clean | 10 | 120/120 | 1654 | 3984 | 1543 .. 2029 | −33/+4 |
| LiveKit | 2.1 | lte | 10 | 115/120 | 1695 | 6328 | 1569 .. 1969 | −32/+3 |
| LiveKit | 2.1 | lte-bad | 10 | 119/120 | 1831 | 3518 | 1657 .. 2244 | −52/+17 |
| LiveKit | 2.1, alone | clean | 3 | 36/36 | 1455 | 2697 | 1355 .. 1503 | −33/+4 |
| AIVC CE | 2.1 | clean | 10 | 120/120 | 1178 | 5340 | 1060 .. 2509 | −24/+88 |
| AIVC CE | 2.1 | lte | 10 | 120/120 | 1319 | 5175 | 1197 .. 3003 | −25/+88 |
| AIVC CE | 2.1 | lte-bad | 10 | 120/120 | 1330 | 5959 | 1102 .. 3304 | −35/+97 |
| AIVC CE | 2.1, alone | clean | 3 | 36/36 | 1042 | 1376 | 1012 .. 1085 | −24/+88 |
| AIVC CE | 1.5 | clean | 10 | 120/120 | 827 | 1274 | 808 .. 892 | −24/+88 |
| AIVC CE | 1.5 | lte | 10 | 120/120 | 901 | 1294 | 852 .. 971 | −25/+88 |
| AIVC CE | 1.5 | lte-bad | 10 | 120/120 | 963 | 1468 | 910 .. 1221 | −35/+97 |

Barge-in: whether the agent stopped within 2 s of the caller cutting in, and its stop time (ms)
when it did; 10 turns per call.

| target | engine | profile | interruptions stopped | stop time p50 (bar) | backchannels stopped | coughs stopped |
| --- | --- | --- | --- | --- | --- | --- |
| LiveKit | 2.1 | clean | 49/50 | 707 (+0/+79) | 21/25 | 1/22 |
| LiveKit | 2.1 | lte | 47/49 | 768 (+0/+71) | 21/22 | 1/22 |
| LiveKit | 2.1 | lte-bad | 46/49 | 896 (−5/+94) | 19/21 | 3/21 |
| AIVC CE | 2.1 | clean | 48/48 | 294 (+0/+72) | 18/21 | 0/21 |
| AIVC CE | 2.1 | lte | 50/51 | 409 (+0/+72) | 21/25 | 0/24 |
| AIVC CE | 2.1 | lte-bad | 49/51 | 424 (+0/+119) | 20/25 | 0/24 |
| AIVC CE | 1.5 | clean | 51/51 | 312 (+0/+72) | 18/25 | 0/24 |
| AIVC CE | 1.5 | lte | 50/50 | 352 (+0/+72) | 15/25 | 0/24 |
| AIVC CE | 1.5 | lte-bad | 46/46 | 385 (+0/+119) | 12/22 | 0/22 |

So, on the same engine, LiveKit answers a turn 0.4-0.5 s later than AI Voice Connector CE at the
median, alone or under load, and stops for an interruption 0.4-0.5 s later. Both stop for most
backchannels and almost never for a cough. AI Voice Connector CE on gpt-realtime-1.5 answers about
0.2 s sooner than on 2.1 alone, with a short tail (p95 1.3-1.5 s); its verdicts are those of 2.1,
with the greeting on time more often (28/30 vs 24/30) and two missed transfers (refer 28/30).
The long tail of 2.1 in the six-stack runs (p95 4-6 s) did not
show alone; with 36 turns alone, load and time of day are not separated.

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
