### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 682.9 [603.8, 697.7] ms (-63.6/-1.0) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.2 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 1.6 [1.3, 3.6] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 0.5 [0.4, 0.5] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.4, 1.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.4, 1.3] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.3 [0.2, 0.4] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1652.9 [1649.1, 1666.6] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1001.0 [1000.7, 1001.7] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1651.4 [1644.0, 1659.5] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 670.0 [662.3, 718.1] ms (-44.6/+3.2) n=10 | - |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1824.2 [1815.5, 1844.1] ms (-44.6/+3.2) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1830.2 [1802.5, 1844.5] ms (-44.6/+3.2) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.4, 0.8] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1833.4 [1812.4, 1846.6] ms (-44.6/+3.2) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 2.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1828.4 [1807.1, 1841.6] ms (-44.6/+3.2) n=10 | - |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 2.3] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) |
| codec-change | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 728.7 [714.4, 742.7] ms (-67.6/+0.8) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.2 [0.2, 0.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 41.6 [40.4, 43.6] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 0.4 [0.4, 1.1] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 126 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.3 [0.2, 0.3] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1716.9 [1683.0, 1816.5] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1001.1 [1000.6, 1002.2] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1709.8 [1684.0, 1824.9] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 735.3 [694.6, 757.6] ms (-43.3/+3.6) n=10 | - |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1930.2 [1876.1, 2023.3] ms (-43.3/+3.6) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1909.7 [1897.8, 2074.0] ms (-43.3/+3.6) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1930.8 [1873.2, 1963.7] ms (-43.3/+3.6) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1931.4 [1903.9, 1982.5] ms (-43.3/+3.6) n=10 | - |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 0.8] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 124 packets) |
| codec-change | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 733.3 [724.6, 805.7] ms (-109.8/+11.4) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.2 [0.2, 0.3] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 64.4 [38.2, 96.2] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 0.5 [0.4, 0.8] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.3, 0.7] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 119 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 118 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.2 [0.2, 0.4] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1825.1 [1745.6, 2183.2] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1001.0 [1000.7, 1001.7] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1837.1 [1746.2, 2002.3] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 733.5 [692.6, 748.5] ms (-60.9/+15.5) n=10 | - |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 2040.7 [1935.5, 2180.4] ms (-60.9/+15.5) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 2046.2 [1986.7, 2288.4] ms (-60.9/+15.5) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 2083.1 [1931.0, 2183.1] ms (-60.9/+15.5) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 2150.5 [1928.0, 2231.7] ms (-60.9/+15.5) n=10 | - |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 119 packets) |
| codec-change | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) |


Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-15.5, +60.9] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5)
- [-11.4, +109.8] ms: webrtcvad first onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5)
- [-3.6, +43.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5)
- [-3.2, +44.6] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5)
- [-0.8, +67.6] ms: webrtcvad first onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
- [+1.0, +63.6] ms: webrtcvad first onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5)

Wall-clock steps during the run: none.

## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | across a clock step | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 10 | 120/120 | 1713 | 1833 | 1893 | 1826 .. 1852 | 0 | [-3.2, +44.6] webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5) |
| lte | 10 | 120/120 | 1879 | 1997 | 2109 | 1973 .. 2015 | 0 | [-3.6, +43.3] webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5) |
| lte-bad | 10 | 120/120 | 1924 | 2134 | 2273 | 2080 .. 2174 | 0 | [-15.5, +60.9] webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5) |

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts).

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | across a clock step | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 51/51 | 100% .. 100% | 2 | 306 | 486 | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| clean | backchannel | 10 | 25/25 | 100% .. 100% | -16 | 296 | 416 | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| clean | cough | 10 | 24/24 | 100% .. 100% | -88 | 283 | 419 | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| lte | interrupt | 10 | 51/51 | 100% .. 100% | 47 | 459 | 643 | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte | backchannel | 10 | 25/25 | 100% .. 100% | 10 | 441 | 543 | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte | cough | 10 | 24/24 | 100% .. 100% | 148 | 438 | 630 | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte-bad | interrupt | 10 | 51/51 | 100% .. 100% | 153 | 579 | 812 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | backchannel | 10 | 25/25 | 100% .. 100% | 224 | 619 | 719 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | cough | 10 | 24/24 | 100% .. 100% | 159 | 545 | 708 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |

## Turn latency by part

Turn latency on the mock engine, split where it heard the end of the caller's speech and sent its first audio (one clock with the captures), ms, p50 [p5, p95]: uplink and downlink are the target's; the engine waits 1000 ms of silence and answers 500 ms later by design. Uplink carries the caller's label error (±17 ms), downlink the onset error bar of the profile and codec.

| profile | turns | wire latency | uplink | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 120 | 1833 [1713, 1893] | 186 [60, 203] | 1501 [1501, 1503] | 149 [134, 197] |
| lte | 120 | 1997 [1879, 2109] | 302 [196, 401] | 1501 [1501, 1502] | 189 [170, 232] |
| lte-bad | 120 | 2134 [1924, 2273] | 426 [267, 582] | 1501 [1501, 1502] | 201 [157, 258] |

Greeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the target's request for a greeting (negative: asked before answering), the engine's 500 ms, and from its first audio to the agent's speech on the wire (webrtcvad onset bar).

| profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 10 | 681 [604, 698] | -21 [-100, -8] | 501 [500, 503] | 203 [187, 210] |
| lte | 10 | 727 [714, 743] | -6 [-12, 5] | 501 [501, 501] | 235 [222, 240] |
| lte-bad | 10 | 733 [725, 806] | -8 [-30, -3] | 501 [501, 502] | 238 [235, 314] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 180 | 21.1 [0.7, 22.7] | 0.19 [0.04, 0.56] |
| lte | 180 | 34.4 [9.7, 39.4] | 3.34 [2.20, 3.79] |
| lte-bad | 180 | 122.6 [81.0, 142.2] | 20.10 [15.12, 21.48] |

## Engine audio as the caller received it

The mock engine's answers as the caller received them (completed answers in the latency and barge-in calls), median [min, max] over answers. Each piece of speech is aligned with what the mock sent; for 24 kHz audio, that is its interpolation through an ideal 8 kHz converter, so the mock's own resampling is not counted. Samples in packets the network lost are left out. unchanged: answers with every sample as sent. distortion: the audio against what no linear filter of ±4 ms explains; a resampler or band filter would leave G.711's own, about 37 dB. moved: answers where a piece came out 5 ms or more later or earlier than the one before (a pause lengthened or shortened, audio inserted or dropped), and the largest move. gain: least squares. 3.4-4 kHz: that band against 300-3400 Hz, relative to what was sent.

| profile | answers | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB |
| --- | --- | --- | --- | --- | --- | --- |
| clean | 240 | 0 | 27.4 [23.0, 29.7] | 14, up to 40 ms | -0.2 [-0.3, -0.0] | -8.2 [-8.9, -7.3] |
| lte | 240 | 0 | 27.3 [23.0, 29.8] | 23, up to 40 ms | -0.2 [-0.3, -0.0] | -8.2 [-12.5, -7.4] |
| lte-bad | 237 | 0 | 26.8 [20.7, 30.1] | 17, up to 40 ms | -0.2 [-0.3, -0.0] | -10.1 [-15.4, +11.1] |
