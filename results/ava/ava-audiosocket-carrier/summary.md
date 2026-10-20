### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 693.2 [681.7, 810.4] ms (-63.6/-1.0) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.8 [1.4, 3.8] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: -14.2 [-35.2, 2.2] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 12 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 2.2 [1.9, 2.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.3 [2.0, 3.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.5 [1.9, 3.2] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.2 [2.0, 2.7] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.2 [1.1, 1.6] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 5898.3 [5878.2, 5919.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2.6 [2.2, 4.1] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 5890.4 [5877.1, 5922.0] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 4 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.2 [2.0, 3.0] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13258.0 [13230.9, 13285.6] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1568.5 [1565.0, 1574.1] ms (-44.6/+3.2) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1543.4 [1539.8, 1551.2] ms (-44.6/+3.2) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.4 [2.0, 3.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1542.6 [1538.0, 1564.8] ms (-44.6/+3.2) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 2.0 [1.5, 3.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1543.6 [1540.9, 1550.3] ms (-44.6/+3.2) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1542.3 [1540.9, 1548.0] ms (-44.6/+3.2) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1542.3 [1540.7, 1548.2] ms (-44.6/+3.2) n=10 | - |
| late-offer | pass 10/10 | end of the question to agent speech: 1541.8 [1541.1, 1545.6] ms (-44.6/+3.2) n=10 | - |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 725.3 [721.4, 791.6] ms (-67.6/+0.8) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.7 [1.4, 2.8] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 32.0 [22.7, 43.8] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 6 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 2.3 [1.9, 3.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.1 [1.9, 2.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.4 [2.0, 2.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.2 [1.8, 3.1] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.2 [1.0, 1.2] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | flips: pass 9, fail 1 | end of the request to REFER: 5931.8 [5920.5, 6023.8] ms (-17.0/+17.0) n=9<br>final NOTIFY to agent BYE: 2.4 [2.2, 2.9] ms (-0.4/+0.4) n=9 | agent transfers (REFER) (1/10) |
| refer-fail | fail 10/10 | end of the request to REFER: 5937.4 [5915.8, 6057.1] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 2 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.1 [1.9, 4.0] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13248.4 [13222.2, 13296.8] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1649.7 [1645.0, 1668.6] ms (-43.3/+3.6) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1622.4 [1612.7, 1626.2] ms (-43.3/+3.6) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.1 [1.9, 3.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1623.1 [1615.1, 1626.8] ms (-43.3/+3.6) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.7 [1.6, 2.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1622.4 [1618.1, 1628.1] ms (-43.3/+3.6) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1623.5 [1619.5, 1633.5] ms (-43.3/+3.6) n=10 | - |
| sdp-ssrc | flips: pass 9, fail 1 | end of the question to agent speech: 1623.8 [1615.8, 1627.6] ms (-43.3/+3.6) n=9 | agent replies within 10000 ms (1/10) |
| late-offer | pass 10/10 | end of the question to agent speech: 1621.3 [1611.5, 1629.8] ms (-43.3/+3.6) n=10 | - |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 724.4 [681.8, 791.3] ms (-109.8/+11.4) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.6 [1.3, 2.0] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 26.5 [-12.8, 86.6] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 6 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 2.3 [1.9, 2.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.3 [1.9, 2.8] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.3 [2.0, 2.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.2 [1.8, 4.3] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.2 [1.0, 2.1] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | flips: pass 8, fail 2 | end of the request to REFER: 6002.5 [5944.8, 6123.3] ms (-17.0/+17.0) n=8<br>final NOTIFY to agent BYE: 3.0 [2.3, 4.7] ms (-0.4/+0.4) n=8 | agent transfers (REFER) (2/10) |
| refer-fail | fail 10/10 | end of the request to REFER: 5967.7 [5873.8, 6104.1] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 4 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.3 [1.9, 3.2] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13240.9 [13221.6, 13274.1] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | flips: pass 9, fail 1 | end of the question to agent speech: 1667.1 [1614.7, 1690.6] ms (-60.9/+15.5) n=9 | agent replies within 10000 ms (1/10) |
| ssrc-change | flips: pass 9, fail 1 | end of the question to agent speech: 1610.8 [1578.3, 1672.3] ms (-60.9/+15.5) n=9 | agent replies within 10000 ms (1/10) |
| reinvite | flips: pass 9, fail 1 | refresh re-INVITE to 2xx: 2.2 [1.8, 2.8] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1628.9 [1599.1, 1710.5] ms (-60.9/+15.5) n=9 | media undisturbed by the refresh (1/10: agent RTP stops 0 ms after the 2xx); agent replies within 10000 ms (1/10) |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.7 [1.4, 2.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1615.2 [1576.1, 1719.0] ms (-60.9/+15.5) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1651.8 [1569.2, 1715.4] ms (-60.9/+15.5) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1636.6 [1582.6, 1689.7] ms (-60.9/+15.5) n=10 | - |
| late-offer | pass 10/10 | end of the question to agent speech: 1637.8 [1551.6, 1716.4] ms (-60.9/+15.5) n=10 | - |


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
| clean | 10 | 693 [682, 810] | 152 [140, 186] | 501 [501, 503] | 41 [39, 123] |
| lte | 10 | 725 [721, 792] | 144 [138, 159] | 501 [501, 501] | 79 [76, 132] |
| lte-bad | 10 | 718 [682, 791] | 145 [142, 157] | 501 [500, 502] | 66 [38, 142] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 150 | 200.4 [41.0, 286.9] | 1.38 [0.90, 2.20] |
| lte | 150 | 204.5 [64.0, 227.8] | 4.08 [2.68, 4.70] |
| lte-bad | 146 | 259.3 [110.8, 318.2] | 19.65 [14.01, 22.14] |

Pauses: where the agent stopped sending RTP for a second or more and went on with the same stream, outside a hold (silence suppression, RFC 3551 4.1), median [min, max]: per call; how far the RTP clock fell behind across each, ms (the pause less what the timestamps advanced: 0 if they kept time, as RFC 3550 5.1 requires); and how many packets after one carry the marker bit, as 4.1 asks. A carrier that hangs up on RTP inactivity may hang up on these.

| profile | calls | pauses | clock behind | marker |
| --- | --- | --- | --- | --- |
| clean | 150 | 1 [0, 2] | 1 [-1, 5722] | 100/110 |
| lte | 150 | 1 [0, 2] | 2 [-9, 5783] | 98/109 |
| lte-bad | 150 | 1 [0, 2] | -4 [-99, 5835] | 94/107 |
