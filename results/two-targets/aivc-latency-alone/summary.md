
Error bars: true value = measured - error, error within


## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 3 | 36/36 | 724 | 1042 | 1376 | 1012 .. 1085 | [-88.1, +24.3] webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech) |
