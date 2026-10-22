### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 541.8 [541.3, 542.5] ms (-64.9/-1.1) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.3 [1.2, 3.1] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 0.4 [-18.7, 1.4] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 3 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.1 [1.9, 2.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.2 [2.0, 3.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 3.4 [-0.1, 4.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.0 [-0.0, 0.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.1 [1.9, 3.1] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.1 [1.9, 2.5] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 16.1 [12.1, 19.1] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.0 [-0.0, 0.0] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.3 [1.2, 1.8] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 501 Not Implemented); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1503.1 [1502.9, 1505.1] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 12.0 [8.0, 14.7] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1503.1 [1502.5, 1506.0] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 517.5 [513.9, 518.6] ms (-11.0/+133.0) n=10 | - |
| timer | inconclusive 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported (RFC 4028 9, optional; the caller may refresh alone)) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1540.2 [1528.7, 1551.9] ms (-11.0/+133.0) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1508.4 [1508.3, 1509.0] ms (-11.0/+133.0) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.9 [1.7, 2.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1508.5 [1508.2, 1509.1] ms (-11.0/+133.0) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| compact-headers | pass 10/10 | end of the question to agent speech: 1508.4 [1508.2, 1509.2] ms (-11.0/+133.0) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1508.3 [1508.2, 1509.3] ms (-11.0/+133.0) n=10 | - |
| late-offer | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 578.4 [562.7, 617.2] ms (-67.7/+2.5) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.3 [1.2, 1.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 35.2 [20.0, 47.4] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 3 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.1 [2.0, 2.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.0 [1.8, 2.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 49.8 [42.7, 55.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.8 [-3.8, 2.7] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.0 [1.8, 2.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.0 [1.9, 2.6] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 47.4 [38.7, 59.2] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.2 [-2.4, 2.1] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.3 [1.1, 1.5] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 501 Not Implemented); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1541.0 [1533.5, 1547.2] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 9.1 [2.3, 19.5] ms (-0.4/+0.4) n=10 | - |
| refer-fail | pass 10/10 | end of the request to REFER: 1544.2 [1517.6, 1546.0] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 562.0 [552.0, 566.1] ms (-14.1/+131.0) n=10 | - |
| timer | inconclusive 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported (RFC 4028 9, optional; the caller may refresh alone)) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1627.5 [1613.5, 1637.3] ms (-14.1/+131.0) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1591.0 [1585.8, 1599.0] ms (-14.1/+131.0) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.9 [1.7, 2.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1587.5 [1583.0, 1594.7] ms (-14.1/+131.0) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| compact-headers | pass 10/10 | end of the question to agent speech: 1594.2 [1584.5, 1625.4] ms (-14.1/+131.0) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1589.4 [1584.6, 1684.9] ms (-14.1/+131.0) n=10 | - |
| late-offer | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 577.9 [532.5, 641.6] ms (-102.9/+13.1) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.5 [1.2, 1.6] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 34.7 [16.7, 88.7] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 3 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.1 [1.8, 2.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.0 [1.8, 2.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 58.1 [27.1, 93.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -4.7 [-15.9, 16.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.1 [1.8, 2.6] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.2 [1.8, 2.6] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 19.5 [-0.0, 73.2] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.3 [-9.6, 19.5] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 1.3 [1.1, 1.5] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 501 Not Implemented); agent reacts within 5000 ms (10/10) |
| refer | flips: pass 9, fail 1 | end of the request to REFER: 1541.4 [1519.8, 1595.2] ms (-17.0/+17.0) n=9<br>final NOTIFY to agent BYE: 8.6 [3.5, 22.5] ms (-0.4/+0.4) n=9 | call completed (1/10: SIP/2.0 500 Server Internal Error) |
| refer-fail | pass 10/10 | end of the request to REFER: 1555.6 [1522.6, 1606.0] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 561.0 [539.1, 597.0] ms (-22.9/+141.5) n=10 | - |
| timer | inconclusive 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported (RFC 4028 9, optional; the caller may refresh alone)) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1654.1 [1623.4, 1680.4] ms (-22.9/+141.5) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1585.6 [1546.9, 1624.1] ms (-22.9/+141.5) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.0 [1.7, 2.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1599.2 [1513.0, 1706.5] ms (-22.9/+141.5) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| compact-headers | pass 10/10 | end of the question to agent speech: 1572.5 [1548.1, 1636.8] ms (-22.9/+141.5) n=10 | - |
| sdp-ssrc | pass 10/10 | end of the question to agent speech: 1611.5 [1572.3, 1658.2] ms (-22.9/+141.5) n=10 | - |
| late-offer | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) |


Error bars: true value = measured - error, error within

- [-141.5, +22.9] ms: webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech, seeds 1-5)
- [-133.0, +11.0] ms: webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech, seeds 1-5)
- [-131.0, +14.1] ms: webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech, seeds 1-5)
- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-13.1, +102.9] ms: webrtcvad first onset, p5..p95, PCMA, lte-bad (calibrate --speech, seeds 1-5)
- [-2.5, +67.7] ms: webrtcvad first onset, p5..p95, PCMA, lte (calibrate --speech, seeds 1-5)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
- [+1.1, +64.9] ms: webrtcvad first onset, p5..p95, PCMA, clean (calibrate --speech, seeds 1-5)

Wall-clock steps during the run: none.

## Turn latency by part


Greeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the target's request for a greeting (negative: asked before answering), the engine's 500 ms, and from its first audio to the agent's speech on the wire (webrtcvad onset bar).

| profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 10 | 542 [541, 543] | 2 [2, 3] | 501 [500, 501] | 39 [38, 40] |
| lte | 10 | 577 [563, 617] | 2 [2, 2] | 501 [500, 501] | 74 [60, 114] |
| lte-bad | 10 | 570 [533, 642] | 2 [2, 4] | 501 [501, 501] | 66 [30, 139] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 140 | 1.1 [0.6, 4.4] | 0.22 [0.02, 0.48] |
| lte | 140 | 15.7 [11.8, 19.8] | 3.32 [2.58, 3.70] |
| lte-bad | 139 | 106.2 [79.4, 141.9] | 20.09 [14.64, 21.78] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.
