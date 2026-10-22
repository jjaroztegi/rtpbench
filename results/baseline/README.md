# Baseline: both targets on a mock engine

2026-10-17: every case proven on the reference agent and run against LiveKit and AI Voice
Connector CE, direct and through the [carrier](../../docs/targets.md#carrier), under three network
profiles, 10 repeats each, with both targets on the [mock engine](../../docs/targets.md#mock-engine)
instead of a paid AI engine, so every verdict is the connector's and the engine's share of each
turn is known. Every set below is one `rtpbench` invocation of the same code, image
`rtpbench:ad0a03d9c585`. Senders schedule on the monotonic clock and every run logs wall-clock
steps: 0 were seen. Summaries, records and reports are in this folder; the raw run directories
(captures, logs, the reference agent's truth) are [archived](#raw-runs). The image tag is a hash
of `src`, the `Dockerfile` and the corpus, so it names this code in any clone; `commit` in
`conditions.json` is `git describe` in the checkout that ran it. The git tag `baseline` is a
commit with this code: `git checkout baseline` to run it again.

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
each, clean (an earlier wave, image `rtpbench:ba330eecbd02`; the caller, the reference agent
and their stacks have changed since only by a progress line the caller prints). Wire against
truth; the reference agent's scheduling error; how late each sender's
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
the same way with image `rtpbench:965085c223d2` (the detector, the caller and the reference
agent have changed since only by that progress line), against them: a p5..p95 bar leaves about
10% outside.

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

Every call's SIP, speech and RTP on one timeline: reference [direct](https://jjaroztegi.github.io/rtpbench/baseline/reference-direct/report.html), [carrier](https://jjaroztegi.github.io/rtpbench/baseline/reference-carrier/report.html); LiveKit [direct](https://jjaroztegi.github.io/rtpbench/baseline/livekit-direct/report.html), [carrier](https://jjaroztegi.github.io/rtpbench/baseline/livekit-carrier/report.html); AI Voice Connector CE [direct](https://jjaroztegi.github.io/rtpbench/baseline/aivc-direct/report.html), [carrier](https://jjaroztegi.github.io/rtpbench/baseline/aivc-carrier/report.html).

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
| `timer` | 90/90 | 90/90 | inconclusive 30/30 | inconclusive 30/30 | inconclusive 30/30 | inconclusive 30/30 | yes |
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
  all 30 of each earlier wave on the mock, it hung up. The cause is a race in LiveKit's SIP
  stack: the 202 was handled before the REFER's transaction had set its UDP timers, so the
  transaction was deleted with the 202 unread
  ([livekit/sip#906](https://github.com/livekit/sip/issues/906), fix proposed in
  [livekit/sipgo#18](https://github.com/livekit/sipgo/pull/18)).
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
the target's own path. Stopped within 2 s, and the stop time p50 (ms), of the interjections made
while the agent spoke: a turn whose speech the gate heard end before the interjection, by more
than the stop bar, is left out (14, 10 and 10 per profile for AI Voice Connector CE, 3 on clean
for LiveKit):

| target | profile | interruptions stopped | backchannels stopped | coughs stopped | stop bar |
| --- | --- | --- | --- | --- | --- |
| LiveKit | clean | 51/51, p50 306 | 24/24, p50 296 | 22/22, p50 293 | +0/+85 |
| LiveKit | lte | 51/51, p50 459 | 25/25, p50 441 | 24/24, p50 438 | +0/+82 |
| LiveKit | lte-bad | 51/51, p50 579 | 25/25, p50 619 | 24/24, p50 545 | +0/+105 |
| AIVC CE | clean | 47/47, p50 37 | 21/21, p50 22 | 18/18, p50 5 | +0/+85 |
| AIVC CE | lte | 48/48, p50 104 | 22/22, p50 87 | 20/20, p50 80 | +0/+78 |
| AIVC CE | lte-bad | 47/47, p50 141 | 22/22, p50 89 | 21/21, p50 96 | +0/+101 |

So, with the engine held fixed, LiveKit's media path adds 324 ms to a turn at the median on
clean (its uplink and downlink against AI Voice Connector CE's). How each drives a real engine
(24 kHz PCM against G.711 passed through, and the engine's own speech detection settings) is
not measured here.

## The connectors' RTP

How evenly each connector's audio reached the caller (RTP pacing in each set's summary): late,
the p99 of how much later than their RTP timestamps the packets arrived, against the earliest
before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550
interarrival jitter estimate, its median over a call. ms, late / jitter, the median over every
call of the set (120 to 180 per profile); the reference agent's show what the network and the
carrier add by themselves.

| profile | route | reference agent | LiveKit | AIVC CE |
| --- | --- | --- | --- | --- |
| clean | direct | 0.2 / 0.02 | 21.1 / 0.19 | 1.2 / 0.13 |
| clean | carrier | 0.7 / 0.04 | 21.2 / 0.22 | 1.4 / 0.25 |
| lte | direct | 15.7 / 3.28 | 34.4 / 3.34 | 15.9 / 3.33 |
| lte | carrier | 15.7 / 3.30 | 34.2 / 3.35 | 15.7 / 3.32 |
| lte-bad | direct | 105.6 / 20.02 | 122.6 / 20.10 | 106.6 / 20.13 |
| lte-bad | carrier | 106.3 / 20.19 | 120.6 / 20.20 | 105.2 / 20.07 |

LiveKit's stream falls 20 ms behind its own timestamps once in a call: at its 210th packet,
4.2-4.3 s after its 200 OK, it leaves a 20 ms slot empty without advancing the RTP timestamp,
and stays 20 ms late to the end. It does so in every call long enough. The cause is the
resampler that takes the room's 48 kHz audio to the call's 8 kHz: on the 212th 20 ms frame it
returns one sample short, and the writer holds the whole frame back
([livekit/media-sdk#109](https://github.com/livekit/media-sdk/issues/109)). In `ptime-30` the caller
does not see it: LiveKit still sends 20 ms packets and slips on its own leg (`carrier.pcap`),
but rtpengine, repacketizing the call for the 30 ms the carrier offered LiveKit, sends them on
to the caller on its own clock. A receiver needs a 21.1 ms jitter buffer for LiveKit's stream on a
clean network, or fills a 20 ms gap 4 s into every call; the jitter estimate barely shows it.
On a mobile path the slip adds to what the network needs (34 ms against 16 under `lte`). AI
Voice Connector CE needs 1.2 ms on a clean network. Neither stops sending RTP for a
second or more outside a hold: both send silence between replies.

## The connectors' audio

The engine's answers as the caller received them (engine audio in the direct sets' summaries:
220 to 240 completed answers per profile in the latency and barge-in calls), each piece of speech
aligned with what the mock sent, median over answers. Distortion is the audio against what no
linear filter of ±4 ms explains (G.711 alone leaves about 37 dB); moved counts answers where a
piece came out 5 ms or more later or earlier than the one before it.

| target | profile | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB |
| --- | --- | --- | --- | --- | --- | --- |
| LiveKit | clean | 0 of 240 | 27.5 | 14, up to 40 ms | -0.2 | -8.3 |
| LiveKit | lte | 0 of 240 | 27.4 | 23, up to 40 ms | -0.2 | -8.3 |
| LiveKit | lte-bad | 0 of 237 | 26.8 | 17, up to 40 ms | -0.2 | -10.1 |
| AIVC CE | clean | 222 of 222 | exact | 0 | +0.0 | +0.0 |
| AIVC CE | lte | 220 of 220 | exact | 0 | +0.0 | +0.0 |
| AIVC CE | lte-bad | 221 of 221 | exact | 0 | +0.0 | +0.0 |

AI Voice Connector CE delivers the engine's G.711 as it got it: every aligned sample of the
speech in every answer, under every profile (the network only removed packets). LiveKit takes
the engine's 24 kHz audio through its room, over WebRTC (Opus, as its log shows), and back to
8 kHz G.711: the level holds (-0.2 dB), 3.4-4 kHz comes out 8.3 dB lower, as a telephone
band filter leaves it, and what no filter explains is 27.5 dB below the speech. In 6% of
answers on a clean network a piece of speech came 20 or 40 ms later or earlier than the one
before it, each time after the clip's 280 ms of digital silence: LiveKit lengthened or
shortened the pause. Its [mixer](https://github.com/livekit/media-sdk/blob/bc3eace31b2e/mixer/mixer.go)
waits for 3 frames when an input runs dry and discards from a full one, and Opus may stop
sending in silence (`usedtx=1` in LiveKit's SDP); which of these does it was not measured.

The mock sends LiveKit 24 kHz audio interpolated from 8 kHz clips. The comparison is against
that audio through an ideal 8 kHz converter, so the interpolation's own loss near 4 kHz is not
counted against LiveKit; what its images above 4 kHz alias back into the band would be.

## Raw runs

Attached to the [release](../../docs/README.md#published-results) as `.tar.zst`; each unpacks to
the directory `rtpbench` wrote, and each is named by the image that wrote it.

| archive | SHA-256 |
| --- | --- |
| `baseline-reference-direct-ad0a03d9c585.tar.zst` | `8f500ff4514a3c8c308cd36cdbb4356fbfd3c906e46b476b33d1c15f893dbd86` |
| `baseline-reference-carrier-ad0a03d9c585.tar.zst` | `f262eb30cc7f215f79ecc9ba44480f79237c75611d9d715de68fd7cd31e63f0f` |
| `baseline-aivc-direct-ad0a03d9c585.tar.zst` | `17f366dbe602c00c874ad48640668578200c428c2dc9ec4a75e6435f2b817bb5` |
| `baseline-livekit-direct-ad0a03d9c585.tar.zst` | `84458093f9f13a919b080e20452d9e636a97ac5b55556e5efd55231ad6ed1440` |
| `baseline-aivc-carrier-ad0a03d9c585.tar.zst` | `4dfdf3e456fe2c10b71d14589cdb852703b642e43ac7454feca90c8813e31f26` |
| `baseline-livekit-carrier-ad0a03d9c585.tar.zst` | `dd33b15214a7b3cd90a12f3a539cd171e87cce5a59b97b9a4515abf66c300371` |
| `baseline-calibrate-ad0a03d9c585.tar.zst` | `66a8a401c6eae1696b4c421833137b181f3db57dcbff6c1b238538e90800fddd` |
| `baseline-calibrate-carrier-ad0a03d9c585.tar.zst` | `34ea4d0af153af10cdb15bb59aca0f3bdb16179bd0619da25d27728e75790dc1` |
| `baseline-detector-seeds6-10-965085c223d2.tar.zst` | `b2ffa0585eb3c6d29eef4d0287cff53b12d57cc25fcf648c349efee872515640` |
| `baseline-capacity-ba330eecbd02.tar.zst` | `c586a53e25bf0db0674eb4ddf5a887dfbcd620aa62540062ec8f879647c75b52` |

