### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 691.0 [686.5, 789.7] ms (-63.6/-1.0) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.4 [0.3, 1.0] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: -14.9 [-30.5, -6.8] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 5 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 0.9 [0.7, 2.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.8 [0.7, 2.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.0 [0.7, 1.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 5888.4 [5875.0, 5916.6] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.8, 1.2] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 5899.8 [5878.3, 5922.6] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 2 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 0.9 [0.8, 1.2] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13265.7 [13232.9, 13293.7] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1542.0 [1540.6, 1544.6] ms (-44.6/+3.2) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1541.3 [1539.8, 1546.4] ms (-44.6/+3.2) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 1.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1542.1 [1540.6, 1545.8] ms (-44.6/+3.2) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.6 [0.5, 0.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1542.5 [1540.7, 1545.8] ms (-44.6/+3.2) n=10 | - |
| hold-zero | inconclusive 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.8 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10 | resume from c=0.0.0.0: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| codec-change | pass 10/10 | end of the question to agent speech: 1543.8 [1541.3, 1547.9] ms (-64.9/-1.1) n=10 | - |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 725.0 [717.3, 761.7] ms (-67.6/+0.8) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 26.9 [13.5, 39.0] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 4 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 0.8 [0.7, 1.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.8 [0.7, 2.2] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.8 [0.7, 1.4] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 5930.5 [5912.7, 5957.5] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.7, 1.1] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 5932.5 [5915.1, 5945.4] ms (-17.0/+17.0) n=9 | agent transfers (REFER) (1/10); agent keeps the call for 10 s (9/10: BYE 1 ms after it); agent speaks within 5000 ms (9/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 0.9 [0.7, 1.1] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13248.1 [13223.6, 13269.0] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1621.7 [1609.7, 1624.1] ms (-43.3/+3.6) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1620.3 [1616.6, 1634.1] ms (-43.3/+3.6) n=10 | - |
| reinvite | flips: pass 9, fail 1 | refresh re-INVITE to 2xx: 0.8 [0.7, 1.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1626.4 [1615.9, 1629.9] ms (-43.3/+3.6) n=9 | media undisturbed by the refresh (1/10: agent RTP stops 0 ms after the 2xx); agent replies within 10000 ms (1/10) |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.5 [0.4, 1.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1622.8 [1614.8, 1632.3] ms (-43.3/+3.6) n=10 | - |
| hold-zero | inconclusive 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.9 [0.7, 1.3] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.6, 1.3] ms (-0.4/+0.4) n=10 | resume from c=0.0.0.0: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| codec-change | pass 10/10 | end of the question to agent speech: 1622.4 [1603.1, 1629.3] ms (-67.7/+2.5) n=10 | - |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 718.8 [685.2, 745.1] ms (-109.8/+11.4) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.3 [0.3, 0.9] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 48.6 [-17.8, 71.6] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 4 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.8 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 5962.1 [5903.8, 6027.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.8, 1.0] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 5966.9 [5908.1, 6030.3] ms (-17.0/+17.0) n=9 | agent transfers (REFER) (1/10); agent keeps the call for 10 s (9/10: BYE 1 ms after it); agent speaks within 5000 ms (9/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13261.5 [13213.1, 13304.2] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1615.1 [1579.0, 1687.1] ms (-60.9/+15.5) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1612.3 [1586.0, 1657.6] ms (-60.9/+15.5) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.7 [0.6, 1.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1638.8 [1568.8, 1670.5] ms (-60.9/+15.5) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.5 [0.5, 0.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1660.0 [1614.3, 1723.5] ms (-60.9/+15.5) n=10 | - |
| hold-zero | inconclusive 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.8 [0.8, 1.1] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.6, 0.9] ms (-0.4/+0.4) n=10 | resume from c=0.0.0.0: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| codec-change | pass 10/10 | end of the question to agent speech: 1613.2 [328.5, 1712.8] ms (-102.9/+13.1) n=10 | - |


Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-15.5, +60.9] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5)
- [-13.1, +102.9] ms: webrtcvad first onset, p5..p95, PCMA, lte-bad (calibrate --speech, seeds 1-5)
- [-11.4, +109.8] ms: webrtcvad first onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5)
- [-3.6, +43.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5)
- [-3.2, +44.6] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5)
- [-2.5, +67.7] ms: webrtcvad first onset, p5..p95, PCMA, lte (calibrate --speech, seeds 1-5)
- [-0.8, +67.6] ms: webrtcvad first onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
- [+1.0, +63.6] ms: webrtcvad first onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5)
- [+1.1, +64.9] ms: webrtcvad first onset, p5..p95, PCMA, clean (calibrate --speech, seeds 1-5)

Wall-clock steps during the run: none.

## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | across a clock step | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 10 | 120/120 | 1469 | 1588 | 1594 | 1587 .. 1589 | 0 | [-3.2, +44.6] webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5) |
| lte | 10 | 120/120 | 1546 | 1663 | 1679 | 1657 .. 1668 | 0 | [-3.6, +43.3] webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5) |
| lte-bad | 10 | 120/120 | 1501 | 1650 | 1713 | 1633 .. 1669 | 0 | [-15.5, +60.9] webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5) |

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts).

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | across a clock step | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 0/51 | 0% .. 0% | - | - | - | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| clean | backchannel | 10 | 0/25 | 0% .. 0% | - | - | - | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| clean | cough | 10 | 0/24 | 0% .. 0% | - | - | - | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| lte | interrupt | 10 | 0/51 | 0% .. 0% | - | - | - | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte | backchannel | 10 | 0/25 | 0% .. 0% | - | - | - | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte | cough | 10 | 0/24 | 0% .. 0% | - | - | - | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte-bad | interrupt | 10 | 0/51 | 0% .. 0% | - | - | - | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | backchannel | 10 | 0/25 | 0% .. 0% | - | - | - | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | cough | 10 | 0/24 | 0% .. 0% | - | - | - | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |

## Turn latency by part

Turn latency on the mock engine, split where it heard the end of the caller's speech and sent its first audio (one clock with the captures), ms, p50 [p5, p95]: uplink and downlink are the target's; the engine waits 1000 ms of silence and answers 500 ms later by design. Uplink carries the caller's label error (±17 ms), downlink the onset error bar of the profile and codec.

| profile | turns | wire latency | uplink | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 120 | 1588 [1469, 1594] | 1 [-111, 5] | 1501 [1500, 1502] | 87 [77, 92] |
| lte | 120 | 1663 [1546, 1679] | 40 [-72, 48] | 1501 [1501, 1502] | 122 [100, 133] |
| lte-bad | 120 | 1650 [1501, 1713] | 41 [-87, 77] | 1501 [1500, 1502] | 106 [58, 152] |

Greeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the target's request for a greeting (negative: asked before answering), the engine's 500 ms, and from its first audio to the agent's speech on the wire (webrtcvad onset bar).

| profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 10 | 690 [687, 790] | 150 [142, 196] | 501 [501, 502] | 40 [39, 123] |
| lte | 10 | 725 [717, 762] | 142 [137, 149] | 501 [500, 502] | 82 [76, 115] |
| lte-bad | 10 | 718 [685, 745] | 140 [137, 145] | 501 [501, 502] | 75 [40, 103] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 176 | 200.3 [40.8, 739.8] | 1.38 [0.82, 2.04] |
| lte | 177 | 188.7 [48.5, 686.0] | 4.09 [2.38, 4.92] |
| lte-bad | 174 | 246.6 [92.4, 711.0] | 19.55 [12.59, 22.34] |

Pauses: where the agent stopped sending RTP for a second or more and went on with the same stream, outside a hold (silence suppression, RFC 3551 4.1), median [min, max]: per call; how far the RTP clock fell behind across each, ms (the pause less what the timestamps advanced: 0 if they kept time, as RFC 3550 5.1 requires); and how many packets after one carry the marker bit, as 4.1 asks. A carrier that hangs up on RTP inactivity may hang up on these.

| profile | calls | pauses | clock behind | marker |
| --- | --- | --- | --- | --- |
| clean | 170 | 1 [0, 12] | 0 [0, 1] | 310/310 |
| lte | 170 | 1 [0, 12] | 1 [-14, 16] | 307/309 |
| lte-bad | 170 | 1 [0, 12] | -9 [-97, 102] | 298/310 |

## Engine audio as the caller received it

The mock engine's answers as the caller received them (completed answers in the latency and barge-in calls), median [min, max] over answers. Each piece of speech is aligned with what the mock sent; for 24 kHz audio, that is its interpolation through an ideal 8 kHz converter, so the mock's own resampling is not counted. Samples in packets the network lost are left out. unchanged: answers whose aligned speech came through sample for sample (pauses are not compared). distortion: the audio against what no linear filter of ±4 ms explains; a resampler or band filter would leave G.711's own, about 37 dB. moved: answers where a piece came out 5 ms or more later or earlier than the one before (a pause lengthened or shortened, audio inserted or dropped), and the largest move. gain: least squares. 3.4-4 kHz: that band against 300-3400 Hz, relative to what was sent.

| profile | answers | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB |
| --- | --- | --- | --- | --- | --- | --- |
| clean | 200 | 0 | 25.6 [25.6, 29.4] | 0 | -0.2 [-0.2, -0.2] | -1.2 [-2.3, -1.2] |
| lte | 199 | 0 | 25.6 [20.1, 36.0] | 2, up to 5 ms | -0.2 [-0.2, -0.2] | -2.1 [-2.6, -1.0] |
| lte-bad | 190 | 0 | 35.3 [18.5, 36.5] | 11, up to 48 ms | -0.2 [-0.2, -0.2] | -2.3 [-2.9, +8.0] |

## Caller audio as the engine received it

The caller's lines in the latency and barge-in calls as the mock engine received them, aligned piece by piece with what the caller sent (its own capture, before the network), median [min, max] over lines; the columns as for the engine's audio above. Lost packets are the target's to fill: what it filled them with counts as distortion, and what it left out as moved. above 4 kHz: energy above 4 kHz against 300-3400 Hz in 24 kHz audio (the caller sends none). full scale: lines with samples at full scale. missing 20 ms: the caller's voiced 20 ms with nothing like them within 25 ms in what the engine got, and what came in their place: silence, the 20 ms before again (repeat), or other (also the next audio, where a packet was left out: see moved). appends: the audio each append carried, the median of each call's.

| profile | lines | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB | above 4 kHz, dB | full scale | missing 20 ms | appends, ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 220 | 0 | 24.9 [15.9, 42.1] | 0 | -0.5 [-0.6, -0.3] | -5.6 [-5.9, -5.2] | -25.2 [-31.0, -22.1] | 0 | 0.1%: 20 silence | 20 [20, 20] |
| lte | 219 | 0 | 22.0 [0.8, 42.1] | 68, up to 60 ms | -0.5 [-4.0, -0.3] | -5.6 [-6.5, -3.3] | -25.2 [-31.1, -22.0] | 0 | 0.6%: 23 silence, 62 other | 20 [20, 20] |
| lte-bad | 177 | 0 | 9.8 [-2.7, 41.8] | 122, up to 60 ms | -1.3 [-6.1, -0.3] | -5.5 [-7.0, -4.0] | -25.4 [-31.1, -21.8] | 0 | 2.9%: 62 silence, 214 other | 20 [20, 20] |
