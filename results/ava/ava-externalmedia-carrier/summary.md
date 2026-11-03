### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 691.2 [688.7, 802.2] ms (-63.6/-1.0) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.9 [1.4, 2.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: -13.4 [-33.2, -3.2] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 7 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 2.3 [2.0, 2.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.1 [1.9, 2.6] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.3 [1.9, 3.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.3 [2.0, 2.8] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.1 [1.0, 1.3] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 5997.7 [5986.6, 6009.4] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2.9 [2.1, 10.3] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 5997.2 [5987.3, 6027.2] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 3 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.4 [2.0, 5.8] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13747.2 [13710.3, 13780.5] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1567.4 [1565.3, 1573.9] ms (-44.6/+3.2) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1543.6 [1541.2, 1553.2] ms (-44.6/+3.2) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.2 [2.0, 2.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1542.5 [1540.1, 1548.6] ms (-44.6/+3.2) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.7 [1.5, 1.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1542.4 [1541.1, 1545.5] ms (-44.6/+3.2) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1543.9 [1540.9, 1550.8] ms (-44.6/+3.2) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1542.9 [1541.1, 1548.7] ms (-44.6/+3.2) n=10 | - |
| late-offer | pass 10/10 | end of the question to agent speech: 1542.8 [1541.1, 1547.7] ms (-44.6/+3.2) n=10 | - |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 735.5 [725.2, 746.2] ms (-67.6/+0.8) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.6 [1.4, 2.0] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 27.7 [20.9, 37.9] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 5 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 2.4 [2.0, 3.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.2 [1.9, 2.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.3 [1.9, 2.7] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.2 [2.0, 2.5] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.2 [1.1, 1.3] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 6048.2 [6029.1, 6070.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2.5 [2.2, 2.9] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 6044.4 [6030.7, 6066.0] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 2 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.5 [2.1, 3.2] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13750.1 [13728.1, 13796.2] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1652.6 [1648.0, 1669.0] ms (-43.3/+3.6) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1622.6 [1614.1, 1631.2] ms (-43.3/+3.6) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.3 [2.1, 2.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1624.5 [1619.3, 1628.7] ms (-43.3/+3.6) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.8 [1.5, 2.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1624.2 [1616.5, 1630.3] ms (-43.3/+3.6) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1626.9 [1617.6, 1632.3] ms (-43.3/+3.6) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1623.8 [1615.5, 1630.3] ms (-43.3/+3.6) n=10 | - |
| late-offer | pass 10/10 | end of the question to agent speech: 1624.2 [1615.2, 1630.3] ms (-43.3/+3.6) n=10 | - |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 747.5 [729.7, 789.3] ms (-109.8/+11.4) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.7 [1.4, 1.8] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 19.4 [-18.9, 74.7] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 7 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 2.5 [2.1, 2.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.3 [1.9, 2.6] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.3 [2.1, 2.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.3 [2.1, 2.7] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.2 [1.0, 1.5] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 6058.1 [6026.8, 6117.2] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2.8 [2.4, 3.5] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 6057.5 [6025.1, 6098.8] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 2 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.3 [2.1, 2.3] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13737.8 [13715.0, 13764.6] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1681.9 [1615.5, 1709.3] ms (-60.9/+15.5) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1626.7 [1590.5, 1656.9] ms (-60.9/+15.5) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.4 [2.1, 2.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1623.2 [1572.8, 1749.4] ms (-60.9/+15.5) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.8 [1.5, 2.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1636.4 [1610.7, 1784.6] ms (-60.9/+15.5) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1666.4 [1611.8, 1732.7] ms (-60.9/+15.5) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1615.6 [1571.9, 1702.6] ms (-60.9/+15.5) n=10 | - |
| late-offer | pass 10/10 | end of the question to agent speech: 1637.5 [1576.2, 1675.5] ms (-60.9/+15.5) n=10 | - |


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
| clean | 10 | 691 [689, 802] | 150 [147, 182] | 501 [501, 502] | 40 [39, 119] |
| lte | 10 | 735 [725, 746] | 152 [145, 161] | 501 [500, 502] | 81 [79, 85] |
| lte-bad | 10 | 745 [730, 789] | 149 [143, 158] | 501 [501, 501] | 99 [80, 142] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 150 | 191.7 [47.9, 832.7] | 1.36 [0.94, 2.03] |
| lte | 150 | 241.4 [92.4, 837.7] | 4.21 [3.43, 4.92] |
| lte-bad | 147 | 290.4 [112.8, 894.8] | 19.79 [13.78, 22.48] |

Pauses: where the agent stopped sending RTP for a second or more and went on with the same stream, outside a hold (silence suppression, RFC 3551 4.1), median [min, max]: per call; how far the RTP clock fell behind across each, ms (the pause less what the timestamps advanced: 0 if they kept time, as RFC 3550 5.1 requires); and how many packets after one carry the marker bit, as 4.1 asks. A carrier that hangs up on RTP inactivity may hang up on these.

| profile | calls | pauses | clock behind | marker |
| --- | --- | --- | --- | --- |
| clean | 150 | 1 [0, 2] | 5690 [5627, 31038] | 0/110 |
| lte | 150 | 1 [0, 2] | 5755 [5662, 31033] | 0/110 |
| lte-bad | 150 | 1 [0, 2] | 5798 [5658, 31090] | 0/110 |
