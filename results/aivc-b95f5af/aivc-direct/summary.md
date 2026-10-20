### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 541.2 [541.0, 542.4] ms (-64.9/-1.1) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 0.2 [-19.8, 0.3] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 2 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.8 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.9 [0.8, 1.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 5.1 [2.0, 6.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.0 [-0.1, 0.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.8 [0.7, 1.1] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.9 [0.7, 1.1] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 2.3 [1.2, 19.3] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.0 [-0.0, 0.0] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.6 [0.5, 0.7] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 501 Not Implemented); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1502.4 [1502.0, 1502.9] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 12.5 [10.4, 19.5] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1502.3 [1501.9, 1502.7] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 518.5 [516.9, 519.0] ms (-11.0/+133.0) n=10 | - |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1508.6 [1508.0, 1529.2] ms (-11.0/+133.0) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1508.2 [1508.0, 1509.1] ms (-11.0/+133.0) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.7 [0.6, 1.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1508.3 [1508.0, 1509.1] ms (-11.0/+133.0) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.8 [0.6, 2.1] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.6, 0.9] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) |
| codec-change | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU after it (10/10: payload types 8); agent replies within 10000 ms (10/10) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 580.5 [574.6, 588.1] ms (-67.7/+2.5) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 36.3 [20.8, 42.3] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 2 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.9 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 52.4 [49.3, 59.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.9 [-1.6, 5.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.9 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 50.9 [46.1, 54.1] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.9 [-3.6, 4.7] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.6 [0.5, 1.1] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 501 Not Implemented); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1541.5 [1536.5, 1546.0] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 13.3 [0.9, 19.6] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1541.4 [1518.3, 1548.1] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 560.7 [551.0, 563.8] ms (-14.1/+131.0) n=10 | - |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1589.2 [1583.5, 1602.9] ms (-14.1/+131.0) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1585.7 [1583.1, 1598.6] ms (-14.1/+131.0) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.7 [0.6, 0.8] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1588.6 [1581.4, 1607.3] ms (-14.1/+131.0) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.7 [0.6, 0.9] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.7 [0.7, 0.8] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 122 packets) |
| codec-change | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU after it (10/10: payload types 8); agent replies within 10000 ms (10/10) |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 573.2 [552.2, 625.8] ms (-102.9/+13.1) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.3 [0.3, 0.3] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 35.6 [18.3, 62.4] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 2 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.9 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 47.3 [0.2, 120.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 6.4 [-18.7, 24.6] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.9 [0.8, 0.9] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 42.5 [10.6, 89.3] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -1.1 [-26.3, 10.0] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.6 [0.5, 0.6] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 501 Not Implemented); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1545.9 [1511.2, 1584.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 13.5 [4.8, 16.1] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1546.8 [1524.6, 1600.3] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 547.6 [510.0, 618.2] ms (-22.9/+141.5) n=10 | - |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1614.6 [1564.6, 1651.1] ms (-22.9/+141.5) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1641.7 [1550.6, 1670.2] ms (-22.9/+141.5) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.7 [0.6, 0.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1604.7 [1539.5, 1639.5] ms (-22.9/+141.5) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.7 [0.6, 0.9] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.7 [0.6, 0.8] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 117 packets) |
| codec-change | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU after it (10/10: payload types 8); agent replies within 10000 ms (10/10) |


Error bars: true value = measured - error, error within

- [-141.5, +22.9] ms: webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech, seeds 1-5)
- [-133.0, +11.0] ms: webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech, seeds 1-5)
- [-131.0, +14.1] ms: webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech, seeds 1-5)
- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-13.1, +102.9] ms: webrtcvad first onset, p5..p95, PCMA, lte-bad (calibrate --speech, seeds 1-5)
- [-2.5, +67.7] ms: webrtcvad first onset, p5..p95, PCMA, lte (calibrate --speech, seeds 1-5)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
- [+1.1, +64.9] ms: webrtcvad first onset, p5..p95, PCMA, clean (calibrate --speech, seeds 1-5)

Wall-clock steps during the run: none.

## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | across a clock step | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 10 | 120/120 | 1504 | 1511 | 1517 | 1509 .. 1512 | 0 | [-133.0, +11.0] webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech, seeds 1-5) |
| lte | 10 | 120/120 | 1583 | 1593 | 1609 | 1589 .. 1598 | 0 | [-131.0, +14.1] webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech, seeds 1-5) |
| lte-bad | 10 | 120/120 | 1546 | 1604 | 1652 | 1579 .. 1628 | 0 | [-141.5, +22.9] webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech, seeds 1-5) |

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts).

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | across a clock step | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 51/51 | 100% .. 100% | -311 | 23 | 179 | 0 | [-84.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in, seeds 1-5) |
| clean | backchannel | 10 | 25/25 | 100% .. 100% | -191 | 13 | 150 | 0 | [-84.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in, seeds 1-5) |
| clean | cough | 10 | 24/24 | 100% .. 100% | -331 | -1 | 148 | 0 | [-84.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in, seeds 1-5) |
| lte | interrupt | 10 | 51/51 | 100% .. 100% | -156 | 98 | 259 | 0 | [-77.6, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in, seeds 1-5) |
| lte | backchannel | 10 | 25/25 | 100% .. 100% | -188 | 83 | 212 | 0 | [-77.6, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in, seeds 1-5) |
| lte | cough | 10 | 24/24 | 100% .. 100% | -265 | 75 | 233 | 0 | [-77.6, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in, seeds 1-5) |
| lte-bad | interrupt | 10 | 51/51 | 100% .. 100% | -64 | 112 | 279 | 0 | [-100.7, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | backchannel | 10 | 25/25 | 100% .. 100% | -158 | 81 | 202 | 0 | [-100.7, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | cough | 10 | 24/24 | 100% .. 100% | -90 | 98 | 290 | 0 | [-100.7, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in, seeds 1-5) |

## Turn latency by part

Turn latency on the mock engine, split where it heard the end of the caller's speech and sent its first audio (one clock with the captures), ms, p50 [p5, p95]: uplink and downlink are the target's; the engine waits 1000 ms of silence and answers 500 ms later by design. Uplink carries the caller's label error (±17 ms), downlink the onset error bar of the profile and codec.

| profile | turns | wire latency | uplink | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 120 | 1511 [1504, 1517] | 0 [-2, 4] | 1501 [1500, 1501] | 9 [2, 16] |
| lte | 120 | 1593 [1583, 1609] | 40 [36, 48] | 1501 [1501, 1502] | 51 [40, 62] |
| lte-bad | 120 | 1604 [1546, 1652] | 40 [1, 85] | 1501 [1500, 1502] | 57 [21, 106] |

Greeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the target's request for a greeting (negative: asked before answering), the engine's 500 ms, and from its first audio to the agent's speech on the wire (webrtcvad onset bar).

| profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 10 | 541 [541, 542] | 2 [2, 3] | 501 [500, 502] | 38 [37, 40] |
| lte | 10 | 580 [575, 588] | 2 [2, 2] | 501 [501, 501] | 77 [71, 85] |
| lte-bad | 10 | 572 [552, 626] | 2 [2, 3] | 501 [500, 502] | 69 [49, 123] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 180 | 1.1 [0.7, 3.4] | 0.20 [0.03, 0.33] |
| lte | 180 | 15.7 [10.7, 19.8] | 3.33 [2.48, 3.63] |
| lte-bad | 180 | 106.8 [72.1, 142.1] | 20.02 [12.60, 21.72] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.

## Engine audio as the caller received it

The mock engine's answers as the caller received them (completed answers in the latency and barge-in calls), median [min, max] over answers. Each piece of speech is aligned with what the mock sent; for 24 kHz audio, that is its interpolation through an ideal 8 kHz converter, so the mock's own resampling is not counted. Samples in packets the network lost are left out. unchanged: answers whose aligned speech came through sample for sample (pauses are not compared). distortion: the audio against what no linear filter of ±4 ms explains; a resampler or band filter would leave G.711's own, about 37 dB. moved: answers where a piece came out 5 ms or more later or earlier than the one before (a pause lengthened or shortened, audio inserted or dropped), and the largest move. gain: least squares. 3.4-4 kHz: that band against 300-3400 Hz, relative to what was sent.

| profile | answers | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB |
| --- | --- | --- | --- | --- | --- | --- |
| clean | 230 | 230 | exact [exact, exact] | 0 | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| lte | 224 | 224 | exact [exact, exact] | 0 | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |
| lte-bad | 222 | 222 | exact [exact, exact] | 0 | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |

## Caller audio as the engine received it

The caller's lines in the latency and barge-in calls as the mock engine received them, aligned piece by piece with what the caller sent (its own capture, before the network), median [min, max] over lines; the columns as for the engine's audio above. Lost packets are the target's to fill: what it filled them with counts as distortion, and what it left out as moved. above 4 kHz: energy above 4 kHz against 300-3400 Hz in 24 kHz audio (the caller sends none). full scale: lines with samples at full scale. missing 20 ms: the caller's voiced 20 ms with nothing like them within 25 ms in what the engine got, and what came in their place: silence, the 20 ms before again (repeat), or other (also the next audio, where a packet was left out: see moved). appends: the audio each append carried, the median of each call's.

| profile | lines | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB | above 4 kHz, dB | full scale | missing 20 ms | appends, ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 320 | 320 | exact [exact, exact] | 0 | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |  | 0 | 0.0% | 20 [20, 20] |
| lte | 314 | 223 | exact [-2.3, exact] | 80, up to 60 ms | +0.0 [-5.8, +0.0] | +0.0 [-1.6, +1.3] |  | 0 | 0.8%: 15 silence, 126 other | 20 [20, 20] |
| lte-bad | 259 | 68 | 10.6 [-3.1, exact] | 158, up to 60 ms | -0.6 [-7.0, +0.0] | +0.0 [-4.0, +2.1] |  | 0 | 2.9%: 44 silence, 302 other | 20 [20, 20] |
