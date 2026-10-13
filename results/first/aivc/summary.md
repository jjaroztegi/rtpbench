### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 7, fail 3 | 200 OK to agent speech: 1386.8 [1131.1, 5811.8] ms (-24.3/+88.1) n=10 | agent speaks within 2000 ms (3/10) |
| bye | pass 10/10 | BYE to its response: 0.3 [0.2, 0.6] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: -9.2 [-19.6, 0.6] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 2 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.9 [0.8, 1.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.0 [0.7, 1.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 6.0 [0.2, 17.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.0 [-0.1, 0.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.9 [0.7, 1.2] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.0 [0.8, 1.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 14.6 [5.3, 19.4] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.0 [-0.1, 0.1] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 39981.0 [39903.7, 40002.9] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1759.4 [1460.0, 4730.3] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1549.9 [631.1, 3128.0] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1960.6 [1623.3, 8199.8] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 926.2 [291.8, 1286.9] ms (-24.3/+88.1) n=4 | agent keeps the call for 10 s (10/10: BYE 830 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 6, fail 4 | 200 OK to agent speech: 1406.2 [1183.7, 2698.7] ms (-25.2/+87.6) n=10 | agent speaks within 2000 ms (4/10) |
| bye | pass 10/10 | BYE to its response: 0.3 [0.2, 0.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 36.6 [-23.3, 42.7] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 3 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.9 [0.7, 1.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.9 [0.8, 1.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 48.5 [40.1, 63.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.3 [-3.8, 6.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.9 [0.7, 1.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.0 [0.9, 1.3] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 49.0 [17.0, 57.7] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.5 [-48.2, 19.2] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly); resume from inactive: same RTP stream (1/10: ssrc 0x16319700->0x16319700, seq 4502->4503, clock -48 ms) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 39972.6 [39942.2, 40002.0] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1814.7 [1424.8, 5365.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2040.3 [1357.1, 3044.8] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1893.1 [1411.8, 2794.7] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 1137.3 [261.2, 1331.4] ms (-25.2/+87.6) n=4 | agent keeps the call for 10 s (10/10: BYE 3104 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 7, fail 3 | 200 OK to agent speech: 1300.0 [1195.3, 4643.4] ms (-35.1/+96.9) n=10 | agent speaks within 2000 ms (3/10) |
| bye | pass 10/10 | BYE to its response: 0.3 [0.2, 0.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 47.1 [4.4, 65.0] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 2 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.9 [0.9, 2.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.9 [0.7, 2.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 40.8 [6.3, 109.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.3 [-11.9, 15.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.1 [0.7, 2.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.1 [0.8, 1.9] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 41.7 [12.2, 108.0] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.5 [-18.8, 21.4] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 39980.0 [39953.4, 40001.4] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1877.5 [1347.8, 5160.9] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2237.4 [1079.0, 3568.0] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 2359.5 [1538.9, 9661.1] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 435.7 [194.0, 1350.5] ms (-35.1/+96.9) n=5 | agent keeps the call for 10 s (10/10: BYE 2028 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |


Error bars: true value = measured - error, error within

- [-96.9, +35.1] ms: webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech --profiles lte-bad)
- [-88.1, +24.3] ms: webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech)
- [-87.6, +25.2] ms: webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech --profiles lte)
- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)

## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 10 | 120/120 | 795 | 1109 | 4682 | 1000 .. 2281 | [-88.1, +24.3] webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech) |
| lte | 10 | 120/120 | 833 | 1209 | 3656 | 1050 .. 1839 | [-87.6, +25.2] webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech --profiles lte) |
| lte-bad | 10 | 120/120 | 905 | 1206 | 4753 | 1057 .. 2802 | [-96.9, +35.1] webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech --profiles lte-bad) |

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts).

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 51/51 | 100% .. 100% | -66 | 287 | 560 | [-71.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in) |
| clean | backchannel | 10 | 21/25 | 67% .. 100% | -280 | 182 | 270 | [-71.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in) |
| clean | cough | 10 | 1/24 | 0% .. 33% | 407 | 407 | 407 | [-71.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in) |
| lte | interrupt | 10 | 49/50 | 86% .. 100% | 205 | 368 | 801 | [-72.1, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in --profiles lte) |
| lte | backchannel | 10 | 24/25 | 67% .. 100% | -16 | 279 | 547 | [-72.1, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in --profiles lte) |
| lte | cough | 10 | 0/24 | 0% .. 0% | - | - | - | [-72.1, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in --profiles lte) |
| lte-bad | interrupt | 10 | 51/51 | 100% .. 100% | 64 | 404 | 764 | [-118.8, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in --profiles lte-bad) |
| lte-bad | backchannel | 10 | 24/25 | 67% .. 100% | 15 | 263 | 491 | [-118.8, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in --profiles lte-bad) |
| lte-bad | cough | 10 | 0/24 | 0% .. 0% | - | - | - | [-118.8, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in --profiles lte-bad) |
