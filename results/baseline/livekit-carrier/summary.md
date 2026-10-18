### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 689.6 [666.7, 706.1] ms (-63.6/-1.0) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.2 [0.8, 1.8] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2.7 [2.1, 5.6] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 1.6 [1.2, 3.7] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.4 [1.1, 2.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.4 [1.1, 1.7] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.5 [1.1, 1.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.4 [1.2, 1.8] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.6 [0.5, 0.8] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1652.3 [1644.1, 1675.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1002.1 [1001.8, 1002.5] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1655.5 [1648.4, 1670.0] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 698.1 [652.5, 718.8] ms (-44.6/+3.2) n=10 | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1882.5 [1871.7, 1895.1] ms (-44.6/+3.2) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1821.5 [1810.3, 1844.6] ms (-44.6/+3.2) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.3 [1.2, 2.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1829.5 [1816.2, 1846.6] ms (-44.6/+3.2) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.1 [1.0, 1.8] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1824.4 [1817.7, 1843.6] ms (-44.6/+3.2) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1829.9 [1812.5, 1841.9] ms (-44.6/+3.2) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1832.1 [1816.1, 1840.7] ms (-44.6/+3.2) n=10 | - |
| late-offer | fail 10/10 | - | call completed (10/10: SIP/2.0 400 ) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 710.1 [693.7, 766.6] ms (-67.6/+0.8) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.1 [0.9, 2.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 42.2 [40.5, 48.5] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 1.5 [1.2, 4.1] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.4 [1.2, 2.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.4 [1.2, 2.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.3 [1.2, 2.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.5 [1.1, 2.8] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 123 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 124 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.6 [0.6, 0.7] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | flips: pass 9, fail 1 | end of the request to REFER: 1755.2 [1688.6, 1800.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1002.1 [1001.7, 1003.0] ms (-0.4/+0.4) n=9 | agent hangs up within 10 s (1/10) |
| refer-fail | pass 10/10 | end of the request to REFER: 1709.3 [1693.9, 1736.7] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 709.3 [700.2, 750.9] ms (-43.3/+3.6) n=10 | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1987.3 [1931.7, 2113.1] ms (-43.3/+3.6) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1912.3 [1896.4, 2024.7] ms (-43.3/+3.6) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.4 [1.2, 4.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1936.9 [1910.7, 2017.0] ms (-43.3/+3.6) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.1 [1.0, 2.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1955.6 [1905.8, 1998.5] ms (-43.3/+3.6) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1956.6 [1891.0, 2085.4] ms (-43.3/+3.6) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1953.4 [1904.9, 2017.4] ms (-43.3/+3.6) n=10 | - |
| late-offer | fail 10/10 | - | call completed (10/10: SIP/2.0 400 ) |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 754.3 [662.4, 831.1] ms (-109.8/+11.4) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.2 [1.0, 2.6] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 65.4 [-51.1, 102.8] ms (-0.4/+0.4) n=10 | - |
| cancel | pass 10/10 | CANCEL to the INVITE's final response: 1.4 [1.2, 2.7] ms (-0.4/+0.4) n=10 | - |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.6 [1.3, 2.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.5 [1.3, 3.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.4 [1.1, 1.7] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.5 [1.2, 1.8] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 110 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 119 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.6 [0.6, 1.0] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 405 Method Not Allowed); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1792.8 [1739.8, 2010.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1002.3 [1001.9, 1004.2] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1900.6 [1725.8, 2130.2] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 693.7 [678.4, 825.1] ms (-60.9/+15.5) n=10 | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 2144.7 [2021.4, 2234.1] ms (-60.9/+15.5) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 2053.6 [1977.4, 2250.7] ms (-60.9/+15.5) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.6 [1.3, 4.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 2041.2 [1935.7, 2137.7] ms (-60.9/+15.5) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.1 [1.0, 1.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 2050.0 [1950.2, 2148.5] ms (-60.9/+15.5) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 2009.7 [1907.3, 2167.9] ms (-60.9/+15.5) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 2056.8 [1935.2, 2330.5] ms (-60.9/+15.5) n=10 | - |
| late-offer | fail 10/10 | - | call completed (10/10: SIP/2.0 400 ) |


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

## Turn latency by part


Greeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the target's request for a greeting (negative: asked before answering), the engine's 500 ms, and from its first audio to the agent's speech on the wire (webrtcvad onset bar).

| profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 10 | 687 [667, 706] | -16 [-37, -6] | 501 [500, 502] | 203 [195, 218] |
| lte | 10 | 710 [694, 767] | -31 [-52, -7] | 501 [501, 504] | 244 [223, 272] |
| lte-bad | 10 | 748 [662, 831] | -34 [-74, -3] | 501 [501, 502] | 261 [215, 363] |
