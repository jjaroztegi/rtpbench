### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 8, fail 2 | 200 OK to agent speech: 1549.9 [1342.4, 2790.8] ms (-24.3/+88.1) n=10 | agent speaks within 2000 ms (2/10) |
| bye | flips: pass 9, inconclusive 1 | BYE to its response: 1.4 [0.4, 4.7] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: -0.6 [-17.1, 0.9] ms (-0.4/+0.4) n=10 | agent was talking at the BYE (1/10) |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 26 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.5 [0.9, 26.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.6 [1.1, 12.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 7.9 [0.8, 17.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.1 [-0.4, 0.2] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.5 [1.0, 4.1] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.1 [1.3, 12.9] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 8.0 [0.3, 17.4] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.0 [-0.3, 0.0] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 39940.2 [39839.6, 39972.5] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1937.8 [1526.5, 6581.9] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1861.1 [1187.9, 3208.1] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1720.5 [1591.8, 3290.8] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 400.9 [98.7, 1858.3] ms (-24.3/+88.1) n=9 | agent keeps the call for 10 s (10/10: BYE 3414 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1099.0 [990.5, 5025.4] ms (-24.3/+88.1) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 3.3 [1.0, 12.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1269.6 [1049.6, 3909.0] ms (-24.3/+88.1) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 1.3 [0.9, 7.3] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 1.4 [0.8, 66.5] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) |
| codec-change | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU after it (10/10: payload types 8); agent replies within 10000 ms (10/10) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 7, fail 3 | 200 OK to agent speech: 1610.2 [1337.2, 5608.4] ms (-25.2/+87.6) n=10 | agent speaks within 2000 ms (3/10) |
| bye | pass 10/10 | BYE to its response: 0.5 [0.3, 7.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 34.3 [16.8, 42.7] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 12 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 3.5 [1.0, 52.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.8 [0.9, 10.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 49.4 [41.8, 73.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.4 [-4.3, 52.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 3.6 [1.2, 26.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.5 [0.9, 20.2] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 47.7 [36.9, 56.1] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.7 [-4.1, 5.7] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (1/10: ssrc 0x1032a718->0x1032a718, seq 4714->4715, clock +53 ms); inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 39901.5 [39838.6, 40043.2] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1798.2 [1576.5, 7449.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1680.4 [534.6, 2551.6] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1974.2 [1484.0, 7914.4] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 292.7 [103.5, 1096.1] ms (-25.2/+87.6) n=9 | agent keeps the call for 10 s (10/10: BYE 2600 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1189.1 [1090.3, 1716.1] ms (-25.2/+87.6) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.1 [0.8, 17.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1178.7 [1083.5, 2081.5] ms (-25.2/+87.6) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 6.6 [1.7, 39.0] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 6.1 [1.1, 25.5] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 116 packets) |
| codec-change | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU after it (10/10: payload types 8); agent replies within 10000 ms (10/10) |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 9, fail 1 | 200 OK to agent speech: 1539.0 [1269.1, 2175.6] ms (-35.1/+96.9) n=10 | agent speaks within 2000 ms (1/10) |
| bye | flips: pass 9, inconclusive 1 | BYE to its response: 0.9 [0.3, 8.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 27.9 [-9.6, 88.2] ms (-0.4/+0.4) n=10 | agent was talking at the BYE (1/10) |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 18 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.4 [1.2, 20.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.5 [0.8, 692.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 39.7 [1.3, 73.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 6.6 [-574.3, 15.2] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 3.1 [0.9, 122.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.3 [1.1, 6.9] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 33.6 [13.1, 144.4] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -11.2 [-43.7, 10.0] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (1/10: ssrc 0x8093e47->0x8093e47, seq 7798->7799, clock -574 ms); inactive hold: answer inactive (10/10: recvonly); resume from inactive: same RTP stream (1/10: ssrc 0x8093e47->0x8093e47, seq 8037->8038, clock -44 ms) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 39930.4 [39854.7, 39968.4] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1749.8 [1485.4, 2348.2] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1651.5 [1004.1, 2927.2] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1968.7 [1854.4, 2787.2] ms (-17.0/+17.0) n=9<br>failure NOTIFY to agent speech: 251.1 [158.2, 619.5] ms (-35.1/+96.9) n=8 | agent keeps the call for 10 s (9/10: BYE 3854 ms after it); agent speaks within 5000 ms (9/10); agent transfers (REFER) (1/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1254.8 [1093.3, 5309.0] ms (-35.1/+96.9) n=10 | - |
| reinvite | flips: pass 9, fail 1 | refresh re-INVITE to 2xx: 2.6 [0.9, 30.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1274.1 [1112.0, 2114.5] ms (-35.1/+96.9) n=9 | agent replies within 10000 ms (1/10) |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 2.4 [1.1, 7.7] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 3.5 [1.0, 16.2] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) |
| codec-change | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU after it (10/10: payload types 8); agent replies within 10000 ms (10/10) |


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
| clean | 10 | 120/120 | 882 | 1178 | 5340 | 1060 .. 2509 | [-88.1, +24.3] webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech) |
| lte | 10 | 120/120 | 933 | 1319 | 5175 | 1197 .. 3003 | [-87.6, +25.2] webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech --profiles lte) |
| lte-bad | 10 | 120/120 | 976 | 1330 | 5959 | 1102 .. 3304 | [-96.9, +35.1] webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech --profiles lte-bad) |

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts).

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 48/48 | 100% .. 100% | -31 | 294 | 452 | [-71.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in) |
| clean | backchannel | 10 | 18/21 | 50% .. 100% | -139 | 260 | 1142 | [-71.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in) |
| clean | cough | 10 | 0/21 | 0% .. 0% | - | - | - | [-71.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in) |
| lte | interrupt | 10 | 50/51 | 86% .. 100% | 212 | 409 | 890 | [-72.1, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in --profiles lte) |
| lte | backchannel | 10 | 21/25 | 50% .. 100% | 196 | 315 | 580 | [-72.1, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in --profiles lte) |
| lte | cough | 10 | 0/24 | 0% .. 0% | - | - | - | [-72.1, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in --profiles lte) |
| lte-bad | interrupt | 10 | 49/51 | 80% .. 100% | 216 | 424 | 872 | [-118.8, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in --profiles lte-bad) |
| lte-bad | backchannel | 10 | 20/25 | 33% .. 100% | -487 | 359 | 679 | [-118.8, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in --profiles lte-bad) |
| lte-bad | cough | 10 | 0/24 | 0% .. 0% | - | - | - | [-118.8, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in --profiles lte-bad) |
