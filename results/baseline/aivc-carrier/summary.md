### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 541.7 [541.3, 543.7] ms (-64.9/-1.1) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.4 [1.1, 4.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 0.4 [-19.4, 3.0] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 4 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.0 [1.7, 2.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.1 [1.7, 2.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 1.8 [0.2, 17.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.0 [-0.1, 0.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.1 [1.6, 2.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.2 [1.7, 6.2] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 14.6 [3.0, 16.2] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.0 [-0.1, 0.0] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 30034.5 [29383.3, 30627.6] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 408 Request Timeout); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1503.1 [1502.6, 1503.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 9.2 [7.1, 17.0] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1503.2 [1502.6, 1507.4] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 18 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1550.2 [1531.1, 1553.4] ms (-11.0/+133.0) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1508.6 [1508.3, 1509.2] ms (-11.0/+133.0) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.8 [1.7, 4.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1508.5 [1508.3, 1509.3] ms (-11.0/+133.0) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| compact-headers | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) |
| sdp-ssrc | fail 10/10 | - | call completed (10/10: INVITE timed out) |
| late-offer | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 582.1 [576.7, 589.1] ms (-67.7/+2.5) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.1 [1.1, 2.8] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 24.5 [18.7, 26.3] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 3 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.1 [1.8, 3.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.1 [1.6, 4.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 47.8 [43.0, 61.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.2 [-0.8, 1.2] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.0 [1.7, 4.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.9 [1.8, 2.1] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 49.4 [39.0, 59.8] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.3 [-1.9, 3.4] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 30169.8 [29321.5, 30886.4] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 408 Request Timeout); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1542.7 [1537.4, 1549.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 10.9 [2.0, 21.9] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1541.3 [1537.5, 1546.6] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 13 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1627.5 [1602.7, 1635.5] ms (-14.1/+131.0) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1589.6 [1584.1, 1596.1] ms (-14.1/+131.0) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.8 [1.5, 5.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1592.1 [1582.5, 1598.6] ms (-14.1/+131.0) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| compact-headers | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) |
| sdp-ssrc | fail 10/10 | - | call completed (10/10: INVITE timed out) |
| late-offer | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 579.2 [539.3, 682.5] ms (-102.9/+13.1) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.1 [0.9, 2.0] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 55.9 [32.5, 80.7] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 4 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.9 [1.6, 2.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.2 [1.6, 2.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 57.2 [28.2, 101.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 2.1 [-37.5, 20.3] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.0 [1.7, 5.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.0 [1.7, 2.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 23.1 [-0.0, 88.4] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.2 [-4.2, 15.3] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 30065.7 [29966.4, 30512.2] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 408 Request Timeout); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1557.9 [1511.9, 1575.1] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 12.0 [1.7, 22.0] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1560.0 [1528.4, 1579.2] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 4 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1634.9 [1580.1, 1686.6] ms (-22.9/+141.5) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1601.1 [1576.4, 1694.6] ms (-22.9/+141.5) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.9 [1.5, 2.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1584.5 [1549.2, 1653.8] ms (-22.9/+141.5) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| compact-headers | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) |
| sdp-ssrc | fail 10/10 | - | call completed (10/10: INVITE timed out) |
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
| clean | 10 | 542 [541, 544] | 2 [2, 3] | 501 [500, 501] | 38 [38, 40] |
| lte | 10 | 582 [577, 589] | 2 [2, 15] | 501 [501, 502] | 77 [70, 86] |
| lte-bad | 10 | 576 [539, 682] | 3 [2, 3] | 501 [501, 502] | 73 [35, 179] |
