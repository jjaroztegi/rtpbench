# The reference agent and AI Voice Connector CE

First published results, 2026-10-13: the reference agent and
[OpenSIPS AI Voice Connector CE](https://github.com/OpenSIPS/opensips-ai-voice-connector-ce),
every call repeated 10 times under each network profile. Summaries, per-call records and the HTML
reports (with a timeline per call) are in this folder; the captures are not published.

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

## Cases

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

## Turn latency and barge-in, AIVC CE

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
