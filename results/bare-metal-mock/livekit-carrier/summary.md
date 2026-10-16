### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 670.4 [616.5, 701.6] ms (-32.9/+3.8) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.0 [0.9, 1.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2.3 [2.2, 4.6] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 1.5 [1.3, 2.3] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.3 [1.1, 1.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.4 [1.2, 2.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.4 [1.2, 1.8] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.4 [1.1, 3.5] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.6 [0.5, 0.7] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1653.8 [1642.6, 1670.1] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1002.4 [1001.8, 1002.8] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1652.8 [1645.4, 1660.6] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 695.3 [663.1, 720.9] ms (-32.9/+3.8) n=10 | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| compact-headers | pass 10/10 | end of the question to agent speech: 1829.0 [1817.0, 1835.7] ms (-32.9/+3.8) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1824.9 [1806.8, 1851.7] ms (-32.9/+3.8) n=10 | - |
| late-offer | fail 10/10 | - | call completed (10/10: SIP/2.0 400 ) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1878.0 [1871.7, 1896.3] ms (-32.9/+3.8) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1827.5 [1813.7, 1836.8] ms (-32.9/+3.8) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.4 [1.2, 2.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1829.5 [1816.1, 1836.0] ms (-32.9/+3.8) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.1 [1.0, 1.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1831.6 [1810.3, 1843.6] ms (-32.9/+3.8) n=10 | - |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 729.7 [704.2, 761.5] ms (-32.3/+3.4) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.9 [0.8, 1.8] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 44.2 [41.1, 51.2] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 1.3 [1.2, 2.6] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.2 [1.1, 2.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.2 [1.1, 2.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.3 [1.1, 2.2] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.3 [1.1, 1.5] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.6 [0.5, 0.7] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1727.6 [1692.2, 1809.4] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1002.0 [1001.4, 1003.2] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1705.1 [1673.3, 1817.0] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 720.3 [697.7, 748.2] ms (-32.3/+3.4) n=10 | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1990.6 [1963.0, 2050.3] ms (-32.3/+3.4) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1943.5 [1887.8, 2032.6] ms (-32.3/+3.4) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.3 [1.1, 1.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1915.1 [1885.0, 2000.0] ms (-32.3/+3.4) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.0 [0.9, 1.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1971.2 [1898.9, 2044.8] ms (-32.3/+3.4) n=10 | - |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 716.5 [695.9, 762.9] ms (-52.5/+16.7) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.0 [0.9, 1.8] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 64.9 [7.6, 96.9] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 1.5 [1.2, 2.1] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.4 [1.1, 3.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.3 [1.1, 1.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.3 [1.1, 1.7] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.3 [1.2, 3.1] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 124 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.6 [0.6, 0.8] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1795.0 [1737.3, 1941.9] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1002.2 [1001.7, 1003.2] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1852.2 [1768.3, 1959.5] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 721.7 [687.9, 783.9] ms (-52.5/+16.7) n=10 | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 2130.9 [2054.1, 2214.3] ms (-52.5/+16.7) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1976.5 [1939.3, 2078.0] ms (-52.5/+16.7) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.4 [1.2, 2.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 2035.5 [1935.6, 2249.0] ms (-52.5/+16.7) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.0 [0.9, 1.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 2038.1 [1925.3, 2183.5] ms (-52.5/+16.7) n=10 | - |


Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-16.7, +52.5] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech --profiles lte-bad)
- [-3.8, +32.9] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech)
- [-3.4, +32.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech --profiles lte)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)

Wall-clock steps during the run: none.

## Turn latency by part


Greeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the target's request for a greeting (negative: asked before answering), the engine's 500 ms, and from its first audio to the agent's speech on the wire (webrtcvad onset bar).

| profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 10 | 669 [617, 702] | -26 [-80, -8] | 501 [500, 501] | 195 [191, 216] |
| lte | 10 | 728 [704, 761] | -10 [-36, -4] | 501 [500, 502] | 241 [221, 273] |
| lte-bad | 10 | 711 [696, 763] | -14 [-38, -7] | 501 [501, 501] | 229 [214, 292] |
