### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 541.4 [541.1, 542.4] ms (-24.3/+88.1) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.4 [0.3, 1.0] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 0.2 [-19.8, 0.4] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 2 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.1 [0.8, 1.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.0 [0.9, 2.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 3.1 [0.5, 19.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.0 [-0.1, 0.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.0 [0.9, 2.6] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.9 [0.9, 1.2] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 15.3 [0.2, 19.3] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.0 [-0.1, 0.0] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 40006.8 [40004.9, 40008.0] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1502.6 [1502.2, 1503.4] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 12.3 [10.2, 18.9] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1502.8 [1502.3, 1504.1] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 19 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1508.3 [1508.2, 1528.4] ms (-24.3/+88.1) n=10 | - |
| large-invite | fail 10/10 | end of the question to agent speech: 1508.3 [1508.1, 1509.0] ms (-24.3/+88.1) n=10 | INVITE over TCP answered 2xx (10/10: ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 1.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1508.2 [1508.1, 1508.6] ms (-24.3/+88.1) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.7, 1.3] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) |
| codec-change | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU after it (10/10: payload types 8); agent replies within 10000 ms (10/10) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 581.8 [570.8, 584.4] ms (-25.2/+87.6) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 26.1 [20.8, 41.6] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 2 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.0 [0.9, 1.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.9 [0.9, 1.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 52.2 [38.9, 58.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -1.3 [-4.1, 2.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.9 [0.8, 2.2] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.9 [0.9, 1.8] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 46.4 [41.1, 53.0] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.5 [-1.8, 3.4] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 40015.5 [40008.4, 40020.1] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1541.9 [1537.1, 1544.9] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 9.8 [2.1, 20.2] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1542.9 [1536.3, 1547.4] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 19 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1590.0 [1583.5, 1604.1] ms (-25.2/+87.6) n=10 | - |
| large-invite | fail 10/10 | end of the question to agent speech: 1590.1 [1582.5, 1613.1] ms (-25.2/+87.6) n=10 | INVITE over TCP answered 2xx (10/10: ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.8, 1.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1588.1 [1580.3, 1626.5] ms (-25.2/+87.6) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.9 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.9 [0.8, 1.0] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 121 packets) |
| codec-change | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU after it (10/10: payload types 8); agent replies within 10000 ms (10/10) |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 581.6 [558.1, 628.5] ms (-35.1/+96.9) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.3 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 33.1 [-29.5, 67.6] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 3 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.0 [0.8, 1.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.0 [0.8, 1.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 51.6 [25.8, 295.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -6.8 [-11.9, 5.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.0 [0.8, 1.2] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.0 [0.8, 1.3] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 59.7 [11.9, 116.0] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.4 [-11.5, 14.6] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (1/10: ssrc 0x96e795f->0x96e795f, seq 8114->8130, clock -9 ms); inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 40016.1 [40003.2, 40017.1] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1541.0 [1502.2, 1576.3] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 12.0 [3.3, 16.3] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1551.5 [1523.1, 1578.8] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 9 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1605.5 [1566.8, 1649.1] ms (-35.1/+96.9) n=10 | - |
| large-invite | fail 10/10 | end of the question to agent speech: 1602.1 [1571.6, 1643.5] ms (-35.1/+96.9) n=10 | INVITE over TCP answered 2xx (10/10: ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1606.7 [1565.7, 1679.5] ms (-35.1/+96.9) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.9 [0.8, 1.1] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.9 [0.8, 1.9] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 119 packets) |
| codec-change | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU after it (10/10: payload types 8); agent replies within 10000 ms (10/10) |


Error bars: true value = measured - error, error within

- [-96.9, +35.1] ms: webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech --profiles lte-bad)
- [-88.1, +24.3] ms: webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech)
- [-87.6, +25.2] ms: webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech --profiles lte)
- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)

Wall-clock steps during the run: none.

## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | across a clock step | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 10 | 120/120 | 1504 | 1511 | 1517 | 1511 .. 1513 | 0 | [-88.1, +24.3] webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech) |
| lte | 10 | 120/120 | 1581 | 1593 | 1608 | 1591 .. 1595 | 0 | [-87.6, +25.2] webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech --profiles lte) |
| lte-bad | 10 | 120/120 | 1546 | 1604 | 1666 | 1584 .. 1627 | 0 | [-96.9, +35.1] webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech --profiles lte-bad) |

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts).

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | across a clock step | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 51/51 | 100% .. 100% | -245 | 24 | 179 | 0 | [-71.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in) |
| clean | backchannel | 10 | 25/25 | 100% .. 100% | -191 | 21 | 150 | 0 | [-71.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in) |
| clean | cough | 10 | 24/24 | 100% .. 100% | -266 | 6 | 165 | 0 | [-71.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in) |
| lte | interrupt | 10 | 51/51 | 100% .. 100% | -150 | 102 | 254 | 0 | [-72.1, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in --profiles lte) |
| lte | backchannel | 10 | 25/25 | 100% .. 100% | -194 | 96 | 220 | 0 | [-72.1, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in --profiles lte) |
| lte | cough | 10 | 24/24 | 100% .. 100% | -259 | 79 | 235 | 0 | [-72.1, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in --profiles lte) |
| lte-bad | interrupt | 10 | 51/51 | 100% .. 100% | -118 | 132 | 285 | 0 | [-118.8, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in --profiles lte-bad) |
| lte-bad | backchannel | 10 | 25/25 | 100% .. 100% | -219 | 64 | 231 | 0 | [-118.8, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in --profiles lte-bad) |
| lte-bad | cough | 10 | 24/24 | 100% .. 100% | -121 | 88 | 241 | 0 | [-118.8, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in --profiles lte-bad) |

## Turn latency by part

Turn latency on the mock engine, split where it heard the end of the caller's speech and sent its first audio (one clock with the captures), ms, p50 [p5, p95]: uplink and downlink are the target's; the engine waits 1000 ms of silence and answers 500 ms later by design. Uplink carries the caller's label error (±17 ms), downlink the onset error bar of the profile and codec.

| profile | turns | wire latency | uplink | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 120 | 1511 [1504, 1517] | 0 [-2, 4] | 1501 [1501, 1501] | 9 [2, 16] |
| lte | 120 | 1593 [1581, 1608] | 41 [35, 48] | 1501 [1500, 1502] | 51 [40, 63] |
| lte-bad | 120 | 1604 [1546, 1666] | 47 [12, 85] | 1501 [1500, 1502] | 57 [18, 107] |

Greeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the target's request for a greeting (negative: asked before answering), the engine's 500 ms, and from its first audio to the agent's speech on the wire (webrtcvad onset bar).

| profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 10 | 541 [541, 542] | 3 [2, 4] | 501 [501, 501] | 38 [36, 38] |
| lte | 10 | 581 [571, 584] | 2 [2, 4] | 501 [501, 501] | 78 [67, 81] |
| lte-bad | 10 | 580 [558, 629] | 3 [2, 7] | 501 [501, 503] | 75 [54, 125] |
