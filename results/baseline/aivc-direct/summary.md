### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 541.4 [541.2, 542.3] ms (-64.9/-1.1) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 0.2 [-18.8, 0.3] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 2 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.0 [0.9, 1.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.1 [0.9, 1.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 1.9 [0.2, 15.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.0 [-0.1, 0.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.1 [0.9, 2.1] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.0 [0.8, 1.7] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 15.9 [1.3, 19.3] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.0 [-0.0, 0.0] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 40006.2 [40003.7, 40022.2] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1502.7 [1502.5, 1504.9] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 13.7 [7.6, 16.6] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1502.8 [1502.4, 1506.8] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 19 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1508.3 [1508.1, 1511.4] ms (-11.0/+133.0) n=10 | - |
| large-invite | fail 10/10 | end of the question to agent speech: 1508.4 [1508.1, 1508.9] ms (-11.0/+133.0) n=10 | INVITE over TCP answered 2xx (10/10: ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.9 [0.8, 1.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1508.4 [1508.1, 1509.1] ms (-11.0/+133.0) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.8 [0.8, 1.8] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.9 [0.8, 1.4] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) |
| codec-change | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU after it (10/10: payload types 8); agent replies within 10000 ms (10/10) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 578.7 [562.7, 590.5] ms (-67.7/+2.5) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.3 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 23.8 [21.3, 43.1] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 2 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.9 [0.8, 4.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.9 [0.8, 1.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 55.9 [36.8, 72.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.1 [-2.5, 5.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.9 [0.8, 2.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.9 [0.8, 1.6] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 49.7 [47.5, 58.7] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.6 [-3.0, 4.1] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 40016.6 [40011.9, 40018.0] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1544.3 [1539.4, 1548.5] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 7.7 [2.1, 14.2] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1542.5 [1534.8, 1546.2] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 16 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1588.5 [1582.5, 1597.2] ms (-14.1/+131.0) n=10 | - |
| large-invite | fail 10/10 | end of the question to agent speech: 1587.7 [1583.2, 1605.9] ms (-14.1/+131.0) n=10 | INVITE over TCP answered 2xx (10/10: ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1590.9 [1573.8, 1609.5] ms (-14.1/+131.0) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.8 [0.7, 1.1] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.7, 1.8] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) |
| codec-change | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU after it (10/10: payload types 8); agent replies within 10000 ms (10/10) |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 593.0 [553.1, 633.5] ms (-102.9/+13.1) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 25.3 [-0.1, 102.8] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 2 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.9 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.0 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 37.8 [3.3, 98.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 12.0 [-15.0, 30.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.0 [0.8, 1.2] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.0 [0.8, 1.1] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 41.0 [10.4, 117.5] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 1.6 [-30.8, 18.4] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 40012.3 [40006.4, 40017.8] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1548.3 [1525.6, 1577.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 4.9 [1.0, 17.7] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1561.8 [1525.4, 1583.3] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 20 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1619.9 [1556.9, 1703.4] ms (-22.9/+141.5) n=10 | - |
| large-invite | fail 10/10 | end of the question to agent speech: 1584.3 [1540.9, 1626.7] ms (-22.9/+141.5) n=10 | INVITE over TCP answered 2xx (10/10: ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 1.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1591.9 [1559.5, 1649.6] ms (-22.9/+141.5) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.7, 1.1] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 120 packets) |
| codec-change | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU after it (10/10: payload types 8); agent replies within 10000 ms (10/10) |


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

## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | across a clock step | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 10 | 120/120 | 1504 | 1512 | 1524 | 1511 .. 1514 | 0 | [-133.0, +11.0] webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech, seeds 1-5) |
| lte | 10 | 120/120 | 1582 | 1592 | 1606 | 1590 .. 1595 | 0 | [-131.0, +14.1] webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech, seeds 1-5) |
| lte-bad | 10 | 120/120 | 1553 | 1605 | 1663 | 1587 .. 1635 | 0 | [-141.5, +22.9] webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech, seeds 1-5) |

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts).

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | across a clock step | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 51/51 | 100% .. 100% | -246 | 24 | 179 | 0 | [-84.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in, seeds 1-5) |
| clean | backchannel | 10 | 25/25 | 100% .. 100% | -191 | 4 | 150 | 0 | [-84.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in, seeds 1-5) |
| clean | cough | 10 | 24/24 | 100% .. 100% | -266 | -9 | 146 | 0 | [-84.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in, seeds 1-5) |
| lte | interrupt | 10 | 51/51 | 100% .. 100% | -148 | 103 | 243 | 0 | [-77.6, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in, seeds 1-5) |
| lte | backchannel | 10 | 25/25 | 100% .. 100% | -187 | 86 | 207 | 0 | [-77.6, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in, seeds 1-5) |
| lte | cough | 10 | 24/24 | 100% .. 100% | -265 | 74 | 232 | 0 | [-77.6, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in, seeds 1-5) |
| lte-bad | interrupt | 10 | 51/51 | 100% .. 100% | -188 | 128 | 285 | 0 | [-100.7, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | backchannel | 10 | 25/25 | 100% .. 100% | -210 | 72 | 221 | 0 | [-100.7, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | cough | 10 | 24/24 | 100% .. 100% | -241 | 87 | 230 | 0 | [-100.7, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in, seeds 1-5) |

## Turn latency by part

Turn latency on the mock engine, split where it heard the end of the caller's speech and sent its first audio (one clock with the captures), ms, p50 [p5, p95]: uplink and downlink are the target's; the engine waits 1000 ms of silence and answers 500 ms later by design. Uplink carries the caller's label error (±17 ms), downlink the onset error bar of the profile and codec.

| profile | turns | wire latency | uplink | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 120 | 1512 [1504, 1524] | 1 [-2, 4] | 1501 [1501, 1501] | 10 [3, 22] |
| lte | 120 | 1592 [1582, 1606] | 40 [33, 45] | 1501 [1500, 1502] | 51 [43, 62] |
| lte-bad | 120 | 1605 [1553, 1663] | 45 [9, 83] | 1501 [1500, 1502] | 61 [24, 104] |

Greeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the target's request for a greeting (negative: asked before answering), the engine's 500 ms, and from its first audio to the agent's speech on the wire (webrtcvad onset bar).

| profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 10 | 541 [541, 542] | 3 [2, 5] | 501 [500, 501] | 37 [35, 39] |
| lte | 10 | 578 [563, 590] | 2 [2, 3] | 501 [501, 501] | 75 [59, 87] |
| lte-bad | 10 | 591 [553, 633] | 2 [2, 7] | 501 [501, 502] | 88 [45, 129] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 180 | 1.2 [0.3, 3.6] | 0.13 [0.05, 0.45] |
| lte | 180 | 15.9 [11.1, 19.5] | 3.33 [2.26, 3.92] |
| lte-bad | 180 | 106.6 [76.5, 142.4] | 20.13 [13.57, 22.59] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.
