# Both targets on a mock engine, on bare metal

2026-10-16: the same cases on a bare-metal Linux host, with both targets on the
[mock engine](../../docs/targets.md#mock-engine) instead of a paid AI engine, so every verdict is the connector's and
the engine's share of each turn is known. Senders schedule on the monotonic clock and every run
logs wall-clock steps: 0 were seen across all the runs published here. Summaries, records
and reports are in this folder; captures are not published.

```sh
uv run rtpbench calibrate [--carrier]
uv run --extra vad rtpbench cases [--carrier] --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench target livekit --mock --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench target livekit --mock --carrier --profiles clean,lte,lte-bad --runs 10 \
  --only greeting,bye,cancel,hold,dtmf-rfc4733,dtmf-info,refer,refer-fail,timer,ptime-30,ssrc-change,reinvite,reinvite-nosdp
uv run --extra vad rtpbench target livekit --mock --carrier --profiles clean --runs 10 \
  --only compact-headers,sdp-ssrc,late-offer
# the same for aivc
```

Conditions: 8 cores, 16 threads, kernel 6.8.0-147-generic, CPU governor
`performance`, Docker 29.9.1; python 3.14.8 and
tcpdump 4.99.5 in the containers. Calls placed from a clean checkout at
commit 3ab5fe7 (calibrations at 3ab5fe7). The calibrations ran alone. The cases ran
each profile of each target as its own process, up to 12 at once, a new one starting only while
the load average was under 4.5; while the target stacks ran it reached 10.7 (16
threads), above the range the capacity curve below covers. Engine: the mock, which waits 1000 ms of silence and
answers 500 ms later; AI Voice Connector CE and LiveKit at the versions
in [targets](../../docs/targets.md).

## Timing on this host

Wire timing against the reference agent's truth (max abs error, ms), direct and through the
carrier, 20 turns per profile, and the time the carrier adds per packet:

| profile | turns | wire − truth, direct: max abs | through the carrier: max abs | carrier transit p50 / p95 / max |
| --- | --- | --- | --- | --- |
| clean | 20 | 0.00 | 0.00 | 0.04 / 0.07 / 0.9 |
| delay | 20 | 0.00 | 0.00 | 0.04 / 0.09 / 1.7 |
| jitter | 20 | 0.00 | 0.00 | 0.04 / 0.08 / 1.3 |
| loss | 20 | 0.00 | 0.00 | 0.05 / 0.07 / 0.4 |
| mobile | 20 | 0.00 | 0.00 | 0.04 / 0.07 / 2.9 |
| lte | 20 | 0.00 | 0.00 | 0.04 / 0.08 / 2.0 |
| lte-bad | 20 | 0.00 | 0.12 | 0.05 / 0.10 / 3.2 |

Sender lateness, both ends, direct, 57016 packets: p50 0.009, p99 0.046, max 2.06 ms

How far concurrent stacks can go before timing suffers: N reference stacks at once, 60 turns
each, clean (commit e37a944). Wire against truth; the reference agent's scheduling error; how late each sender's
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

Nothing degrades up to 12 reference stacks. Target stacks weigh more and were not
measured this way; the wire timing of the cases below rests on the calibrations above.

## Cases on the mock engine

Reference: calls with the expected verdict over every behaviour and profile. Targets: verdicts
over the three profiles, 10 repeats each (signalling mutations: clean only). Last column: what a
deterministic engine can judge of the case.

| case | reference, direct | reference, carrier | LiveKit, direct | LiveKit, carrier | AIVC CE, direct | AIVC CE, carrier | a mock judges |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `greeting` | 90/90 | 90/90 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | stack's time, not the model's |
| `bye` | 60/60 | 60/60 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | yes |
| `cancel` | 60/60 | 60/60 | pass 30/30 | pass 30/30 | inconclusive 30/30 | inconclusive 30/30 | yes |
| `hold` | 90/90 | 90/90 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | yes |
| `dtmf-rfc4733` | 60/60 | 60/60 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | digit reaches the engine |
| `dtmf-info` | 60/60 | 60/60 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | digit reaches the engine |
| `refer` | 90/90 | 90/90 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | transfer mechanics |
| `refer-fail` | 90/90 | 90/90 | pass 30/30 | pass 30/30 | **fail** 30/30 | **fail** 30/30 | failure handed back |
| `codec-pcmu` | 60/60 | – | pass 30/30 | – | pass 30/30 | – | yes |
| `codec-pcma` | 60/60 | – | pass 30/30 | – | pass 30/30 | – | yes |
| `timer` | 90/90 | 90/90 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | yes |
| `compact-headers` | – | 60/60 | – | pass 10/10 | – | **fail** 10/10 | yes |
| `sdp-ssrc` | – | 60/60 | – | pass 10/10 | – | **fail** 10/10 | yes |
| `late-offer` | – | 60/60 | – | **fail** 10/10 | – | **fail** 10/10 | yes |
| `ptime-30` | – | 60/60 | – | pass 30/30 | – | pass 30/30 | yes |
| `ssrc-change` | 60/60 | 60/60 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | yes |
| `large-invite` | 60/60 | – | pass 30/30 | – | **fail** 30/30 | – | yes |
| `reinvite` | 60/60 | 60/60 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | yes |
| `reinvite-nosdp` | 60/60 | 60/60 | pass 30/30 | pass 30/30 | **fail** 30/30 | **fail** 30/30 | yes |
| `hold-zero` | 60/60 | – | **fail** 30/30 | – | **fail** 30/30 | – | yes |
| `codec-change` | 60/60 | – | **fail** 30/30 | – | **fail** 30/30 | – | yes |

- The SIP and media cases test the connector alone: the engine only has to hear the caller and
  answer, which the mock always does. Around a model's decision the mock judges only the
  mechanics ([what it cannot stand in for](../../docs/targets.md#mock-engine)).
- No verdict flips between repeats on the mock. Flips on SIP and media cases in the earlier
  results (`bye`, `ssrc-change`, `reinvite` through the carrier) did not recur here; whether they
  came from the engine, the VM's clock steps or its load is not separated.
- `large-invite` (new): an INVITE over 1300 bytes, sent over TCP as RFC 3261 18.1.1 requires.
  LiveKit's SIP bridge listens on TCP and takes it. AI Voice Connector CE's example
  configuration opens a UDP socket only, so the connection is refused and the call goes nowhere
  (the caller's UDP retry is answered); adding a TCP socket to its OpenSIPS configuration makes
  it pass.

## Turn latency, split

Where each target's time goes with the engine held fixed: uplink is from the caller's labelled
end of speech on the wire to when the mock heard it end; engine, the mock's own wait; downlink,
from the mock's first audio to the agent's speech on the wire. ms, p50 [p5, p95]; bar: the
detector's error bar for the profile and codec.

| target | profile | turns | wire latency | uplink | engine | downlink | onset bar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LiveKit | clean | 120 | 1834 [1712, 1893] | 186 [61, 201] | 1501 [1501, 1502] | 148 [135, 193] | −33/+4 |
| LiveKit | lte | 120 | 1984 [1868, 2065] | 290 [182, 354] | 1501 [1501, 1502] | 186 [168, 230] | −32/+3 |
| LiveKit | lte-bad | 120 | 2109 [1941, 2284] | 411 [229, 550] | 1501 [1501, 1502] | 193 [144, 253] | −52/+17 |
| AIVC CE | clean | 120 | 1511 [1504, 1517] | 0 [-2, 4] | 1501 [1501, 1501] | 9 [2, 16] | −24/+88 |
| AIVC CE | lte | 120 | 1593 [1581, 1608] | 41 [35, 48] | 1501 [1500, 1502] | 51 [40, 63] | −25/+88 |
| AIVC CE | lte-bad | 120 | 1604 [1546, 1666] | 47 [12, 85] | 1501 [1500, 1502] | 57 [18, 107] | −35/+97 |

Greeting: from the 200 OK to the agent's first speech, split the same way (the request is when
the target asked the engine to speak, against its 200 OK):

| target | profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- | --- |
| LiveKit | clean | 10 | 687 [661, 697] | -8 [-35, -5] | 501 [501, 502] | 196 [191, 206] |
| LiveKit | lte | 10 | 719 [695, 740] | -17 [-46, -5] | 501 [501, 502] | 233 [224, 258] |
| LiveKit | lte-bad | 10 | 719 [676, 799] | -15 [-54, -7] | 501 [501, 502] | 235 [200, 305] |
| AIVC CE | clean | 10 | 541 [541, 542] | 3 [2, 4] | 501 [501, 501] | 38 [36, 38] |
| AIVC CE | lte | 10 | 581 [571, 584] | 2 [2, 4] | 501 [501, 501] | 78 [67, 81] |
| AIVC CE | lte-bad | 10 | 580 [558, 629] | 3 [2, 7] | 501 [501, 503] | 75 [54, 125] |

Barge-in: the mock cancels its answer on the first voiced 10 ms of the caller, so what is left is
the target's own path. Stopped within 2 s, and the stop time p50 (ms):

| target | profile | interruptions stopped | backchannels stopped | coughs stopped | stop bar |
| --- | --- | --- | --- | --- | --- |
| LiveKit | clean | 51/51, p50 298 | 25/25, p50 245 | 24/24, p50 238 | +0/+79 |
| LiveKit | lte | 51/51, p50 476 | 25/25, p50 428 | 24/24, p50 437 | +0/+71 |
| LiveKit | lte-bad | 51/51, p50 641 | 25/25, p50 543 | 24/24, p50 587 | −5/+94 |
| AIVC CE | clean | 51/51, p50 24 | 25/25, p50 21 | 24/24, p50 6 | +0/+72 |
| AIVC CE | lte | 51/51, p50 102 | 25/25, p50 96 | 24/24, p50 79 | +0/+72 |
| AIVC CE | lte-bad | 51/51, p50 132 | 25/25, p50 64 | 24/24, p50 88 | +0/+119 |

So, with the engine held fixed, LiveKit's media path adds 325 ms to a turn at the median on
clean (its uplink and downlink against AI Voice Connector CE's). On the real engine it answered
0.4-0.5 s later ([on a real engine](../two-targets)); the rest of that is how
each drives the engine (24 kHz PCM against G.711 passed through, and the engine's own speech
detection settings).

## A correction to the earlier carrier results

Until the carrier waited for its media relay to start (#54), the calls in the first minute of a
run could go around the relay: media straight between caller and agent while the signalling went
through the carrier. In a first run of this wave the first five calls of some runs did. The
earlier results' captures are not published, so which of their calls did cannot be said.
Everything here ran after the fix.
