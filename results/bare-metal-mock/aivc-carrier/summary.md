### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 542.3 [527.5, 543.7] ms (-24.3/+88.1) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.2 [0.9, 2.1] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 0.4 [-19.6, 0.5] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 3 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.5 [1.7, 5.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.1 [1.7, 4.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 3.0 [-0.1, 18.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.0 [-0.7, 0.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.1 [1.7, 3.6] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.1 [1.8, 2.3] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 14.0 [2.3, 19.2] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.0 [-0.4, 0.1] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 29779.1 [29321.8, 30581.8] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 408 Request Timeout); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1503.2 [1502.6, 1507.3] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 15.8 [6.5, 25.1] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1503.6 [1502.8, 1505.1] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 13 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| compact-headers | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) |
| sdp-ssrc | fail 10/10 | - | call completed (10/10: INVITE timed out) |
| late-offer | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1544.4 [1531.3, 1552.9] ms (-24.3/+88.1) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1508.6 [1508.3, 1529.0] ms (-24.3/+88.1) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.1 [1.4, 4.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1508.7 [1507.8, 1528.3] ms (-24.3/+88.1) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 577.8 [566.7, 587.1] ms (-25.2/+87.6) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.1 [0.9, 1.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 37.2 [17.5, 45.5] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 3 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.0 [1.7, 2.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.9 [1.6, 2.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 48.8 [42.1, 57.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.2 [-3.6, 4.3] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.8 [1.6, 2.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.9 [1.6, 2.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 48.3 [43.7, 63.3] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.9 [-3.2, 5.0] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 30022.7 [29390.4, 30757.8] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 408 Request Timeout); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1542.3 [1523.3, 1549.0] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 11.3 [1.6, 19.3] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1543.1 [1516.2, 1550.1] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 4 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1620.0 [1610.8, 1630.7] ms (-25.2/+87.6) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1589.9 [1586.8, 1597.0] ms (-25.2/+87.6) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.8 [1.5, 3.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1590.7 [1584.3, 1606.5] ms (-25.2/+87.6) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 580.9 [543.8, 657.0] ms (-35.1/+96.9) n=10 | - |
| bye | pass 10/10 | BYE to its response: 1.2 [1.0, 1.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 42.9 [4.4, 86.7] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 3 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.9 [1.6, 2.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.9 [1.6, 2.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 47.3 [15.3, 99.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.4 [-4.1, 19.3] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.0 [1.6, 2.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.8 [1.6, 2.2] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 41.1 [4.1, 125.4] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 4.2 [-13.0, 16.4] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 30090.7 [29592.7, 30893.9] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 408 Request Timeout); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1540.2 [1525.0, 1567.5] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 9.7 [3.6, 21.4] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1561.9 [1538.8, 1597.6] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 12 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1635.5 [1579.1, 1698.0] ms (-35.1/+96.9) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1618.0 [1534.3, 1690.9] ms (-35.1/+96.9) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 1.9 [1.4, 2.8] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1598.5 [1517.4, 1657.4] ms (-35.1/+96.9) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |


Error bars: true value = measured - error, error within

- [-96.9, +35.1] ms: webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech --profiles lte-bad)
- [-88.1, +24.3] ms: webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech)
- [-87.6, +25.2] ms: webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech --profiles lte)
- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)

Wall-clock steps during the run: none.

## Turn latency by part


Greeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the target's request for a greeting (negative: asked before answering), the engine's 500 ms, and from its first audio to the agent's speech on the wire (webrtcvad onset bar).

| profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 10 | 542 [527, 544] | 2 [2, 4] | 501 [501, 503] | 38 [23, 40] |
| lte | 10 | 577 [567, 587] | 2 [2, 4] | 501 [501, 502] | 73 [62, 84] |
| lte-bad | 10 | 580 [544, 657] | 2 [2, 3] | 501 [501, 502] | 76 [41, 154] |
