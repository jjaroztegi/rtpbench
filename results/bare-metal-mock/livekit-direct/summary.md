### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 688.0 [661.1, 696.9] ms (-32.9/+3.8) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.2 [0.2, 0.3] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 1.4 [1.3, 1.8] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 0.4 [0.4, 0.8] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 1.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.3, 0.7] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.3 [0.2, 0.3] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1646.5 [1641.0, 1653.4] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1001.1 [1000.6, 1001.5] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1650.8 [1644.1, 1656.1] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 662.5 [656.9, 706.0] ms (-32.9/+3.8) n=10 | - |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1828.9 [1817.4, 1842.4] ms (-32.9/+3.8) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1822.5 [1814.4, 1845.0] ms (-32.9/+3.8) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1829.6 [1807.1, 1844.5] ms (-32.9/+3.8) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1823.9 [1814.0, 1843.7] ms (-32.9/+3.8) n=10 | - |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) |
| codec-change | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 721.9 [695.3, 739.7] ms (-32.3/+3.4) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.2 [0.2, 0.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 41.5 [38.0, 47.8] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 0.4 [0.4, 0.5] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 124 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.2 [0.2, 0.4] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1731.9 [1669.8, 1783.3] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1001.0 [1000.6, 1001.4] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1705.9 [1665.6, 1780.7] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 732.9 [693.3, 786.4] ms (-32.3/+3.4) n=10 | - |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1928.6 [1893.5, 1991.3] ms (-32.3/+3.4) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1949.5 [1890.5, 1989.7] ms (-32.3/+3.4) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1922.1 [1894.0, 2143.3] ms (-32.3/+3.4) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1944.8 [1901.1, 2033.0] ms (-32.3/+3.4) n=10 | - |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) |
| codec-change | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 721.3 [676.0, 799.4] ms (-52.5/+16.7) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.2 [0.2, 0.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 64.9 [34.6, 111.0] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 0.4 [0.4, 0.6] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 122 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 114 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.3 [0.2, 0.5] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1844.6 [1756.6, 2015.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1001.3 [1000.7, 1001.5] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1874.8 [1738.9, 2011.7] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 733.8 [676.2, 752.1] ms (-52.5/+16.7) n=10 | - |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 2050.8 [1969.2, 2154.5] ms (-52.5/+16.7) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 2134.7 [1988.7, 2208.7] ms (-52.5/+16.7) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 2063.7 [1994.3, 2239.2] ms (-52.5/+16.7) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 2120.7 [1986.2, 2255.6] ms (-52.5/+16.7) n=10 | - |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 113 packets) |
| codec-change | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) |


Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-16.7, +52.5] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech --profiles lte-bad)
- [-3.8, +32.9] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech)
- [-3.4, +32.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech --profiles lte)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)

Wall-clock steps during the run: none.

## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | across a clock step | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 10 | 120/120 | 1712 | 1834 | 1893 | 1826 .. 1844 | 0 | [-3.8, +32.9] webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech) |
| lte | 10 | 120/120 | 1868 | 1984 | 2065 | 1948 .. 2019 | 0 | [-3.4, +32.3] webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech --profiles lte) |
| lte-bad | 10 | 120/120 | 1941 | 2109 | 2284 | 2072 .. 2151 | 0 | [-16.7, +52.5] webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech --profiles lte-bad) |

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts).

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | across a clock step | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 51/51 | 100% .. 100% | -11 | 298 | 479 | 0 | [-79.2, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in --codecs pcmu) |
| clean | backchannel | 10 | 25/25 | 100% .. 100% | -142 | 245 | 424 | 0 | [-79.2, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in --codecs pcmu) |
| clean | cough | 10 | 24/24 | 100% .. 100% | -93 | 238 | 442 | 0 | [-79.2, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in --codecs pcmu) |
| lte | interrupt | 10 | 51/51 | 100% .. 100% | 53 | 476 | 622 | 0 | [-71.0, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in --codecs pcmu --profiles lte) |
| lte | backchannel | 10 | 25/25 | 100% .. 100% | -10 | 428 | 525 | 0 | [-71.0, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in --codecs pcmu --profiles lte) |
| lte | cough | 10 | 24/24 | 100% .. 100% | 120 | 437 | 596 | 0 | [-71.0, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in --codecs pcmu --profiles lte) |
| lte-bad | interrupt | 10 | 51/51 | 100% .. 100% | 210 | 641 | 863 | 0 | [-94.2, +5.4] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in --codecs pcmu --profiles lte-bad) |
| lte-bad | backchannel | 10 | 25/25 | 100% .. 100% | 423 | 543 | 740 | 0 | [-94.2, +5.4] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in --codecs pcmu --profiles lte-bad) |
| lte-bad | cough | 10 | 24/24 | 100% .. 100% | 173 | 587 | 797 | 0 | [-94.2, +5.4] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in --codecs pcmu --profiles lte-bad) |

## Turn latency by part

Turn latency on the mock engine, split where it heard the end of the caller's speech and sent its first audio (one clock with the captures), ms, p50 [p5, p95]: uplink and downlink are the target's; the engine waits 1000 ms of silence and answers 500 ms later by design. Uplink carries the caller's label error (±17 ms), downlink the onset error bar of the profile and codec.

| profile | turns | wire latency | uplink | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 120 | 1834 [1712, 1893] | 186 [61, 201] | 1501 [1501, 1502] | 148 [135, 193] |
| lte | 120 | 1984 [1868, 2065] | 290 [182, 354] | 1501 [1501, 1502] | 186 [168, 230] |
| lte-bad | 120 | 2109 [1941, 2284] | 411 [229, 550] | 1501 [1501, 1502] | 193 [144, 253] |

Greeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the target's request for a greeting (negative: asked before answering), the engine's 500 ms, and from its first audio to the agent's speech on the wire (webrtcvad onset bar).

| profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 10 | 687 [661, 697] | -8 [-35, -5] | 501 [501, 502] | 196 [191, 206] |
| lte | 10 | 719 [695, 740] | -17 [-46, -5] | 501 [501, 502] | 233 [224, 258] |
| lte-bad | 10 | 719 [676, 799] | -15 [-54, -7] | 501 [501, 502] | 235 [200, 305] |
