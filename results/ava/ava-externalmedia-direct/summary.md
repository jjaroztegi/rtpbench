### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 694.1 [689.5, 816.2] ms (-63.6/-1.0) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.4 [0.3, 0.7] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: -11.4 [-31.4, -1.0] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 5 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 0.9 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.9 [0.7, 1.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.9 [0.8, 1.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.8 [0.7, 1.1] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 6005.8 [5986.5, 6008.1] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.8, 1.8] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 5990.4 [5985.8, 6017.2] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 0.9 [0.8, 1.8] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13739.8 [13718.1, 13762.5] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1542.1 [1540.5, 1545.2] ms (-44.6/+3.2) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1542.5 [1540.8, 1545.7] ms (-44.6/+3.2) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 1.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1543.0 [1541.3, 1547.3] ms (-44.6/+3.2) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.5 [0.5, 0.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1542.3 [1540.9, 1545.4] ms (-44.6/+3.2) n=10 | - |
| hold-zero | inconclusive 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.9 [0.8, 1.1] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.7, 1.1] ms (-0.4/+0.4) n=10 | resume from c=0.0.0.0: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| codec-change | pass 10/10 | end of the question to agent speech: 1527.3 [1526.2, 1533.7] ms (-64.9/-1.1) n=10 | - |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 727.2 [722.9, 732.9] ms (-67.6/+0.8) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 24.2 [0.4, 32.7] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 4 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 0.9 [0.8, 1.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.8 [0.7, 1.2] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.8 [0.8, 1.1] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.4 [0.4, 0.5] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 6045.8 [6024.0, 6064.6] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.7, 3.0] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 6055.1 [6029.7, 6071.9] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 0.9 [0.7, 1.1] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13740.2 [13676.6, 13784.6] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1622.4 [1613.0, 1628.4] ms (-43.3/+3.6) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1623.5 [1616.1, 1629.1] ms (-43.3/+3.6) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1623.2 [1614.5, 1633.2] ms (-43.3/+3.6) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.5 [0.4, 0.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1625.2 [1620.3, 1628.6] ms (-43.3/+3.6) n=10 | - |
| hold-zero | inconclusive 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.8 [0.8, 1.1] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.7, 1.3] ms (-0.4/+0.4) n=10 | resume from c=0.0.0.0: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| codec-change | pass 10/10 | end of the question to agent speech: 1606.4 [1603.2, 1684.8] ms (-67.7/+2.5) n=10 | - |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 739.1 [697.6, 774.9] ms (-109.8/+11.4) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 28.0 [-31.9, 50.1] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 4 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 6055.0 [6011.5, 6091.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.8, 1.1] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 6069.9 [6020.2, 6114.5] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13756.0 [13698.4, 13783.1] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1622.3 [1578.1, 1699.8] ms (-60.9/+15.5) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1602.1 [1584.9, 1751.1] ms (-60.9/+15.5) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 1.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1627.4 [1588.0, 1686.6] ms (-60.9/+15.5) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.5 [0.4, 0.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1611.2 [1577.7, 1677.8] ms (-60.9/+15.5) n=10 | - |
| hold-zero | inconclusive 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.8 [0.7, 1.1] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10 | resume from c=0.0.0.0: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| codec-change | pass 10/10 | end of the question to agent speech: 1645.1 [1570.7, 1771.0] ms (-102.9/+13.1) n=10 | - |


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
| clean | 10 | 120/120 | 1469 | 1588 | 1596 | 1586 .. 1590 | 0 | [-3.2, +44.6] webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5) |
| lte | 10 | 120/120 | 1551 | 1662 | 1675 | 1659 .. 1667 | 0 | [-3.6, +43.3] webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5) |
| lte-bad | 10 | 120/120 | 1533 | 1656 | 1727 | 1641 .. 1674 | 0 | [-15.5, +60.9] webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5) |

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts).

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | across a clock step | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 1/51 | 0% .. 14% | 1330 | 1330 | 1330 | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
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
| clean | 120 | 1588 [1469, 1596] | 1 [-111, 5] | 1501 [1501, 1502] | 88 [78, 92] |
| lte | 120 | 1662 [1551, 1675] | 41 [-69, 47] | 1501 [1500, 1502] | 121 [109, 132] |
| lte-bad | 120 | 1656 [1533, 1727] | 41 [-56, 84] | 1501 [1500, 1502] | 112 [46, 161] |

Greeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the target's request for a greeting (negative: asked before answering), the engine's 500 ms, and from its first audio to the agent's speech on the wire (webrtcvad onset bar).

| profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 10 | 694 [689, 816] | 153 [146, 189] | 501 [501, 501] | 39 [38, 127] |
| lte | 10 | 727 [723, 733] | 146 [144, 150] | 501 [501, 502] | 79 [75, 85] |
| lte-bad | 10 | 736 [698, 775] | 146 [142, 148] | 501 [501, 502] | 89 [51, 126] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 180 | 207.0 [41.2, 832.0] | 1.44 [0.89, 2.29] |
| lte | 180 | 234.6 [67.6, 833.2] | 4.23 [3.34, 4.99] |
| lte-bad | 167 | 286.3 [111.1, 844.3] | 19.73 [13.82, 22.78] |

Pauses: where the agent stopped sending RTP for a second or more and went on with the same stream, outside a hold (silence suppression, RFC 3551 4.1), median [min, max]: per call; how far the RTP clock fell behind across each, ms (the pause less what the timestamps advanced: 0 if they kept time, as RFC 3550 5.1 requires); and how many packets after one carry the marker bit, as 4.1 asks. A carrier that hangs up on RTP inactivity may hang up on these.

| profile | calls | pauses | clock behind | marker |
| --- | --- | --- | --- | --- |
| clean | 170 | 1 [0, 12] | 8038 [287, 31020] | 0/311 |
| lte | 170 | 1 [0, 12] | 8113 [5692, 31021] | 0/310 |
| lte-bad | 170 | 1 [0, 12] | 8099 [5647, 31071] | 0/310 |

## Engine audio as the caller received it

The mock engine's answers as the caller received them (completed answers in the latency and barge-in calls), median [min, max] over answers. Each piece of speech is aligned with what the mock sent; for 24 kHz audio, that is its interpolation through an ideal 8 kHz converter, so the mock's own resampling is not counted. Samples in packets the network lost are left out. unchanged: answers whose aligned speech came through sample for sample (pauses are not compared). distortion: the audio against what no linear filter of ±4 ms explains; a resampler or band filter would leave G.711's own, about 37 dB. moved: answers where a piece came out 5 ms or more later or earlier than the one before (a pause lengthened or shortened, audio inserted or dropped), and the largest move. gain: least squares. 3.4-4 kHz: that band against 300-3400 Hz, relative to what was sent.

| profile | answers | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB |
| --- | --- | --- | --- | --- | --- | --- |
| clean | 221 | 0 | 25.6 [25.6, 29.4] | 0 | -0.2 [-0.2, -0.2] | -1.1 [-2.3, -1.1] |
| lte | 217 | 0 | 25.6 [21.4, 36.0] | 0 | -0.2 [-0.2, -0.2] | -1.9 [-2.5, -1.0] |
| lte-bad | 208 | 0 | 28.2 [17.3, 36.4] | 11, up to 60 ms | -0.2 [-0.2, -0.2] | -2.3 [-2.9, +9.2] |

## Caller audio as the engine received it

The caller's lines in the latency and barge-in calls as the mock engine received them, aligned piece by piece with what the caller sent (its own capture, before the network), median [min, max] over lines; the columns as for the engine's audio above. Lost packets are the target's to fill: what it filled them with counts as distortion, and what it left out as moved. above 4 kHz: energy above 4 kHz against 300-3400 Hz in 24 kHz audio (the caller sends none). full scale: lines with samples at full scale. missing 20 ms: the caller's voiced 20 ms with nothing like them within 25 ms in what the engine got, and what came in their place: silence, the 20 ms before again (repeat), or other (also the next audio, where a packet was left out: see moved). appends: the audio each append carried, the median of each call's.

| profile | lines | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB | above 4 kHz, dB | full scale | missing 20 ms | appends, ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 220 | 0 | 43.3 [41.1, 47.5] | 0 | -0.4 [-0.6, -0.3] | -5.6 [-5.9, -5.2] | -25.2 [-31.0, -22.1] | 0 | 0.0% | 20 [20, 20] |
| lte | 213 | 0 | 42.4 [-2.4, 47.5] | 62, up to 60 ms | -0.4 [-5.8, -0.3] | -5.6 [-6.9, -4.1] | -25.1 [-31.0, -22.0] | 0 | 0.3%: 6 silence, 35 other | 20 [20, 20] |
| lte-bad | 161 | 0 | 10.8 [-0.8, 47.5] | 112, up to 60 ms | -1.0 [-5.9, -0.3] | -5.5 [-8.2, -2.4] | -25.3 [-31.5, -18.4] | 0 | 3.0%: 41 silence, 212 other | 20 [20, 20] |
