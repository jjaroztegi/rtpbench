### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 695.4 [686.0, 819.0] ms (-63.6/-1.0) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.6 [1.5, 3.1] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: -13.4 [-16.9, -1.6] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 10 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 2.2 [2.1, 2.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.4 [2.1, 2.7] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.2 [1.9, 2.7] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.4 [2.0, 2.7] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.2 [1.1, 1.5] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 5990.5 [5986.7, 6011.6] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2.7 [2.1, 8.1] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 6006.1 [5989.2, 6018.9] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 3 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.4 [2.1, 5.8] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13738.8 [13697.6, 13764.1] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1568.4 [1565.4, 1569.0] ms (-44.6/+3.2) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1542.5 [1540.0, 1547.6] ms (-44.6/+3.2) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.2 [1.9, 3.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1542.8 [1540.5, 1548.9] ms (-44.6/+3.2) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.8 [1.7, 2.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1542.1 [1541.4, 1547.6] ms (-44.6/+3.2) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1543.0 [1541.0, 1549.2] ms (-44.6/+3.2) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1542.8 [1540.2, 1545.2] ms (-44.6/+3.2) n=10 | - |
| late-offer | pass 10/10 | end of the question to agent speech: 1543.8 [1541.0, 1547.5] ms (-44.6/+3.2) n=10 | - |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 730.3 [724.0, 732.7] ms (-67.6/+0.8) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.6 [1.5, 1.7] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 29.4 [20.0, 40.8] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 6 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 2.3 [2.0, 2.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.2 [1.8, 2.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.1 [1.9, 2.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.2 [1.9, 2.7] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.2 [1.0, 1.3] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 6044.8 [6030.3, 6073.2] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2.6 [2.3, 3.8] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 6048.3 [6040.5, 6064.2] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 2 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.2 [2.1, 2.7] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13753.2 [13694.8, 13765.3] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1656.3 [1645.4, 1667.6] ms (-43.3/+3.6) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1626.9 [1616.7, 1634.5] ms (-43.3/+3.6) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.2 [1.8, 5.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1622.8 [1609.2, 1636.1] ms (-43.3/+3.6) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.8 [1.5, 2.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1626.2 [1615.5, 1632.0] ms (-43.3/+3.6) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1621.9 [1617.5, 1662.3] ms (-43.3/+3.6) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1622.0 [1615.7, 1627.9] ms (-43.3/+3.6) n=10 | - |
| late-offer | pass 10/10 | end of the question to agent speech: 1621.2 [1613.8, 1628.8] ms (-43.3/+3.6) n=10 | - |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 721.8 [692.4, 785.6] ms (-109.8/+11.4) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.8 [1.4, 3.0] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 23.4 [-59.1, 60.9] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 6 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 2.3 [1.9, 2.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.3 [1.8, 2.7] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.5 [2.0, 5.2] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.3 [2.1, 6.6] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.2 [1.0, 1.6] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 6057.0 [6036.6, 6114.6] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2.6 [2.2, 4.5] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 6059.7 [6012.3, 6093.3] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 2 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 2.3 [2.0, 3.0] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13750.5 [13698.8, 13790.5] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1675.2 [1634.9, 1724.6] ms (-60.9/+15.5) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1645.5 [1578.1, 1664.6] ms (-60.9/+15.5) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.1 [2.0, 3.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1639.0 [1576.9, 1693.2] ms (-60.9/+15.5) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 1.8 [1.4, 2.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1633.6 [1594.3, 1669.3] ms (-60.9/+15.5) n=10 | - |
| compact-headers | pass 10/10 | end of the question to agent speech: 1618.6 [1532.5, 1686.4] ms (-60.9/+15.5) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1648.8 [1564.8, 1736.5] ms (-60.9/+15.5) n=10 | - |
| late-offer | pass 10/10 | end of the question to agent speech: 1634.8 [1553.3, 1693.7] ms (-60.9/+15.5) n=10 | - |


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
| clean | 10 | 695 [686, 819] | 155 [145, 197] | 501 [501, 502] | 40 [38, 121] |
| lte | 10 | 730 [724, 733] | 149 [147, 153] | 501 [501, 502] | 78 [76, 83] |
| lte-bad | 10 | 719 [692, 786] | 149 [145, 159] | 501 [500, 502] | 58 [39, 138] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 150 | 208.3 [41.2, 849.6] | 1.47 [0.94, 2.52] |
| lte | 150 | 245.1 [94.0, 836.2] | 4.25 [3.17, 5.23] |
| lte-bad | 146 | 288.9 [132.1, 916.1] | 19.79 [14.18, 22.88] |

Pauses: where the agent stopped sending RTP for a second or more and went on with the same stream, outside a hold (silence suppression, RFC 3551 4.1), median [min, max]: per call; how far the RTP clock fell behind across each, ms (the pause less what the timestamps advanced: 0 if they kept time, as RFC 3550 5.1 requires); and how many packets after one carry the marker bit, as 4.1 asks. A carrier that hangs up on RTP inactivity may hang up on these.

| profile | calls | pauses | clock behind | marker |
| --- | --- | --- | --- | --- |
| clean | 150 | 1 [0, 2] | 5695 [5620, 31020] | 0/110 |
| lte | 150 | 1 [0, 2] | 5762 [5687, 31038] | 0/110 |
| lte-bad | 150 | 1 [0, 2] | 5793 [5545, 31061] | 0/110 |
