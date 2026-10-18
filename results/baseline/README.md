# Baseline: both targets on a mock engine

2026-10-17: every case proven on the reference agent and run against LiveKit and AI Voice
Connector CE, direct and through the [carrier](../../docs/targets.md#carrier), under three network
profiles, 10 repeats each, with both targets on the [mock engine](../../docs/targets.md#mock-engine)
instead of a paid AI engine, so every verdict is the connector's and the engine's share of each
turn is known. Every set below is one `rtpbench` invocation from a clean checkout at commit
4b0b7bc. Senders schedule on the monotonic clock and every run logs wall-clock steps:
0 were seen. Summaries, records and reports are in this folder; the raw run directories
(captures, logs, the reference agent's truth) are [archived](#raw-runs).

```sh
uv run rtpbench calibrate [--carrier]
uv run --extra vad rtpbench cases [--carrier] --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench target livekit --mock --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench target livekit --mock --carrier --profiles clean,lte,lte-bad --runs 10 \
  --only greeting,bye,cancel,hold,dtmf-rfc4733,dtmf-info,refer,refer-fail,timer,ptime-30,ssrc-change,reinvite,reinvite-nosdp,compact-headers,sdp-ssrc,late-offer
# the same for aivc
```

Conditions: 16 CPUs, kernel 6.8.0-147-generic, CPU governor `performance`, Docker 29.9.1;
python 3.14.8 and tcpdump 4.99.5 in the containers. The six case sets ran at once, each
its own stack; the load average reached 8.9. The calibrations ran alone, after them.
Engine: the mock, which waits 1000 ms of silence and answers 500 ms later. AI Voice
Connector CE and LiveKit at the versions in [targets](../../docs/targets.md), every Python
package pinned.

## Timing on this host

Wire timing against the reference agent's truth (max abs error, ms), direct and through the
carrier, 20 turns per profile, and the time the carrier adds per packet:

| profile | turns | wire − truth, direct: max abs | through the carrier: max abs | carrier transit p50 / p95 / max |
| --- | --- | --- | --- | --- |
| clean | 20 | 0.00 | 0.00 | 0.05 / 0.08 / 2.3 |
| delay | 20 | 0.00 | 0.00 | 0.05 / 0.08 / 2.7 |
| jitter | 20 | 0.00 | 0.00 | 0.04 / 0.07 / 2.9 |
| loss | 20 | 0.00 | 0.12 | 0.05 / 0.07 / 0.9 |
| mobile | 20 | 0.00 | 0.00 | 0.04 / 0.07 / 3.2 |
| lte | 20 | 0.00 | 0.00 | 0.04 / 0.07 / 2.2 |
| lte-bad | 20 | 0.00 | 0.00 | 0.05 / 0.09 / 0.9 |

Sender lateness, both ends, direct, 57017 packets: p50 0.010, p99 0.050, max 2.65 ms

How far concurrent stacks can go before timing suffers: N reference stacks at once, 60 turns
each, clean (an earlier wave, commit e37a944; the caller, the reference agent and their
stacks have changed since only by a progress line the caller prints). Wire against truth; the reference agent's scheduling error; how late each sender's
packets left against its own 20 ms grid (from its capture); capture drops; load average (1 min):

| N | turns | wire-truth p99 / max | agent sched p99 / max | late caller p99 / max | late agent p99 / max | > 10 ms late | drops | load mean / max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 60 | 0.00 / 0.00 | 0.10 / 0.10 | 0.04 / 0.06 | 0.04 / 4.07 | 0 | 0 | 2.0 / 3.2 |
| 2 | 120 | 0.00 / 0.00 | 0.11 / 0.11 | 0.04 / 1.81 | 0.04 / 1.69 | 0 | 0 | 3.1 / 5.7 |
| 4 | 240 | 0.00 / 0.00 | 0.09 / 0.10 | 0.04 / 2.07 | 0.04 / 3.17 | 0 | 0 | 2.5 / 3.3 |
| 6 | 360 | 0.00 / 0.00 | 0.10 / 0.13 | 0.04 / 4.08 | 0.04 / 2.81 | 0 | 0 | 1.8 / 2.4 |
| 8 | 480 | 0.00 / 0.00 | 0.10 / 0.45 | 0.04 / 3.81 | 0.04 / 2.44 | 0 | 0 | 2.4 / 3.5 |
| 10 | 600 | 0.00 / 0.00 | 0.10 / 1.18 | 0.04 / 2.59 | 0.04 / 3.46 | 0 | 0 | 2.6 / 3.5 |
| 12 | 720 | 0.00 / 0.00 | 0.10 / 0.44 | 0.04 / 3.98 | 0.04 / 3.25 | 0 | 0 | 3.2 / 4.3 |

Nothing degrades up to 12 reference stacks. Target stacks weigh more and were not measured this
way; the wire timing of the cases below rests on the calibrations above.

## Detector error bars, held out

The speech onset and barge-in stop bars in the code are the p5..p95 of seeds 1-5
(`calibrate --speech`, `calibrate --barge-in`, pooled with `rtpbench analyze`). Seeds 6-10, run
the same way at commit ba41c79 (the detector, the caller and the reference agent have
changed since only by that progress line), against them: a p5..p95 bar leaves about 10% outside.

| bar | profile | codec | shipped | turns | below | above | outside |
| --- | --- | --- | --- | --- | --- | --- | --- |
| onset | clean | PCMU | [-3.2, +44.6] | 215 | 7 | 7 | 7% |
| onset | clean | PCMA | [-133.0, +11.0] | 215 | 14 | 13 | 13% |
| onset | lte | PCMU | [-3.6, +43.3] | 215 | 14 | 9 | 11% |
| onset | lte | PCMA | [-131.0, +14.1] | 215 | 14 | 15 | 13% |
| onset | lte-bad | PCMU | [-15.5, +60.9] | 215 | 13 | 11 | 11% |
| onset | lte-bad | PCMA | [-141.5, +22.9] | 215 | 13 | 15 | 13% |
| first onset | clean | PCMU | [+1.0, +63.6] | 215 | 10 | 12 | 10% |
| first onset | clean | PCMA | [+1.1, +64.9] | 215 | 16 | 10 | 12% |
| first onset | lte | PCMU | [-0.8, +67.6] | 215 | 13 | 11 | 11% |
| first onset | lte | PCMA | [-2.5, +67.7] | 215 | 6 | 12 | 8% |
| first onset | lte-bad | PCMU | [-11.4, +109.8] | 215 | 12 | 8 | 9% |
| first onset | lte-bad | PCMA | [-13.1, +102.9] | 215 | 11 | 6 | 8% |
| stop | clean | PCMU | [-84.8, +0.0] | 230 | 13 | 0 | 6% |
| stop | clean | PCMA | [-84.9, +0.0] | 230 | 12 | 0 | 5% |
| stop | lte | PCMU | [-81.9, +0.0] | 230 | 20 | 2 | 10% |
| stop | lte | PCMA | [-77.6, +0.0] | 230 | 20 | 1 | 9% |
| stop | lte-bad | PCMU | [-104.9, +0.0] | 230 | 10 | 6 | 7% |
| stop | lte-bad | PCMA | [-100.7, +0.0] | 230 | 18 | 4 | 10% |

## Cases on the mock engine

Reference: calls with the expected verdict over every behaviour and profile. Targets: verdicts
over the three profiles, 10 repeats each. Last column: what a deterministic engine can judge of
the case.

| case | reference, direct | reference, carrier | LiveKit, direct | LiveKit, carrier | AIVC CE, direct | AIVC CE, carrier | a mock judges |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `greeting` | 90/90 | 90/90 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | stack's time, not the model's |
| `bye` | 60/60 | 60/60 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | yes |
| `cancel` | 60/60 | 60/60 | pass 30/30 | pass 30/30 | inconclusive 30/30 | inconclusive 30/30 | yes |
| `hold` | 90/90 | 90/90 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | yes |
| `dtmf-rfc4733` | 60/60 | 60/60 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | digit reaches the engine |
| `dtmf-info` | 60/60 | 60/60 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | digit reaches the engine |
| `refer` | 90/90 | 90/90 | pass 30/30 | flips: pass 29, fail 1 | pass 30/30 | pass 30/30 | transfer mechanics |
| `refer-fail` | 90/90 | 90/90 | pass 30/30 | pass 30/30 | **fail** 30/30 | **fail** 30/30 | failure handed back |
| `codec-pcmu` | 60/60 | – | pass 30/30 | – | pass 30/30 | – | yes |
| `codec-pcma` | 60/60 | – | pass 30/30 | – | pass 30/30 | – | yes |
| `timer` | 90/90 | 90/90 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | yes |
| `compact-headers` | – | 60/60 | – | pass 30/30 | – | **fail** 30/30 | yes |
| `sdp-ssrc` | – | 60/60 | – | pass 30/30 | – | **fail** 30/30 | yes |
| `late-offer` | – | 60/60 | – | **fail** 30/30 | – | **fail** 30/30 | yes |
| `ptime-30` | – | 60/60 | – | pass 30/30 | – | pass 30/30 | yes |
| `ssrc-change` | 60/60 | 60/60 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | yes |
| `large-invite` | 60/60 | – | pass 30/30 | – | **fail** 30/30 | – | yes |
| `reinvite` | 60/60 | 60/60 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | yes |
| `reinvite-nosdp` | 60/60 | 60/60 | pass 30/30 | pass 30/30 | **fail** 30/30 | **fail** 30/30 | yes |
| `hold-zero` | 60/60 | – | **fail** 30/30 | – | **fail** 30/30 | – | yes |
| `codec-change` | 60/60 | – | **fail** 30/30 | – | **fail** 30/30 | – | yes |

- What a mock can judge: the SIP and media cases test the connector alone (whether a hold stops
  its media, whether it takes a codec change, a re-INVITE without SDP, an INVITE over TCP); the
  engine only has to hear the caller and answer, which the mock always does. Around a model's
  decision it judges the mechanics: `greeting` times the stack with a fixed engine; `refer`, the
  REFER once the tool is called; `refer-fail`, whether the failure goes back to the engine so the
  agent can speak; the DTMF cases, whether a digit reaches the engine at all. Whether a model
  greets in time, asks for the transfer or stops for a backchannel, it cannot say.
- One verdict flipped between repeats: LiveKit `refer` through the carrier, lte
  repeat 6: the carrier relayed the 202 Accepted to LiveKit
  0.7 ms after its REFER and the first NOTIFY 0.2 ms after that; LiveKit logged the REFER as
  "transaction failed to complete (0 intermediate responses)", answered the final NOTIFY (200 OK)
  5 s late, after three retransmissions, and stayed on the call. In the other 29 repeats, and in
  all 30 of each earlier wave on the mock, it hung up.
- `large-invite`: an INVITE over 1300 bytes, sent over TCP as RFC 3261 18.1.1 requires. LiveKit's
  SIP bridge listens on TCP and takes it. AI Voice Connector CE's example configuration opens a
  UDP socket only, so the connection is refused and the call goes nowhere (the caller's UDP
  retry is answered).

## Turn latency, split

Where each target's time goes with the engine held fixed: uplink is from the caller's labelled
end of speech on the wire to when the mock heard it end; engine, the mock's own wait; downlink,
from the mock's first audio to the agent's speech on the wire. ms, p50 [p5, p95]; bar: the
detector's error bar for the profile and codec.

| target | profile | turns | wire latency | uplink | engine | downlink | onset bar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LiveKit | clean | 120 | 1833 [1713, 1893] | 186 [60, 203] | 1501 [1501, 1503] | 149 [134, 197] | −45/+3 |
| LiveKit | lte | 120 | 1997 [1879, 2109] | 302 [196, 401] | 1501 [1501, 1502] | 189 [170, 232] | −43/+4 |
| LiveKit | lte-bad | 120 | 2134 [1924, 2273] | 426 [267, 582] | 1501 [1501, 1502] | 201 [157, 258] | −61/+16 |
| AIVC CE | clean | 120 | 1512 [1504, 1524] | 1 [-2, 4] | 1501 [1501, 1501] | 10 [3, 22] | −11/+133 |
| AIVC CE | lte | 120 | 1592 [1582, 1606] | 40 [33, 45] | 1501 [1500, 1502] | 51 [43, 62] | −14/+131 |
| AIVC CE | lte-bad | 120 | 1605 [1553, 1663] | 45 [9, 83] | 1501 [1500, 1502] | 61 [24, 104] | −23/+142 |

Greeting: from the 200 OK to the agent's first speech, split the same way (the request is when
the target asked the engine to speak, against its 200 OK):

| target | profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- | --- |
| LiveKit | clean | 10 | 681 [604, 698] | -21 [-100, -8] | 501 [500, 503] | 203 [187, 210] |
| LiveKit | lte | 10 | 727 [714, 743] | -6 [-12, 5] | 501 [501, 501] | 235 [222, 240] |
| LiveKit | lte-bad | 10 | 733 [725, 806] | -8 [-30, -3] | 501 [501, 502] | 238 [235, 314] |
| AIVC CE | clean | 10 | 541 [541, 542] | 3 [2, 5] | 501 [500, 501] | 37 [35, 39] |
| AIVC CE | lte | 10 | 578 [563, 590] | 2 [2, 3] | 501 [501, 501] | 75 [59, 87] |
| AIVC CE | lte-bad | 10 | 591 [553, 633] | 2 [2, 7] | 501 [501, 502] | 88 [45, 129] |

Barge-in: the mock cancels its answer on the first voiced 10 ms of the caller, so what is left is
the target's own path. Stopped within 2 s, and the stop time p50 (ms):

| target | profile | interruptions stopped | backchannels stopped | coughs stopped | stop bar |
| --- | --- | --- | --- | --- | --- |
| LiveKit | clean | 51/51, p50 306 | 25/25, p50 296 | 24/24, p50 283 | +0/+85 |
| LiveKit | lte | 51/51, p50 459 | 25/25, p50 441 | 24/24, p50 438 | +0/+82 |
| LiveKit | lte-bad | 51/51, p50 579 | 25/25, p50 619 | 24/24, p50 545 | +0/+105 |
| AIVC CE | clean | 51/51, p50 24 | 25/25, p50 4 | 24/24, p50 -9 | +0/+85 |
| AIVC CE | lte | 51/51, p50 103 | 25/25, p50 86 | 24/24, p50 74 | +0/+78 |
| AIVC CE | lte-bad | 51/51, p50 128 | 25/25, p50 72 | 24/24, p50 87 | +0/+101 |

So, with the engine held fixed, LiveKit's media path adds 324 ms to a turn at the median on
clean (its uplink and downlink against AI Voice Connector CE's). How each drives a real engine
(24 kHz PCM against G.711 passed through, and the engine's own speech detection settings) is
not measured here.

## Raw runs

Attached to the [release](../../docs/README.md#published-results) as `.tar.zst`; each unpacks to
the directory `rtpbench` wrote. The held-out detector seeds and the capacity curve are from the
commits named above.

| archive | SHA-256 |
| --- | --- |
| `baseline-reference-direct-4b0b7bc.tar.zst` | `d84afc6307988fb4995c284051eaaa1ff81d5ffdffb09d50ffde5ea35bb4ee77` |
| `baseline-reference-carrier-4b0b7bc.tar.zst` | `d6c80595d3cbc9c817ad088ec47ebe5a95d004d316494edb1f548563806cd68c` |
| `baseline-aivc-direct-4b0b7bc.tar.zst` | `965607623e8f1bf2444f92fcb6fbe1cdc20ec7056ec87daf8381bd74a177e8aa` |
| `baseline-livekit-direct-4b0b7bc.tar.zst` | `0adfa0b69428b4d9db01219b16e9acab65960f05f06ab2f386a691c0aaa65024` |
| `baseline-aivc-carrier-4b0b7bc.tar.zst` | `e7ea6a8a22ba514ff9c3d4a00b1990bc0dd122aae45e72ccde580748bb179639` |
| `baseline-livekit-carrier-4b0b7bc.tar.zst` | `ff309a7bec0ca2ca4872c793cb13539bc8148f058d67dbd10471d138849c5822` |
| `baseline-calibrate-4b0b7bc.tar.zst` | `fffe4f33a84ea57d5e46bb67994e22e93eb9f7d4628eb297a50d92309576c1c6` |
| `baseline-calibrate-carrier-4b0b7bc.tar.zst` | `9edfcb7f66fc181b786f5c2ffaea49d324377bfa83fb40020472ce6a052f31a5` |
| `baseline-detector-seeds6-10-ba41c79.tar.zst` | `74fae489b78b11301805a42a49a9ea39463cf0bdd40c353f14128df09e89aea5` |
| `baseline-capacity-e37a944.tar.zst` | `9aa82807b06c188d4ce4727562e482ecc7315d9830937c72813f51632dc2dfee` |

