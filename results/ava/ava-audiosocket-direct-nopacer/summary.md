
Error bars: true value = measured - error, error within


Wall-clock steps during the run: none.

## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | across a clock step | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 10 | 120/120 | 1444 | 1572 | 1582 | 1570 .. 1573 | 0 | [-3.2, +44.6] webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5) |
| lte | 10 | 120/120 | 1525 | 1650 | 1666 | 1644 .. 1653 | 0 | [-3.6, +43.3] webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5) |
| lte-bad | 10 | 119/120 | 1498 | 1643 | 1726 | 1599 .. 1658 | 0 | [-15.5, +60.9] webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5) |

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts). Speech ended before (gate): turns left out, the gate having heard the agent's speech end before the onset by more than the bar.

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | across a clock step | speech ended before (gate) | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 0/51 | 0% .. 0% | - | - | - | 0 | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| clean | backchannel | 10 | 0/25 | 0% .. 0% | - | - | - | 0 | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| clean | cough | 10 | 0/24 | 0% .. 0% | - | - | - | 0 | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| lte | interrupt | 10 | 0/51 | 0% .. 0% | - | - | - | 0 | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte | backchannel | 10 | 0/25 | 0% .. 0% | - | - | - | 0 | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte | cough | 10 | 0/24 | 0% .. 0% | - | - | - | 0 | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte-bad | interrupt | 10 | 0/51 | 0% .. 0% | - | - | - | 0 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | backchannel | 10 | 0/25 | 0% .. 0% | - | - | - | 0 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | cough | 10 | 0/24 | 0% .. 0% | - | - | - | 0 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |

Per clip: stopped / turns, over the same turns, and those left out as ended before; interruptions are the caller's lines (--lines), backchannels and coughs the corpus's.

| interjection | clip | words | clean | lte | lte-bad |
| --- | --- | --- | --- | --- | --- |
| interrupt | interrupt-00 |  | 0/17 | 0/17 | 0/17 |
| interrupt | interrupt-01 |  | 0/14 | 0/14 | 0/14 |
| interrupt | interrupt-02 |  | 0/12 | 0/12 | 0/12 |
| interrupt | interrupt-03 |  | 0/8 | 0/8 | 0/8 |
| backchannel | tts-ald-bc | Ajá | 0/2 | 0/2 | 0/2 |
| backchannel | tts-cori-bc | Yeah | 0/3 | 0/3 | 0/3 |
| backchannel | tts-davefx-bc | Vale | 0/1 | 0/1 | 0/1 |
| backchannel | tts-libritts0-bc | Okay | 0/4 | 0/4 | 0/4 |
| backchannel | tts-libritts3-bc | Uh-huh | 0/1 | 0/1 | 0/1 |
| backchannel | tts-ljspeech-bc | Uh-huh | 0/6 | 0/6 | 0/6 |
| backchannel | tts-sharvardf-bc | Vale | 0/5 | 0/5 | 0/5 |
| backchannel | tts-sharvardm-bc | Sí, sí | 0/3 | 0/3 | 0/3 |
| cough | cough-c1-1 |  | 0/3 | 0/3 | 0/3 |
| cough | cough-c2-0 |  | 0/3 | 0/3 | 0/3 |
| cough | cough-c2-1 |  | 0/2 | 0/2 | 0/2 |
| cough | cough-man-0 |  | 0/3 | 0/3 | 0/3 |
| cough | cough-man-1 |  | 0/3 | 0/3 | 0/3 |
| cough | cough-short-0 |  | 0/6 | 0/6 | 0/6 |
| cough | cough-short-1 |  | 0/2 | 0/2 | 0/2 |
| cough | cough-woman_three_times-0 |  | 0/2 | 0/2 | 0/2 |

## Turn latency by part

Turn latency on the mock engine, split where it heard the end of the caller's speech and sent its first audio (one clock with the captures), ms, p50 [p5, p95]: uplink and downlink are the target's; the engine waits 1000 ms of silence and answers 500 ms later by design. Uplink carries the caller's label error (±17 ms), downlink the onset error bar of the profile and codec.

| profile | turns | wire latency | uplink | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 120 | 1572 [1444, 1582] | 1 [-112, 5] | 1501 [1500, 1502] | 71 [37, 79] |
| lte | 120 | 1650 [1525, 1666] | 40 [-73, 48] | 1501 [1500, 1502] | 109 [77, 121] |
| lte-bad | 119 | 1643 [1498, 1726] | 40 [-82, 92] | 1501 [1500, 1502] | 103 [44, 156] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 20 | 2.7 [1.9, 33.4] | 0.30 [0.26, 0.35] |
| lte | 20 | 16.1 [14.2, 60.9] | 3.32 [3.14, 3.42] |
| lte-bad | 20 | 106.2 [101.0, 111.3] | 19.97 [18.96, 20.62] |

Pauses: where the agent stopped sending RTP for a second or more and went on with the same stream, outside a hold (silence suppression, RFC 3551 4.1), median [min, max]: per call; how far the RTP clock fell behind across each, ms (the pause less what the timestamps advanced: 0 if they kept time, as RFC 3550 5.1 requires); and how many packets after one carry the marker bit, as 4.1 asks. A carrier that hangs up on RTP inactivity may hang up on these.

| profile | calls | pauses | clock behind | marker |
| --- | --- | --- | --- | --- |
| clean | 20 | 11 [10, 12] | 0 [0, 1] | 220/220 |
| lte | 20 | 11 [10, 12] | 0 [-15, 7] | 218/220 |
| lte-bad | 20 | 10 [10, 12] | -2 [-89, 102] | 204/219 |

## Engine audio as the caller received it

The mock engine's answers as the caller received them (completed answers in the latency and barge-in calls), median [min, max] over answers. Each piece of speech is aligned with what the mock sent; for 24 kHz audio, that is its interpolation through an ideal 8 kHz converter, so the mock's own resampling is not counted. Samples in packets the network lost are left out. unchanged: answers whose aligned speech came through sample for sample (pauses are not compared). distortion: the audio against what no linear filter of ±4 ms explains; a resampler or band filter would leave G.711's own, about 37 dB. moved: answers where a piece came out 5 ms or more later or earlier than the one before (a pause lengthened or shortened, audio inserted or dropped), and the largest move. gain: least squares. 3.4-4 kHz: that band against 300-3400 Hz, relative to what was sent.

| profile | answers | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB |
| --- | --- | --- | --- | --- | --- | --- |
| clean | 200 | 0 | 25.8 [25.8, 29.6] | 0 | -0.2 [-0.2, -0.2] | -1.2 [-2.3, -1.2] |
| lte | 198 | 0 | 25.8 [21.2, 36.0] | 1, up to 5 ms | -0.2 [-0.2, -0.2] | -2.0 [-2.6, -0.9] |
| lte-bad | 190 | 0 | 35.3 [18.5, 36.9] | 13, up to 59 ms | -0.2 [-0.3, -0.2] | -2.2 [-2.9, +10.1] |

## Caller audio as the engine received it

The caller's lines in the latency and barge-in calls as the mock engine received them, aligned piece by piece with what the caller sent (its own capture, before the network), median [min, max] over lines; the columns as for the engine's audio above. Lost packets are the target's to fill: what it filled them with counts as distortion, and what it left out as moved. above 4 kHz: energy above 4 kHz against 300-3400 Hz in 24 kHz audio (the caller sends none). full scale: lines with samples at full scale. missing 20 ms: the caller's voiced 20 ms with nothing like them within 25 ms in what the engine got, and what came in their place: silence, the 20 ms before again (repeat), or other (also the next audio, where a packet was left out: see moved). appends: the audio each append carried, the median of each call's.

| profile | lines | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB | above 4 kHz, dB | full scale | missing 20 ms | appends, ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 220 | 0 | 24.9 [15.9, 42.1] | 0 | -0.5 [-0.6, -0.3] | -5.6 [-5.9, -5.2] | -25.2 [-31.0, -22.1] | 0 | 0.1%: 20 silence | 20 [20, 20] |
| lte | 214 | 0 | 22.0 [-0.5, 42.7] | 66, up to 60 ms | -0.5 [-4.3, -0.3] | -5.6 [-6.0, -4.0] | -25.3 [-31.0, -22.1] | 0 | 0.5%: 27 silence, 45 other | 20 [20, 20] |
| lte-bad | 162 | 0 | 9.9 [-2.2, 41.8] | 115, up to 60 ms | -1.2 [-7.5, -0.3] | -5.5 [-10.0, +1.2] | -25.2 [-31.1, -21.5] | 0 | 3.2%: 67 silence, 212 other | 20 [20, 20] |
