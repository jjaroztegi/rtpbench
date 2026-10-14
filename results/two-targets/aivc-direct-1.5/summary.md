### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 1231.3 [1101.7, 1641.6] ms (-24.3/+88.1) n=10 | - |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 39931.2 [39842.6, 39957.9] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1514.3 [540.3, 8117.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1729.6 [12.3, 2675.1] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1498.0 [576.6, 2652.1] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 1078.3 [638.2, 1644.1] ms (-24.3/+88.1) n=4 | agent keeps the call for 10 s (10/10: BYE 2657 ms after it); agent speaks within 5000 ms (10/10) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 8, fail 2 | 200 OK to agent speech: 1358.0 [1191.7, 3257.9] ms (-25.2/+87.6) n=9 | agent speaks within 2000 ms (1/10); agent speaks first (1/10) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 39925.3 [39853.8, 39951.5] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 912.8 [596.6, 3039.1] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 17.5 [6.4, 1791.1] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1821.6 [1412.5, 5911.7] ms (-17.0/+17.0) n=9<br>failure NOTIFY to agent speech: 1137.1 [490.6, 1439.4] ms (-25.2/+87.6) n=5 | agent keeps the call for 10 s (9/10: BYE 4 ms after it); agent speaks within 5000 ms (9/10); agent transfers (REFER) (1/10) |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass 10/10 | 200 OK to agent speech: 1228.3 [1171.9, 1455.8] ms (-35.1/+96.9) n=10 | - |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 39912.4 [39835.1, 39943.8] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 487 Request Terminated); agent reacts within 5000 ms (10/10) |
| refer | flips: pass 8, fail 2 | end of the request to REFER: 1624.7 [588.4, 2669.2] ms (-17.0/+17.0) n=8<br>final NOTIFY to agent BYE: 1316.7 [8.5, 2587.2] ms (-0.4/+0.4) n=8 | agent transfers (REFER) (2/10) |
| refer-fail | fail 10/10 | end of the request to REFER: 1449.4 [572.4, 1862.8] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 1043.5 [16.3, 1886.2] ms (-35.1/+96.9) n=8 | agent keeps the call for 10 s (10/10: BYE 2439 ms after it); agent speaks within 5000 ms (10/10) |


Error bars: true value = measured - error, error within

- [-96.9, +35.1] ms: webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech --profiles lte-bad)
- [-88.1, +24.3] ms: webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech)
- [-87.6, +25.2] ms: webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech --profiles lte)
- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)

## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 10 | 120/120 | 522 | 827 | 1274 | 808 .. 892 | [-88.1, +24.3] webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech) |
| lte | 10 | 120/120 | 670 | 901 | 1294 | 852 .. 971 | [-87.6, +25.2] webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech --profiles lte) |
| lte-bad | 10 | 120/120 | 654 | 963 | 1468 | 910 .. 1221 | [-96.9, +35.1] webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech --profiles lte-bad) |

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts).

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 10 | 51/51 | 100% .. 100% | 175 | 312 | 724 | [-71.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in) |
| clean | backchannel | 10 | 18/25 | 33% .. 100% | -173 | 223 | 670 | [-71.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in) |
| clean | cough | 10 | 0/24 | 0% .. 0% | - | - | - | [-71.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in) |
| lte | interrupt | 10 | 50/50 | 100% .. 100% | 216 | 352 | 817 | [-72.1, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in --profiles lte) |
| lte | backchannel | 10 | 15/25 | 0% .. 100% | 87 | 326 | 1141 | [-72.1, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in --profiles lte) |
| lte | cough | 10 | 0/24 | 0% .. 0% | - | - | - | [-72.1, +0.0] gate stop time, p5..p95, PCMA, lte (calibrate --barge-in --profiles lte) |
| lte-bad | interrupt | 10 | 46/46 | 100% .. 100% | 277 | 385 | 832 | [-118.8, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in --profiles lte-bad) |
| lte-bad | backchannel | 10 | 12/22 | 0% .. 100% | 212 | 310 | 1144 | [-118.8, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in --profiles lte-bad) |
| lte-bad | cough | 10 | 0/22 | 0% .. 0% | - | - | - | [-118.8, +0.0] gate stop time, p5..p95, PCMA, lte-bad (calibrate --barge-in --profiles lte-bad) |
