
Error bars: true value = measured - error, error within


Wall-clock steps during the run: none.

## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | across a clock step | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 10 | 120/120 | 1504 | 1512 | 1517 | 1510 .. 1513 | 0 | [-133.0, +11.0] webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech, seeds 1-5) |
| lte | 10 | 120/120 | 1582 | 1594 | 1609 | 1590 .. 1596 | 0 | [-131.0, +14.1] webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech, seeds 1-5) |
| lte-bad | 10 | 120/120 | 1551 | 1605 | 1669 | 1583 .. 1624 | 0 | [-141.5, +22.9] webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech, seeds 1-5) |

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts). Speech ended before (gate): turns left out, the gate having heard the agent's speech end before the onset by more than the bar.

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | across a clock step | speech ended before (gate) | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 47/47 | 100% .. 100% | -14 | 37 | 179 | 0 | 4 | [-84.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in, seeds 1-5) |
| clean | backchannel | 10 | 21/21 | 100% .. 100% | -13 | 22 | 130 | 0 | 4 | [-84.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in, seeds 1-5) |
| clean | cough | 10 | 18/18 | 100% .. 100% | -76 | 19 | 167 | 0 | 6 | [-84.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in, seeds 1-5) |
| lte | interrupt | 10 | 48/48 | 100% .. 100% | -26 | 105 | 254 | 0 | 3 | [-77.6, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in, seeds 1-5) |
| lte | backchannel | 10 | 22/22 | 100% .. 100% | -16 | 96 | 208 | 0 | 3 | [-77.6, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in, seeds 1-5) |
| lte | cough | 10 | 20/20 | 100% .. 100% | -48 | 82 | 241 | 0 | 4 | [-77.6, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in, seeds 1-5) |
| lte-bad | interrupt | 10 | 48/48 | 100% .. 100% | -11 | 155 | 295 | 0 | 3 | [-100.7, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | backchannel | 10 | 22/22 | 100% .. 100% | -28 | 99 | 212 | 0 | 3 | [-100.7, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | cough | 10 | 22/22 | 100% .. 100% | -9 | 103 | 250 | 0 | 2 | [-100.7, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in, seeds 1-5) |

Per clip: stopped / turns, over the same turns, and those left out as ended before; interruptions are the caller's lines (--lines), backchannels and coughs the corpus's.

| interjection | clip | words | clean | lte | lte-bad |
| --- | --- | --- | --- | --- | --- |
| interrupt | interrupt-00 |  | 17/17 | 17/17 | 17/17 |
| interrupt | interrupt-01 |  | 12/12, 2 ended before | 13/13, 1 ended before | 13/13, 1 ended before |
| interrupt | interrupt-02 |  | 11/11, 1 ended before | 11/11, 1 ended before | 11/11, 1 ended before |
| interrupt | interrupt-03 |  | 7/7, 1 ended before | 7/7, 1 ended before | 7/7, 1 ended before |
| backchannel | tts-ald-bc | Ajá | 1/1, 1 ended before | 1/1, 1 ended before | 1/1, 1 ended before |
| backchannel | tts-cori-bc | Yeah | 1/1, 2 ended before | 2/2, 1 ended before | 2/2, 1 ended before |
| backchannel | tts-davefx-bc | Vale | 1/1 | 1/1 | 1/1 |
| backchannel | tts-libritts0-bc | Okay | 3/3, 1 ended before | 3/3, 1 ended before | 3/3, 1 ended before |
| backchannel | tts-libritts3-bc | Uh-huh | 1/1 | 1/1 | 1/1 |
| backchannel | tts-ljspeech-bc | Uh-huh | 6/6 | 6/6 | 6/6 |
| backchannel | tts-sharvardf-bc | Vale | 5/5 | 5/5 | 5/5 |
| backchannel | tts-sharvardm-bc | Sí, sí | 3/3 | 3/3 | 3/3 |
| cough | cough-c1-1 |  | 3/3 | 3/3 | 3/3 |
| cough | cough-c2-0 |  | 2/2, 1 ended before | 3/3 | 3/3 |
| cough | cough-c2-1 |  | 1/1, 1 ended before | 2/2 | 2/2 |
| cough | cough-man-0 |  | 2/2, 1 ended before | 2/2, 1 ended before | 3/3 |
| cough | cough-man-1 |  | 2/2, 1 ended before | 2/2, 1 ended before | 3/3 |
| cough | cough-short-0 |  | 4/4, 2 ended before | 4/4, 2 ended before | 4/4, 2 ended before |
| cough | cough-short-1 |  | 2/2 | 2/2 | 2/2 |
| cough | cough-woman_three_times-0 |  | 2/2 | 2/2 | 2/2 |

## Turn latency by part

Turn latency on the mock engine, split where it heard the end of the caller's speech and sent its first audio (one clock with the captures), ms, p50 [p5, p95]: uplink and downlink are the target's; the engine waits 1000 ms of silence and answers 500 ms later by design. Uplink carries the caller's label error (±17 ms), downlink the onset error bar of the profile and codec.

| profile | turns | wire latency | uplink | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 120 | 1512 [1504, 1517] | 0 [-2, 4] | 1501 [1500, 1501] | 9 [2, 16] |
| lte | 120 | 1594 [1582, 1609] | 40 [35, 46] | 1501 [1500, 1502] | 52 [41, 62] |
| lte-bad | 120 | 1605 [1551, 1669] | 47 [5, 89] | 1501 [1500, 1502] | 61 [25, 97] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 20 | 1.1 [0.6, 2.1] | 0.10 [0.05, 0.38] |
| lte | 20 | 18.5 [17.0, 19.4] | 3.38 [3.32, 3.41] |
| lte-bad | 20 | 107.6 [104.6, 110.2] | 20.37 [19.99, 20.78] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.

## Engine audio as the caller received it

The mock engine's answers as the caller received them (completed answers in the latency and barge-in calls), median [min, max] over answers. Each piece of speech is aligned with what the mock sent; for 24 kHz audio, that is its interpolation through an ideal 8 kHz converter, so the mock's own resampling is not counted. Samples in packets the network lost are left out. unchanged: answers whose aligned speech came through sample for sample (pauses are not compared). distortion: the audio against what no linear filter of ±4 ms explains; a resampler or band filter would leave G.711's own, about 37 dB. moved: answers where a piece came out 5 ms or more later or earlier than the one before (a pause lengthened or shortened, audio inserted or dropped), and the largest move. gain: least squares. 3.4-4 kHz: that band against 300-3400 Hz, relative to what was sent.

| profile | answers | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB |
| --- | --- | --- | --- | --- | --- | --- |
| clean | 227 | 227 | exact [exact, exact] | 0 | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| lte | 220 | 220 | exact [exact, exact] | 0 | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| lte-bad | 220 | 220 | exact [exact, exact] | 0 | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |

## Caller audio as the engine received it

The caller's lines in the latency and barge-in calls as the mock engine received them, aligned piece by piece with what the caller sent (its own capture, before the network), median [min, max] over lines; the columns as for the engine's audio above. Lost packets are the target's to fill: what it filled them with counts as distortion, and what it left out as moved. above 4 kHz: energy above 4 kHz against 300-3400 Hz in 24 kHz audio (the caller sends none). full scale: lines with samples at full scale. missing 20 ms: the caller's voiced 20 ms with nothing like them within 25 ms in what the engine got, and what came in their place: silence, the 20 ms before again (repeat), or other (also the next audio, where a packet was left out: see moved). appends: the audio each append carried, the median of each call's.

| profile | lines | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB | above 4 kHz, dB | full scale | missing 20 ms | appends, ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 320 | 320 | exact [exact, exact] | 0 | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |  | 0 | 0.0% | 20 [20, 20] |
| lte | 317 | 233 | exact [-2.0, exact] | 88, up to 60 ms | +0.0 [-6.3, +0.0] | +0.0 [-0.7, +1.3] |  | 0 | 0.6%: 5 silence, 91 other | 20 [20, 20] |
| lte-bad | 255 | 71 | 12.0 [-2.3, exact] | 154, up to 60 ms | -0.5 [-6.0, +0.0] | +0.0 [-4.6, +5.7] |  | 0 | 3.0%: 52 silence, 302 other | 20 [20, 20] |
