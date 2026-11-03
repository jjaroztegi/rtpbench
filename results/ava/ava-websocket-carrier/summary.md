### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 708.3 [683.3, 1023.6] ms (-63.6/-1.0) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.9 [1.5, 3.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: -14.6 [-16.4, 3.0] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 6 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.2 [2.1, 2.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.1 [2.0, 2.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 5.7 [5.1, 10.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.0 [-20.0, 0.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.3 [2.0, 5.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.2 [2.0, 3.0] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 17.9 [0.2, 19.0] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.5 [-1.0, 0.0] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x60cc361->0x60cc361, seq 49710->49861, clock +0 ms) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.2 [1.0, 1.5] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 6047.6 [6027.2, 6050.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2.7 [2.3, 5.1] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 6028.9 [6026.6, 6046.9] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 3 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.2 [2.0, 3.5] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 12967.7 [12861.2, 13018.5] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1575.1 [1562.4, 1586.8] ms (-44.6/+3.2) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1561.3 [1543.9, 1564.0] ms (-44.6/+3.2) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.2 [2.0, 2.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1554.7 [1543.2, 1561.9] ms (-44.6/+3.2) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.8 [1.6, 2.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1550.2 [1543.3, 1564.2] ms (-44.6/+3.2) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1561.7 [1548.7, 1565.0] ms (-44.6/+3.2) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1561.6 [1545.2, 1562.4] ms (-44.6/+3.2) n=10 | - |
| late-offer | pass 10/10 | end of the question to agent speech: 1561.2 [1543.5, 1563.3] ms (-44.6/+3.2) n=10 | - |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 752.2 [722.5, 852.2] ms (-67.6/+0.8) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.6 [1.4, 1.8] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 27.0 [22.1, 33.7] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 6 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.2 [1.9, 2.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.3 [2.1, 2.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 54.4 [40.6, 59.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.4 [-21.7, 3.2] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.3 [2.1, 2.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.2 [2.0, 2.8] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 48.1 [37.9, 59.6] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.6 [-3.4, 2.1] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x64c6afe3->0x64c6afe3, seq 57926->58077, clock +1 ms) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.2 [1.1, 1.6] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 6082.7 [6067.8, 6104.0] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2.9 [2.2, 5.7] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 6084.5 [6067.6, 6096.6] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 3 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.2 [1.9, 2.6] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 12990.9 [12869.6, 13043.7] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1663.3 [1641.2, 1688.0] ms (-43.3/+3.6) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1645.9 [1627.6, 1649.3] ms (-43.3/+3.6) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.2 [2.0, 3.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1625.1 [1620.2, 1643.8] ms (-43.3/+3.6) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.8 [1.6, 2.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1635.0 [1620.0, 1644.6] ms (-43.3/+3.6) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1638.0 [1620.6, 1644.8] ms (-43.3/+3.6) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1630.1 [1623.2, 1648.6] ms (-43.3/+3.6) n=10 | - |
| late-offer | pass 10/10 | end of the question to agent speech: 1631.3 [1623.0, 1643.5] ms (-43.3/+3.6) n=10 | - |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 788.0 [716.4, 855.2] ms (-109.8/+11.4) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.6 [1.4, 2.1] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 39.8 [-13.2, 59.4] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 6 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.2 [2.0, 2.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.4 [2.0, 3.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 52.5 [13.8, 159.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -33.8 [-52.8, -0.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.4 [2.0, 2.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.3 [2.0, 2.5] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 33.9 [6.5, 90.1] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 4.3 [-0.0, 21.8] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x9438131->0x9438131, seq 53545->53695, clock -40 ms) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.1 [1.0, 1.4] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 6087.2 [6053.5, 6117.4] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2.6 [2.3, 3.1] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 6094.9 [6052.8, 6122.2] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 2 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.4 [2.1, 4.2] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 12985.2 [12871.9, 13046.3] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1681.3 [1624.0, 1778.0] ms (-60.9/+15.5) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1660.0 [1583.6, 1709.5] ms (-60.9/+15.5) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.5 [1.9, 3.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1634.5 [1591.8, 1682.8] ms (-60.9/+15.5) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.8 [1.5, 2.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1671.6 [1628.9, 1711.9] ms (-60.9/+15.5) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1642.8 [1595.1, 1671.4] ms (-60.9/+15.5) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1665.9 [1576.7, 1730.6] ms (-60.9/+15.5) n=10 | - |
| late-offer | pass 10/10 | end of the question to agent speech: 1663.6 [1603.1, 1697.3] ms (-60.9/+15.5) n=10 | - |


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
| clean | 10 | 706 [683, 1024] | 149 [138, 384] | 501 [500, 502] | 47 [40, 138] |
| lte | 10 | 742 [722, 852] | 146 [140, 248] | 501 [501, 504] | 84 [80, 103] |
| lte-bad | 10 | 787 [716, 855] | 153 [141, 250] | 501 [501, 502] | 88 [47, 133] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 150 | 0.3 [0.1, 2.4] | 0.03 [0.02, 0.07] |
| lte | 150 | 15.5 [11.8, 19.5] | 3.29 [2.34, 3.65] |
| lte-bad | 150 | 105.7 [89.0, 121.8] | 20.14 [15.69, 21.97] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.
