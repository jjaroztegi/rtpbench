### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 787.2 [686.3, 990.2] ms (-63.6/-1.0) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: -14.7 [-16.4, -11.5] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 6 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.9 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 1.6 ms (-0.4/+0.4) n=1<br>resume from inactive: RTP clock drift: -0.0 ms (-0.4/+0.4) n=1 | sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: no agent RTP (9/10: 125 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.4 [0.3, 0.7] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 6030.0 [6026.2, 6067.0] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.8, 1.1] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 6029.5 [6009.1, 6048.1] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 0.9 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 12911.2 [12857.4, 13012.7] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1545.6 [1543.4, 1565.0] ms (-44.6/+3.2) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1555.9 [1543.3, 1564.3] ms (-44.6/+3.2) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 1.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1547.5 [1542.9, 1562.7] ms (-44.6/+3.2) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.5 [0.4, 0.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1551.0 [1543.7, 1562.3] ms (-44.6/+3.2) n=10 | - |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.8 [0.7, 1.5] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.6, 0.9] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) |
| codec-change | pass 10/10 | end of the question to agent speech: 1544.9 [1542.3, 1548.4] ms (-64.9/-1.1) n=10 | - |
| refer-lost | pass 10/10 | end of the request to REFER: 6028.4 [6026.2, 6049.0] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>REFER to its copy: 500.1 [499.6, 501.1] ms (-0.4/+0.4) n=10 | - |
| bye-lost | pass 10/10 | BYE to its copy: 499.8 [499.5, 500.6] ms (-0.4/+0.4) n=10 | - |
| invite-retransmit | pass 10/10 | INVITE to the 2xx: 5.5 [4.6, 10.0] ms (-0.4/+0.4) n=10<br>INVITE copy to the agent's response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | - |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 825.0 [727.3, 859.4] ms (-67.6/+0.8) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 25.7 [4.4, 34.0] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 5 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.9 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.8 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.8 [0.7, 1.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 50.7 ms (-0.4/+0.4) n=1<br>resume from inactive: RTP clock drift: 0.5 ms (-0.4/+0.4) n=1 | sendonly hold: no agent RTP (10/10: 124 packets); inactive hold: no agent RTP (9/10: 124 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 6081.0 [5955.9, 6084.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.8, 1.7] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 6081.2 [6057.1, 6103.1] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 0.9 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13003.9 [12919.1, 13038.8] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1637.1 [1623.8, 1646.7] ms (-43.3/+3.6) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1642.3 [1624.7, 1650.3] ms (-43.3/+3.6) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1642.9 [1628.7, 1647.1] ms (-43.3/+3.6) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.6 [0.4, 0.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1641.3 [1622.7, 1654.3] ms (-43.3/+3.6) n=10 | - |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.9 [0.7, 3.3] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.6, 1.1] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) |
| codec-change | pass 10/10 | end of the question to agent speech: 1624.8 [1621.8, 1644.5] ms (-67.7/+2.5) n=10 | - |
| refer-lost | pass 10/10 | end of the request to REFER: 6084.5 [6069.0, 6089.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>REFER to its copy: 500.6 [500.1, 501.0] ms (-0.4/+0.4) n=10 | - |
| bye-lost | pass 10/10 | BYE to its copy: 500.6 [499.7, 500.8] ms (-0.4/+0.4) n=10 | - |
| invite-retransmit | pass 10/10 | INVITE to the 2xx: 5.8 [4.7, 11.0] ms (-0.4/+0.4) n=10<br>INVITE copy to the agent's response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | - |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 798.5 [748.6, 869.4] ms (-109.8/+11.4) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 38.5 [25.1, 72.1] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 5 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.0 [0.8, 3.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.9 [0.8, 1.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10 | sendonly hold: no agent RTP (10/10: 112 packets); inactive hold: no agent RTP (10/10: 120 packets) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 6117.3 [6057.4, 6135.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1.1 [0.9, 2.1] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 6089.6 [6068.1, 6111.6] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 0.9 [0.8, 1.2] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 12951.0 [12912.5, 13019.9] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1639.0 [1595.2, 1704.3] ms (-60.9/+15.5) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1645.2 [1593.1, 1709.0] ms (-60.9/+15.5) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 1.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1651.8 [1608.6, 1692.4] ms (-60.9/+15.5) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.6 [0.5, 0.8] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1618.0 [1587.1, 1681.3] ms (-60.9/+15.5) n=10 | - |
| hold-zero | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.6, 1.2] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 114 packets) |
| codec-change | pass 10/10 | end of the question to agent speech: 1663.8 [1573.0, 1734.3] ms (-102.9/+13.1) n=10 | - |
| refer-lost | pass 10/10 | end of the request to REFER: 6085.2 [6044.4, 6132.4] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.8, 1.6] ms (-0.4/+0.4) n=10<br>REFER to its copy: 500.1 [499.7, 500.8] ms (-0.4/+0.4) n=10 | - |
| bye-lost | pass 10/10 | BYE to its copy: 500.2 [499.7, 501.0] ms (-0.4/+0.4) n=10 | - |
| invite-retransmit | pass 10/10 | INVITE to the 2xx: 6.4 [5.3, 8.9] ms (-0.4/+0.4) n=10<br>INVITE copy to the agent's response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | - |


Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-15.5, +60.9] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5)
- [-13.1, +102.9] ms: webrtcvad first onset, p5..p95, PCMA, lte-bad (calibrate --speech, seeds 1-5)
- [-11.4, +109.8] ms: webrtcvad first onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5)
- [-3.6, +43.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5)
- [-3.2, +44.6] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5)
- [-2.5, +67.7] ms: webrtcvad first onset, p5..p95, PCMA, lte (calibrate --speech, seeds 1-5)
- [-0.8, +67.6] ms: webrtcvad first onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
- [+1.0, +63.6] ms: webrtcvad first onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5)
- [+1.1, +64.9] ms: webrtcvad first onset, p5..p95, PCMA, clean (calibrate --speech, seeds 1-5)

Wall-clock steps during the run: none.

## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | across a clock step | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 10 | 120/120 | 1449 | 1559 | 1580 | 1555 .. 1563 | 0 | [-3.2, +44.6] webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5) |
| lte | 10 | 120/120 | 1525 | 1642 | 1661 | 1631 .. 1650 | 0 | [-3.6, +43.3] webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5) |
| lte-bad | 10 | 120/120 | 1535 | 1657 | 1713 | 1633 .. 1679 | 0 | [-15.5, +60.9] webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5) |

Each turn: a line of PROFILE/REPEAT/latency/turns.jsonl (results.json holds the cases only; rtpbench check gathers the turns into check.json).

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts). Speech ended before (gate): turns left out, the gate having heard the agent's speech end before the onset by more than the bar.

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | across a clock step | speech ended before (gate) | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 0/51 | 0% .. 0% | - | - | - | 0 | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| clean | backchannel | 10 | 0/25 | 0% .. 0% | - | - | - | 0 | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| clean | cough | 10 | 0/24 | 0% .. 0% | - | - | - | 0 | 0 | [-84.8, +0.0] gate stop time, p5..p95, PCMU, clean (calibrate --barge-in, seeds 1-5) |
| lte | interrupt | 10 | 0/51 | 0% .. 0% | - | - | - | 0 | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte | backchannel | 10 | 0/25 | 0% .. 0% | - | - | - | 0 | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte | cough | 10 | 0/24 | 0% .. 0% | - | - | - | 0 | 0 | [-81.9, +0.0] gate stop time, p5..p95, PCMU, lte (calibrate --barge-in, seeds 1-5) |
| lte-bad | interrupt | 10 | 0/51 | 0% .. 0% | - | - | - | 0 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | backchannel | 10 | 0/25 | 0% .. 0% | - | - | - | 0 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | cough | 10 | 0/24 | 0% .. 0% | - | - | - | 0 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |

Per clip: stopped / turns, over the same turns, and those left out as ended before; interruptions are the caller's lines (--lines), backchannels and coughs the corpus's.

| interjection | clip | words | clean | lte | lte-bad |
| --- | --- | --- | --- | --- | --- |
| interrupt | interrupt-00 |  | 0/17 | 0/17 | 0/17 |
| interrupt | interrupt-01 |  | 0/14 | 0/14 | 0/14 |
| interrupt | interrupt-02 |  | 0/12 | 0/12 | 0/12 |
| interrupt | interrupt-03 |  | 0/8 | 0/8 | 0/8 |
| backchannel | tts-ald-bc | Ajá | 0/2 | 0/2 | 0/2 |
| backchannel | tts-cori-bc | Yeah | 0/3 | 0/3 | 0/3 |
| backchannel | tts-davefx-bc | Vale | 0/1 | 0/1 | 0/1 |
| backchannel | tts-libritts0-bc | Okay | 0/4 | 0/4 | 0/4 |
| backchannel | tts-libritts3-bc | Uh-huh | 0/1 | 0/1 | 0/1 |
| backchannel | tts-ljspeech-bc | Uh-huh | 0/6 | 0/6 | 0/6 |
| backchannel | tts-sharvardf-bc | Vale | 0/5 | 0/5 | 0/5 |
| backchannel | tts-sharvardm-bc | Sí, sí | 0/3 | 0/3 | 0/3 |
| cough | cough-c1-1 |  | 0/3 | 0/3 | 0/3 |
| cough | cough-c2-0 |  | 0/3 | 0/3 | 0/3 |
| cough | cough-c2-1 |  | 0/2 | 0/2 | 0/2 |
| cough | cough-man-0 |  | 0/3 | 0/3 | 0/3 |
| cough | cough-man-1 |  | 0/3 | 0/3 | 0/3 |
| cough | cough-short-0 |  | 0/6 | 0/6 | 0/6 |
| cough | cough-short-1 |  | 0/2 | 0/2 | 0/2 |
| cough | cough-woman_three_times-0 |  | 0/2 | 0/2 | 0/2 |

Each turn: a line of PROFILE/REPEAT/barge-in/turns.jsonl (results.json holds the cases only; rtpbench check gathers the turns into check.json).

## Turn latency by part

Turn latency on the mock engine, split where it heard the end of the caller's speech and sent its first audio (one clock with the captures), ms, p50 [p5, p95]: uplink and downlink are the target's; the engine waits 1000 ms of silence and answers 500 ms later by design. Uplink carries the caller's label error (±17 ms), downlink the onset error bar of the profile and codec.

| profile | turns | wire latency | uplink | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 120 | 1559 [1449, 1580] | 1 [-111, 5] | 1501 [1500, 1502] | 60 [51, 78] |
| lte | 120 | 1642 [1525, 1661] | 39 [-71, 48] | 1501 [1501, 1502] | 103 [89, 120] |
| lte-bad | 120 | 1657 [1535, 1713] | 42 [-62, 83] | 1501 [1500, 1502] | 110 [69, 175] |

Greeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the target's request for a greeting (negative: asked before answering), the engine's 500 ms, and from its first audio to the agent's speech on the wire (webrtcvad onset bar).

| profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 10 | 787 [686, 990] | 241 [143, 352] | 501 [501, 501] | 59 [41, 137] |
| lte | 10 | 824 [727, 859] | 240 [142, 267] | 501 [500, 502] | 85 [79, 105] |
| lte-bad | 10 | 789 [749, 869] | 239 [146, 255] | 501 [501, 502] | 80 [48, 137] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 210 | 0.2 [0.1, 20.1] | 0.02 [0.01, 0.13] |
| lte | 210 | 15.8 [9.1, 55.4] | 3.31 [2.53, 3.76] |
| lte-bad | 210 | 107.1 [76.0, 201.7] | 20.25 [16.24, 21.78] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.

## Engine audio as the caller received it

The mock engine's answers as the caller received them (completed answers in the latency and barge-in calls), median [min, max] over answers. Each piece of speech is aligned with what the mock sent; for 24 kHz audio, that is its interpolation through an ideal 8 kHz converter, so the mock's own resampling is not counted. Samples in packets the network lost are left out. unchanged: answers whose aligned speech came through sample for sample (pauses are not compared). distortion: the audio against what no linear filter of ±4 ms explains; a resampler or band filter would leave G.711's own, about 37 dB. moved: answers where a piece came out 5 ms or more later or earlier than the one before (a pause lengthened or shortened, audio inserted or dropped), and the largest move. gain: least squares. 3.4-4 kHz: that band against 300-3400 Hz, relative to what was sent.

| profile | answers | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB |
| --- | --- | --- | --- | --- | --- | --- |
| clean | 199 | 0 | 3.3 [1.1, 8.2] | 199, up to 60 ms | -2.3 [-3.6, -0.7] | -0.1 [-1.2, +1.2] |
| lte | 183 | 0 | 3.6 [-0.3, 13.9] | 183, up to 60 ms | -2.3 [-4.0, -1.0] | -0.2 [-2.2, +1.9] |
| lte-bad | 138 | 0 | 5.3 [0.7, 14.6] | 138, up to 60 ms | -2.6 [-4.3, -0.4] | -0.1 [-2.9, +13.1] |

## Caller audio as the engine received it

The caller's lines in the latency and barge-in calls as the mock engine received them, aligned piece by piece with what the caller sent (its own capture, before the network), median [min, max] over lines; the columns as for the engine's audio above. Lost packets are the target's to fill: what it filled them with counts as distortion, and what it left out as moved. above 4 kHz: energy above 4 kHz against 300-3400 Hz in 24 kHz audio (the caller sends none). full scale: lines with samples at full scale. missing 20 ms: the caller's voiced 20 ms with nothing like them within 25 ms in what the engine got, and what came in their place: silence, the 20 ms before again (repeat), or other (also the next audio, where a packet was left out: see moved). appends: the audio each append carried, the median of each call's.

| profile | lines | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB | above 4 kHz, dB | full scale | missing 20 ms | appends, ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 220 | 0 | 43.3 [41.1, 47.5] | 0 | -0.4 [-0.6, -0.3] | -5.6 [-5.9, -5.2] | -25.2 [-31.0, -22.1] | 0 | 0.0% | 20 [20, 20] |
| lte | 219 | 0 | 42.3 [0.5, 47.5] | 58, up to 60 ms | -0.5 [-4.2, -0.3] | -5.6 [-6.6, -4.8] | -25.1 [-31.0, -21.9] | 0 | 0.3%: 13 silence, 34 other | 20 [20, 20] |
| lte-bad | 163 | 0 | 9.2 [-2.1, 47.5] | 102, up to 60 ms | -1.4 [-6.4, -0.3] | -5.5 [-6.9, -3.8] | -25.4 [-31.5, -21.5] | 0 | 4.2%: 56 silence, 313 other | 20 [20, 20] |
