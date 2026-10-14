### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 6, fail 4 | 200 OK to agent speech: 1675.0 [1121.8, 4694.2] ms (-32.9/+3.8) n=10 | agent speaks within 2000 ms (4/10) |
| bye | pass 10/10 | BYE to its response: 14.3 [1.8, 132.0] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 41.4 [8.9, 101.6] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 195.0 [1.8, 640.0] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 5.5 [2.1, 70.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 12.5 [2.6, 57.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 9.9 [5.0, 64.1] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 6.3 [3.6, 19.5] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 7.5 [1.7, 19.8] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | flips: pass 9, fail 1 | end of the request to REFER: 3590.7 [1989.5, 6048.1] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1017.1 [1009.4, 1041.5] ms (-0.4/+0.4) n=9 | agent hangs up within 10 s (1/10) |
| refer-fail | flips: pass 8, fail 2 | end of the request to REFER: 2355.9 [1749.1, 4636.0] ms (-17.0/+17.0) n=8<br>failure NOTIFY to agent speech: 345.2 [130.6, 1151.1] ms (-32.9/+3.8) n=8 | agent transfers (REFER) (2/10) |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| compact-headers | pass 10/10 | end of the question to agent speech: 1587.5 [1162.9, 3409.8] ms (-32.9/+3.8) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1459.4 [1285.1, 4374.0] ms (-32.9/+3.8) n=10 | - |
| late-offer | fail 10/10 | - | call completed (10/10: SIP/2.0 400 ) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 2123.2 [1410.9, 6431.0] ms (-32.9/+3.8) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1616.8 [1230.8, 2028.1] ms (-32.9/+3.8) n=10 | - |
| reinvite | flips: pass 9, fail 1 | refresh re-INVITE to 2xx: 9.7 [3.9, 53.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1958.4 [791.3, 10161.1] ms (-32.9/+3.8) n=10 | agent replies within 10000 ms (1/10) |
| reinvite-nosdp | flips: pass 9, fail 1 | refresh re-INVITE to 2xx: 4.1 [2.0, 36.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 2085.8 [1399.8, 7478.8] ms (-32.9/+3.8) n=9 | agent replies within 10000 ms (1/10) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 6, fail 4 | 200 OK to agent speech: 1444.2 [857.3, 3351.1] ms (-32.3/+3.4) n=10 | agent speaks within 2000 ms (4/10) |
| bye | flips: pass 9, inconclusive 1 | BYE to its response: 7.1 [-56.6, 20.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 67.9 [23.9, 94.8] ms (-0.4/+0.4) n=10 | agent was talking at the BYE (1/10) |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 289.8 [1.9, 1041.5] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 7.9 [4.3, 48.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 11.9 [3.7, 88.2] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 6.3 [2.2, 29.1] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 6.9 [3.7, 13.5] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 126 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) |
| dtmf-rfc4733 | flips: fail 7, pass 3 | digit to agent speech: 733.8 [480.8, 3352.4] ms (-32.3/+3.4) n=3 | agent reacts within 5000 ms (7/10) |
| dtmf-info | fail 10/10 | INFO to its response: 2.0 [1.0, 40.8] ms (-0.4/+0.4) n=10<br>digit to agent speech: 1807.6 ms (-32.3/+3.4) n=1 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (9/10) |
| refer | pass 10/10 | end of the request to REFER: 2524.9 [1127.3, 7707.2] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1008.7 [1004.7, 1034.9] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 2737.0 [2124.1, 8707.6] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 556.9 [16.7, 3805.4] ms (-32.3/+3.4) n=10 | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1918.7 [1577.2, 2938.5] ms (-32.3/+3.4) n=10 | - |
| ssrc-change | flips: pass 9, fail 1 | end of the question to agent speech: 1707.4 [80.5, 3343.1] ms (-32.3/+3.4) n=9 | agent replies within 10000 ms (1/10) |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 5.6 [3.0, 44.8] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1770.0 [1334.9, 3449.4] ms (-32.3/+3.4) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 8.7 [1.9, 37.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1742.3 [1379.3, 7246.5] ms (-32.3/+3.4) n=10 | - |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 8, fail 2 | 200 OK to agent speech: 1203.8 [674.9, 2751.6] ms (-52.5/+16.7) n=10 | agent speaks within 2000 ms (2/10) |
| bye | pass 10/10 | BYE to its response: 5.2 [1.2, 15.1] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 72.2 [32.9, 160.4] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 175.4 [3.1, 665.0] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 6.5 [1.7, 102.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 4.6 [2.2, 16.6] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 7.3 [3.1, 12.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 8.6 [1.8, 36.5] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 116 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 110 packets) |
| dtmf-rfc4733 | flips: fail 9, pass 1 | digit to agent speech: 202.7 ms (-52.5/+16.7) n=1 | agent reacts within 5000 ms (9/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.5 [1.2, 40.2] ms (-0.4/+0.4) n=10<br>digit to agent speech: 428.0 ms (-52.5/+16.7) n=1 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (9/10) |
| refer | pass 10/10 | end of the request to REFER: 2993.3 [2136.4, 6773.4] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1029.9 [941.6, 1112.1] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 2792.7 [2009.7, 4930.0] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 378.1 [76.5, 950.5] ms (-52.5/+16.7) n=10 | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1883.3 [1499.9, 4625.5] ms (-52.5/+16.7) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1817.2 [1491.4, 5659.1] ms (-52.5/+16.7) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 9.2 [3.3, 47.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1654.6 [396.7, 4511.4] ms (-52.5/+16.7) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 7.7 [2.0, 33.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1862.6 [1385.9, 4843.7] ms (-52.5/+16.7) n=10 | - |


Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-16.7, +52.5] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech --profiles lte-bad)
- [-3.8, +32.9] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech)
- [-3.4, +32.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech --profiles lte)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
