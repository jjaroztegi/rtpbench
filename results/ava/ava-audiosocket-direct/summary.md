### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 689.5 [680.6, 807.1] ms (-63.6/-1.0) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.4 [0.4, 0.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: -14.7 [-18.5, -0.3] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 5 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 0.9 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.8 [0.7, 0.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.8 [0.8, 2.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.8 [0.7, 1.1] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.4 [0.4, 2.5] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 5881.2 [5875.7, 5899.0] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.8, 1.0] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 5880.0 [5877.6, 5899.9] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 0.8 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13255.7 [13236.1, 13289.8] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1541.8 [1540.9, 1545.0] ms (-44.6/+3.2) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1541.4 [1540.7, 1544.1] ms (-44.6/+3.2) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.9 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1542.5 [1541.6, 1543.8] ms (-44.6/+3.2) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.5 [0.5, 0.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1541.5 [1540.9, 1544.6] ms (-44.6/+3.2) n=10 | - |
| hold-zero | inconclusive 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.9 [0.7, 1.3] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10 | resume from c=0.0.0.0: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| codec-change | pass 10/10 | end of the question to agent speech: 1544.1 [1541.1, 1546.0] ms (-64.9/-1.1) n=10 | - |
| refer-lost | pass 10/10 | end of the request to REFER: 5887.9 [5874.6, 5899.5] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.8, 1.2] ms (-0.4/+0.4) n=10<br>REFER to its copy: 500.3 [499.8, 500.8] ms (-0.4/+0.4) n=10 | - |
| bye-lost | pass 10/10 | BYE to its copy: 500.0 [499.7, 500.9] ms (-0.4/+0.4) n=10 | - |
| invite-retransmit | pass 10/10 | INVITE to the 2xx: 5.3 [4.8, 8.4] ms (-0.4/+0.4) n=10<br>INVITE copy to the agent's response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | - |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 730.7 [718.0, 754.8] ms (-67.6/+0.8) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 28.1 [18.3, 41.3] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 4 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 0.9 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.9 [0.7, 2.6] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 5931.5 [5908.3, 5955.9] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1.0 [0.9, 1.3] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 5943.7 [5931.2, 6038.9] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 0.9 [0.7, 1.1] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13271.5 [13229.2, 13282.8] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1622.3 [1616.4, 1629.8] ms (-43.3/+3.6) n=10 | - |
| large-invite | pass 10/10 | end of the question to agent speech: 1624.9 [1612.5, 1633.7] ms (-43.3/+3.6) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1621.1 [1618.3, 1639.7] ms (-43.3/+3.6) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.5 [0.5, 0.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1623.5 [1607.9, 1632.0] ms (-43.3/+3.6) n=10 | - |
| hold-zero | inconclusive 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.9 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.8, 1.2] ms (-0.4/+0.4) n=10 | resume from c=0.0.0.0: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| codec-change | pass 10/10 | end of the question to agent speech: 1621.1 [303.4, 1625.0] ms (-67.7/+2.5) n=10 | - |
| refer-lost | pass 10/10 | end of the request to REFER: 5936.7 [5930.9, 5948.5] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.8 [0.8, 1.2] ms (-0.4/+0.4) n=10<br>REFER to its copy: 500.1 [499.6, 501.1] ms (-0.4/+0.4) n=10 | - |
| bye-lost | pass 10/10 | BYE to its copy: 500.1 [499.4, 500.8] ms (-0.4/+0.4) n=10 | - |
| invite-retransmit | pass 10/10 | INVITE to the 2xx: 5.4 [4.9, 6.4] ms (-0.4/+0.4) n=10<br>INVITE copy to the agent's response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | - |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 750.8 [725.5, 774.8] ms (-109.8/+11.4) n=10 | - |
| bye | pass 10/10 | BYE to its response: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 18.3 [-17.1, 44.9] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 5 ms after the first provisional, before a CANCEL) |
| hold | inconclusive 10/10 | sendonly hold: re-INVITE to 2xx: 1.0 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.9 [0.7, 1.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.8 [0.8, 1.2] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.9 [0.8, 1.1] ms (-0.4/+0.4) n=10 | resume from sendonly: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold); resume from inactive: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| dtmf-rfc4733 | fail 10/10 | - | agent reacts within 5000 ms (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) |
| refer | flips: pass 9, fail 1 | end of the request to REFER: 5965.9 [5922.5, 6107.8] ms (-17.0/+17.0) n=9<br>final NOTIFY to agent BYE: 0.9 [0.8, 1.2] ms (-0.4/+0.4) n=9 | agent transfers (REFER) (1/10) |
| refer-fail | fail 10/10 | end of the request to REFER: 5980.7 [5908.0, 6073.1] ms (-17.0/+17.0) n=9 | agent keeps the call for 10 s (9/10: BYE 1 ms after it); agent speaks within 5000 ms (9/10); agent transfers (REFER) (1/10) |
| codec-pcmu | pass 10/10 | - | - |
| codec-pcma | pass 10/10 | - | - |
| timer | fail 10/10 | refresh re-INVITE to 2xx: 0.9 [0.7, 25.7] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 13252.9 [13227.0, 13288.7] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) |
| ssrc-change | flips: pass 9, fail 1 | end of the question to agent speech: 1651.0 [1607.3, 1730.8] ms (-60.9/+15.5) n=9 | agent replies within 10000 ms (1/10) |
| large-invite | pass 10/10 | end of the question to agent speech: 1613.1 [1580.3, 1676.8] ms (-60.9/+15.5) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1603.6 [1550.7, 1661.1] ms (-60.9/+15.5) n=10 | - |
| reinvite-nosdp | pass 10/10 | refresh re-INVITE to 2xx: 0.5 [0.5, 0.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1667.2 [1578.1, 1695.1] ms (-60.9/+15.5) n=10 | - |
| hold-zero | inconclusive 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 1.0 [0.8, 1.2] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10 | resume from c=0.0.0.0: agent RTP again (10/10: the agent said nothing after the resume, nor for a second before the hold) |
| codec-change | pass 10/10 | end of the question to agent speech: 1612.5 [379.0, 1649.0] ms (-102.9/+13.1) n=10 | - |
| refer-lost | flips: pass 9, fail 1 | end of the request to REFER: 5984.1 [5921.6, 6123.0] ms (-17.0/+17.0) n=9<br>final NOTIFY to agent BYE: 0.9 [0.8, 1.5] ms (-0.4/+0.4) n=9<br>REFER to its copy: 500.3 [499.5, 501.0] ms (-0.4/+0.4) n=9 | agent transfers (REFER) (1/10) |
| bye-lost | flips: pass 9, inconclusive 1 | BYE to its copy: 500.6 [499.7, 501.1] ms (-0.4/+0.4) n=9 | agent hangs up (1/10: no BYE from the agent) |
| invite-retransmit | pass 10/10 | INVITE to the 2xx: 5.0 [4.3, 6.9] ms (-0.4/+0.4) n=10<br>INVITE copy to the agent's response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | - |


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
| clean | 10 | 120/120 | 1469 | 1589 | 1594 | 1587 .. 1590 | 0 | [-3.2, +44.6] webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5) |
| lte | 10 | 120/120 | 1547 | 1662 | 1678 | 1658 .. 1667 | 0 | [-3.6, +43.3] webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5) |
| lte-bad | 10 | 119/120 | 1509 | 1652 | 1733 | 1630 .. 1680 | 0 | [-15.5, +60.9] webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5) |

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
| lte-bad | interrupt | 10 | 1/51 | 0% .. 20% | 1394 | 1394 | 1394 | 0 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | backchannel | 10 | 0/25 | 0% .. 0% | - | - | - | 0 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |
| lte-bad | cough | 10 | 0/24 | 0% .. 0% | - | - | - | 0 | 0 | [-104.9, +0.0] gate stop time, p5..p95, PCMU, lte-bad (calibrate --barge-in, seeds 1-5) |

Per clip: stopped / turns, over the same turns, and those left out as ended before; interruptions are the caller's lines (--lines), backchannels and coughs the corpus's.

| interjection | clip | words | clean | lte | lte-bad |
| --- | --- | --- | --- | --- | --- |
| interrupt | interrupt-00 |  | 0/17 | 0/17 | 0/17 |
| interrupt | interrupt-01 |  | 0/14 | 0/14 | 1/14 |
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
| clean | 120 | 1589 [1469, 1594] | 1 [-111, 5] | 1501 [1500, 1502] | 87 [77, 90] |
| lte | 120 | 1662 [1547, 1678] | 40 [-73, 46] | 1501 [1500, 1502] | 123 [98, 133] |
| lte-bad | 118 | 1652 [1510, 1733] | 37 [-73, 89] | 1501 [1501, 1502] | 119 [40, 165] |

Greeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the target's request for a greeting (negative: asked before answering), the engine's 500 ms, and from its first audio to the agent's speech on the wire (webrtcvad onset bar).

| profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 10 | 688 [681, 807] | 144 [139, 188] | 501 [500, 501] | 41 [39, 118] |
| lte | 10 | 730 [718, 755] | 148 [138, 168] | 501 [500, 501] | 78 [76, 110] |
| lte-bad | 10 | 748 [725, 775] | 146 [139, 191] | 501 [501, 501] | 93 [56, 131] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 203 | 181.3 [40.7, 701.0] | 1.34 [0.72, 2.02] |
| lte | 208 | 191.0 [48.6, 758.7] | 4.10 [2.51, 4.74] |
| lte-bad | 201 | 260.3 [106.2, 807.4] | 19.64 [11.91, 22.39] |

Pauses: where the agent stopped sending RTP for a second or more and went on with the same stream, outside a hold (silence suppression, RFC 3551 4.1), median [min, max]: per call; how far the RTP clock fell behind across each, ms (the pause less what the timestamps advanced: 0 if they kept time, as RFC 3550 5.1 requires); and how many packets after one carry the marker bit, as 4.1 asks. A carrier that hangs up on RTP inactivity may hang up on these.

| profile | calls | pauses | clock behind | marker |
| --- | --- | --- | --- | --- |
| clean | 200 | 1 [0, 12] | 1 [-0, 1] | 330/330 |
| lte | 200 | 1 [0, 12] | 1 [-10, 12] | 328/330 |
| lte-bad | 200 | 1 [0, 12] | -12 [-113, 136] | 300/328 |

## Engine audio as the caller received it

The mock engine's answers as the caller received them (completed answers in the latency and barge-in calls), median [min, max] over answers. Each piece of speech is aligned with what the mock sent; for 24 kHz audio, that is its interpolation through an ideal 8 kHz converter, so the mock's own resampling is not counted. Samples in packets the network lost are left out. unchanged: answers whose aligned speech came through sample for sample (pauses are not compared). distortion: the audio against what no linear filter of ±4 ms explains; a resampler or band filter would leave G.711's own, about 37 dB. moved: answers where a piece came out 5 ms or more later or earlier than the one before (a pause lengthened or shortened, audio inserted or dropped), and the largest move. gain: least squares. 3.4-4 kHz: that band against 300-3400 Hz, relative to what was sent.

| profile | answers | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB |
| --- | --- | --- | --- | --- | --- | --- |
| clean | 200 | 0 | 25.6 [25.6, 29.4] | 0 | -0.2 [-0.2, -0.2] | -1.2 [-2.3, -1.2] |
| lte | 199 | 0 | 25.6 [20.1, 36.0] | 3, up to 59 ms | -0.2 [-0.3, -0.2] | -1.9 [-2.6, -1.0] |
| lte-bad | 185 | 0 | 28.1 [18.4, 36.9] | 8, up to 59 ms | -0.2 [-0.3, -0.2] | -2.2 [-2.9, +8.0] |

## Caller audio as the engine received it

The caller's lines in the latency and barge-in calls as the mock engine received them, aligned piece by piece with what the caller sent (its own capture, before the network), median [min, max] over lines; the columns as for the engine's audio above. Lost packets are the target's to fill: what it filled them with counts as distortion, and what it left out as moved. above 4 kHz: energy above 4 kHz against 300-3400 Hz in 24 kHz audio (the caller sends none). full scale: lines with samples at full scale. missing 20 ms: the caller's voiced 20 ms with nothing like them within 25 ms in what the engine got, and what came in their place: silence, the 20 ms before again (repeat), or other (also the next audio, where a packet was left out: see moved). appends: the audio each append carried, the median of each call's.

| profile | lines | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB | above 4 kHz, dB | full scale | missing 20 ms | appends, ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 220 | 0 | 24.9 [15.9, 42.1] | 0 | -0.5 [-0.6, -0.3] | -5.6 [-5.9, -5.2] | -25.2 [-31.0, -22.1] | 0 | 0.1%: 20 silence | 20 [20, 20] |
| lte | 215 | 0 | 22.0 [0.4, 42.7] | 61, up to 60 ms | -0.5 [-4.3, -0.3] | -5.6 [-5.9, -3.4] | -25.2 [-31.1, -22.1] | 0 | 0.7%: 35 silence, 62 other | 20 [20, 20] |
| lte-bad | 171 | 0 | 9.9 [-2.5, 42.8] | 117, up to 60 ms | -1.2 [-5.9, -0.3] | -5.5 [-9.3, -3.3] | -25.4 [-31.1, -21.7] | 0 | 3.5%: 93 silence, 233 other | 20 [20, 20] |
