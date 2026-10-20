
Error bars: true value = measured - error, error within


Wall-clock steps during the run: none.

## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | across a clock step | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 10 | 120/120 | 1710 | 1833 | 1892 | 1822 .. 1837 | 0 | [-3.2, +44.6] webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5) |
| lte | 10 | 120/120 | 1879 | 1984 | 2065 | 1947 .. 2002 | 0 | [-3.6, +43.3] webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5) |
| lte-bad | 10 | 120/120 | 1956 | 2135 | 2309 | 2089 .. 2198 | 0 | [-15.5, +60.9] webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5) |

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts).

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | across a clock step | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 51/51 | 100% .. 100% | -12 | 296 | 454 | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| clean | backchannel | 10 | 25/25 | 100% .. 100% | 0 | 285 | 383 | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| clean | cough | 10 | 24/24 | 100% .. 100% | -90 | 228 | 435 | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| lte | interrupt | 10 | 51/51 | 100% .. 100% | 32 | 457 | 648 | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte | backchannel | 10 | 25/25 | 100% .. 100% | 229 | 424 | 575 | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte | cough | 10 | 24/24 | 100% .. 100% | 104 | 403 | 627 | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte-bad | interrupt | 10 | 51/51 | 100% .. 100% | 184 | 624 | 818 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | backchannel | 10 | 25/25 | 100% .. 100% | 420 | 551 | 753 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | cough | 10 | 24/24 | 100% .. 100% | 170 | 561 | 742 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |

## Turn latency by part

Turn latency on the mock engine, split where it heard the end of the caller's speech and sent its first audio (one clock with the captures), ms, p50 [p5, p95]: uplink and downlink are the target's; the engine waits 1000 ms of silence and answers 500 ms later by design. Uplink carries the caller's label error (±17 ms), downlink the onset error bar of the profile and codec.

| profile | turns | wire latency | uplink | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 120 | 1833 [1710, 1892] | 190 [63, 205] | 1501 [1501, 1502] | 143 [130, 190] |
| lte | 120 | 1984 [1879, 2065] | 294 [185, 350] | 1501 [1501, 1502] | 187 [167, 236] |
| lte-bad | 120 | 2135 [1956, 2309] | 439 [253, 612] | 1501 [1501, 1502] | 193 [153, 251] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 20 | 21.0 [20.6, 21.5] | 0.13 [0.08, 0.36] |
| lte | 20 | 34.8 [32.7, 37.4] | 3.36 [3.32, 3.46] |
| lte-bad | 20 | 126.7 [123.7, 128.5] | 20.44 [20.23, 20.73] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.

## Engine audio as the caller received it

The mock engine's answers as the caller received them (completed answers in the latency and barge-in calls), median [min, max] over answers. Each piece of speech is aligned with what the mock sent; for 24 kHz audio, that is its interpolation through an ideal 8 kHz converter, so the mock's own resampling is not counted. Samples in packets the network lost are left out. unchanged: answers whose aligned speech came through sample for sample (pauses are not compared). distortion: the audio against what no linear filter of ±4 ms explains; a resampler or band filter would leave G.711's own, about 37 dB. moved: answers where a piece came out 5 ms or more later or earlier than the one before (a pause lengthened or shortened, audio inserted or dropped), and the largest move. gain: least squares. 3.4-4 kHz: that band against 300-3400 Hz, relative to what was sent.

| profile | answers | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB |
| --- | --- | --- | --- | --- | --- | --- |
| clean | 240 | 0 | 27.4 [13.7, 29.8] | 24, up to 40 ms | -0.2 [-0.5, -0.0] | -8.3 [-10.0, -7.5] |
| lte | 240 | 0 | 27.3 [8.8, 30.1] | 23, up to 60 ms | -0.2 [-0.7, -0.0] | -8.3 [-11.4, -7.3] |
| lte-bad | 236 | 0 | 27.1 [21.0, 30.2] | 18, up to 40 ms | -0.2 [-0.7, -0.0] | -10.0 [-14.9, +6.6] |

## Caller audio as the engine received it

The caller's lines in the latency and barge-in calls as the mock engine received them, aligned piece by piece with what the caller sent (its own capture, before the network), median [min, max] over lines; the columns as for the engine's audio above. Lost packets are the target's to fill: what it filled them with counts as distortion, and what it left out as moved. above 4 kHz: energy above 4 kHz against 300-3400 Hz in 24 kHz audio (the caller sends none). full scale: lines with samples at full scale. missing 20 ms: the caller's voiced 20 ms with nothing like them within 25 ms in what the engine got, and what came in their place: silence, the 20 ms before again (repeat), or other (also the next audio, where a packet was left out: see moved). appends: the audio each append carried, the median of each call's.

| profile | lines | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB | above 4 kHz, dB | full scale | missing 20 ms | appends, ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 320 | 0 | 28.3 [17.3, 31.1] | 0 | +1.9 [-0.4, +11.7] | -16.6 [-22.9, -9.9] | -60.7 [-62.6, -50.3] | 20, up to 7 samples | 0.4%: 63 other | 100 [100, 100] |
| lte | 309 | 0 | 19.1 [-1.5, 31.2] | 132, up to 60 ms | +1.6 [-2.7, +11.7] | -16.6 [-22.1, -10.3] | -60.7 [-62.7, -49.9] | 17, up to 7 samples | 0.9%: 9 silence, 4 repeat, 131 other | 100 [100, 100] |
| lte-bad | 236 | 0 | 3.9 [-2.0, 30.4] | 174, up to 60 ms | -0.3 [-4.0, +10.8] | -16.7 [-24.6, -9.4] | -60.8 [-62.8, -50.0] | 8, up to 9 samples | 3.8%: 64 silence, 1 repeat, 333 other | 100 [100, 100] |
