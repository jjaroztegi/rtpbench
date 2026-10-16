# LiveKit and AI Voice Connector CE on a real engine

2026-10-14: [LiveKit](../../docs/targets.md) and AI Voice Connector CE through every case, each call repeated
10 times under each network profile, with and without the [carrier](../../docs/targets.md#carrier), both on the same
engine; AI Voice Connector CE also on a second engine for the calls that depend on the model. The
reference agent proved every case again at the same commit. Signalling mutations ran on clean
only (SIP is never impaired). Summaries, per-call records and reports are in
this folder; captures are not published.

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
  [earlier results](../first), where the caller only reported the transfer.
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

## Cases

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
  ([`reference-hold-rerun`](reference-hold-rerun)).
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

## Turn latency and barge-in

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

The carrier columns predate a carrier fix; see
[a correction](../bare-metal-mock#a-correction-to-the-earlier-carrier-results).
