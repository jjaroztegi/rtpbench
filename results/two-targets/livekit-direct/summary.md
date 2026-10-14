### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 8, fail 2 | 200 OK to agent speech: 1355.5 [894.0, 4368.9] ms (-32.9/+3.8) n=10 | agent speaks within 2000 ms (2/10) |
| bye | pass 10/10 | BYE to its response: 0.4 [0.2, 3.7] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 8.5 [1.1, 46.1] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 1.5 [0.5, 121.0] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.8 [0.4, 3.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.7 [0.3, 6.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.7 [0.4, 1.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.8 [0.4, 1.9] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.7 [0.4, 1.9] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 2051.2 [1570.8, 9724.4] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1003.3 [1001.1, 1032.8] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 3027.7 [1694.4, 8432.5] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 472.4 [71.6, 2029.5] ms (-32.9/+3.8) n=10 | - |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1421.1 [1240.2, 2205.2] ms (-32.9/+3.8) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.6 [0.3, 8.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1416.4 [1297.8, 2838.3] ms (-32.9/+3.8) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.9 [0.4, 3.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1437.3 [1300.3, 2552.9] ms (-32.9/+3.8) n=10 | - |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 1.4 [0.6, 4.3] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.9 [0.5, 10.9] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) |
| codec-change | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 1226.9 [986.7, 1422.0] ms (-32.3/+3.4) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.5 [0.3, 1.0] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 47.0 [40.6, 133.0] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 1.4 [0.5, 187.4] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.5 [0.5, 16.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.9 [0.4, 2.8] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.5 [0.4, 1.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.7 [0.5, 2.1] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 124 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 126 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.5 [0.3, 1.0] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 2242.2 [1755.7, 7300.9] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1003.7 [1001.9, 1039.7] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 2198.6 [1731.1, 3949.8] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 521.2 [21.9, 1155.8] ms (-32.3/+3.4) n=10 | - |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1534.8 [1283.9, 3563.6] ms (-32.3/+3.4) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.7 [0.6, 4.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1581.7 [1408.1, 5788.9] ms (-32.3/+3.4) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.6 [0.4, 2.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1526.1 [1363.5, 2169.6] ms (-32.3/+3.4) n=10 | - |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.7 [0.5, 12.8] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.7 [0.4, 1.8] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) |
| codec-change | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 9, fail 1 | 200 OK to agent speech: 1146.6 [972.0, 4200.8] ms (-52.5/+16.7) n=10 | agent speaks within 2000 ms (1/10) |
| bye | pass 10/10 | BYE to its response: 0.4 [0.3, 3.9] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 61.5 [-39.7, 75.2] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 2.1 [0.5, 341.3] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.6 [0.6, 19.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.7 [0.4, 7.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.8 [0.4, 3.8] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.9 [0.5, 2.1] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 110 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 122 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.5 [0.3, 5.2] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | flips: pass 9, fail 1 | end of the request to REFER: 2534.3 [1972.5, 4931.3] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1002.1 [1001.1, 1006.0] ms (-0.4/+0.4) n=9 | agent hangs up within 10 s (1/10) |
| refer-fail | pass 10/10 | end of the request to REFER: 2029.2 [1394.2, 2350.4] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 473.2 [105.0, 848.2] ms (-52.5/+16.7) n=10 | - |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1571.9 [1397.4, 5506.5] ms (-52.5/+16.7) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.0 [0.5, 5.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1685.3 [1442.2, 3333.6] ms (-52.5/+16.7) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.7 [0.4, 3.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1621.3 [1415.7, 3291.0] ms (-52.5/+16.7) n=10 | - |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.8 [0.4, 7.8] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 1.8 [0.6, 22.4] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 123 packets) |
| codec-change | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) |


Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-16.7, +52.5] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech --profiles lte-bad)
- [-3.8, +32.9] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech)
- [-3.4, +32.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech --profiles lte)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)

## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 10 | 120/120 | 1280 | 1654 | 3984 | 1543 .. 2029 | [-3.8, +32.9] webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech) |
| lte | 10 | 115/120 | 1325 | 1695 | 6328 | 1569 .. 1969 | [-3.4, +32.3] webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech --profiles lte) |
| lte-bad | 10 | 119/120 | 1394 | 1831 | 3518 | 1657 .. 2244 | [-16.7, +52.5] webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech --profiles lte-bad) |

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts).

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 49/50 | 86% .. 100% | 477 | 707 | 1574 | [-79.2, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in --codecs pcmu) |
| clean | backchannel | 10 | 21/25 | 33% .. 100% | 507 | 645 | 1113 | [-79.2, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in --codecs pcmu) |
| clean | cough | 10 | 1/22 | 0% .. 25% | 1617 | 1617 | 1617 | [-79.2, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in --codecs pcmu) |
| lte | interrupt | 10 | 47/49 | 67% .. 100% | 448 | 768 | 1347 | [-71.0, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in --codecs pcmu --profiles lte) |
| lte | backchannel | 10 | 21/22 | 67% .. 100% | 502 | 753 | 943 | [-71.0, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in --codecs pcmu --profiles lte) |
| lte | cough | 10 | 1/22 | 0% .. 33% | 1219 | 1219 | 1219 | [-71.0, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in --codecs pcmu --profiles lte) |
| lte-bad | interrupt | 10 | 46/49 | 60% .. 100% | 514 | 896 | 1288 | [-94.2, +5.4] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in --codecs pcmu --profiles lte-bad) |
| lte-bad | backchannel | 10 | 19/21 | 50% .. 100% | 338 | 869 | 1825 | [-94.2, +5.4] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in --codecs pcmu --profiles lte-bad) |
| lte-bad | cough | 10 | 3/21 | 0% .. 67% | 1446 | 1954 | 1976 | [-94.2, +5.4] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in --codecs pcmu --profiles lte-bad) |
