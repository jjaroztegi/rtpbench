### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 691.0 [683.5, 793.8] ms (-63.6/-1.0) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.7 [1.4, 1.8] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: -7.4 [-15.3, 1.7] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 7 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 2.2 [2.0, 2.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.5 [1.9, 3.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.2 [1.9, 2.8] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.3 [2.0, 2.6] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.1 [1.0, 1.3] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 5883.0 [5874.8, 5900.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2.5 [2.2, 5.3] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 5880.1 [5876.8, 5919.2] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 3 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.3 [1.9, 2.7] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13259.6 [13238.2, 13331.0] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1566.3 [1564.9, 1566.7] ms (-44.6/+3.2) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1542.7 [1540.1, 1543.8] ms (-44.6/+3.2) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.2 [2.0, 2.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1542.1 [1541.1, 1543.7] ms (-44.6/+3.2) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.8 [1.5, 2.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1542.9 [1540.7, 1544.8] ms (-44.6/+3.2) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1541.6 [1540.0, 1548.0] ms (-44.6/+3.2) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1541.8 [1541.0, 1544.6] ms (-44.6/+3.2) n=10 | - |
| late-offer | pass 10/10 | end of the question to agent speech: 1542.0 [1540.8, 1544.6] ms (-44.6/+3.2) n=10 | - |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 728.3 [718.8, 766.9] ms (-67.6/+0.8) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.5 [1.3, 1.9] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 30.1 [3.6, 49.4] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 6 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 2.2 [2.1, 3.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.2 [1.9, 2.7] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.1 [2.0, 2.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.3 [1.9, 2.7] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.1 [1.0, 1.3] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 5937.0 [5928.4, 5957.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2.5 [2.2, 3.0] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 5936.8 [5932.0, 5983.5] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 2 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.2 [2.0, 3.2] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13247.4 [13222.0, 13281.0] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1650.4 [1638.2, 1666.0] ms (-43.3/+3.6) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1623.2 [1615.5, 1630.4] ms (-43.3/+3.6) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.2 [2.0, 2.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1620.5 [1614.4, 1628.3] ms (-43.3/+3.6) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.8 [1.6, 2.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1622.6 [1611.9, 1629.4] ms (-43.3/+3.6) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1626.3 [1617.8, 1631.8] ms (-43.3/+3.6) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1624.1 [1618.2, 1632.9] ms (-43.3/+3.6) n=10 | - |
| late-offer | pass 10/10 | end of the question to agent speech: 1624.0 [1618.4, 1628.3] ms (-43.3/+3.6) n=10 | - |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 751.1 [696.3, 833.1] ms (-109.8/+11.4) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.5 [1.4, 1.9] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 26.7 [-15.4, 68.3] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 7 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 2.4 [2.2, 7.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.4 [2.0, 3.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.5 [2.3, 2.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.5 [2.1, 3.4] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.3 [1.1, 1.6] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | flips: pass 9, fail 1 | end of the request to REFER: 5974.7 [5915.5, 6045.0] ms (-17.0/+17.0) n=9<br>final NOTIFY to agent BYE: 2.6 [2.4, 3.0] ms (-0.4/+0.4) n=9 | agent transfers (REFER) (1/10) |
| refer-fail | fail 10/10 | end of the request to REFER: 5989.8 [5920.3, 6077.0] ms (-17.0/+17.0) n=9 | agent keeps the call for 10 s (9/10: BYE 2 ms after it); agent speaks within 5000 ms (9/10); agent transfers (REFER) (1/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.4 [2.2, 3.4] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13257.7 [13230.9, 13290.9] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1675.6 [1641.7, 1759.5] ms (-60.9/+15.5) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1640.3 [1606.1, 1708.5] ms (-60.9/+15.5) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.5 [2.1, 3.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1627.6 [1579.6, 1678.5] ms (-60.9/+15.5) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 2.0 [1.6, 2.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1619.7 [1584.5, 1682.3] ms (-60.9/+15.5) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1641.4 [1583.8, 1719.6] ms (-60.9/+15.5) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1607.3 [1569.4, 1655.8] ms (-60.9/+15.5) n=10 | - |
| late-offer | flips: pass 9, fail 1 | end of the question to agent speech: 1619.4 [1576.5, 1714.1] ms (-60.9/+15.5) n=9 | agent replies within 10000 ms (1/10) |


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
| clean | 10 | 690 [684, 794] | 142 [141, 172] | 501 [501, 502] | 41 [39, 120] |
| lte | 10 | 728 [719, 767] | 143 [140, 151] | 501 [500, 502] | 83 [77, 122] |
| lte-bad | 10 | 741 [696, 833] | 149 [141, 195] | 501 [501, 502] | 91 [39, 138] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 150 | 182.1 [41.6, 221.6] | 1.33 [0.53, 1.93] |
| lte | 150 | 189.4 [53.1, 214.2] | 4.11 [2.55, 4.69] |
| lte-bad | 141 | 268.8 [124.7, 753.7] | 19.59 [16.88, 21.77] |

Pauses: where the agent stopped sending RTP for a second or more and went on with the same stream, outside a hold (silence suppression, RFC 3551 4.1), median [min, max]: per call; how far the RTP clock fell behind across each, ms (the pause less what the timestamps advanced: 0 if they kept time, as RFC 3550 5.1 requires); and how many packets after one carry the marker bit, as 4.1 asks. A carrier that hangs up on RTP inactivity may hang up on these.

| profile | calls | pauses | clock behind | marker |
| --- | --- | --- | --- | --- |
| clean | 150 | 1 [0, 2] | 1 [0, 5713] | 100/110 |
| lte | 150 | 1 [0, 2] | 2 [-9, 5777] | 100/110 |
| lte-bad | 150 | 1 [0, 2] | -3 [-119, 5840] | 94/109 |
