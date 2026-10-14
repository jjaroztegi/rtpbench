### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1233.1 [1106.0, 1286.6] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.5] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1226.7 [1106.0, 1286.6] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.5] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 1.3] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 0 ms after the 2xx); agent replies within 10000 ms (10/10) | - |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1319.3 [1188.3, 1368.2] ms (-32.3/+3.4) n=10 | - | +10.8 [+0.0, +30.4] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.5 [0.2, 1.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1315.1 [1187.7, 1371.6] ms (-32.3/+3.4) n=10 | - | +10.4 [+0.0, +30.2] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.3 [0.2, 1.4] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 54 ms after the 2xx); agent replies within 10000 ms (10/10) | - |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1343.2 [1222.8, 1403.8] ms (-52.5/+16.7) n=10 | - | +2.2 [-8.7, +60.1] (1/10 outside the bar) |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1323.5 [1206.0, 1447.2] ms (-52.5/+16.7) n=10 | - | -1.2 [-17.0, +99.6] (2/10 outside the bar) |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.3 [0.2, 1.2] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 57 ms after the 2xx); agent replies within 10000 ms (10/10) | - |

Every case proven over 10 repeat(s): good passes, bad fails.

Error bars: true value = measured - error, error within

- [-16.7, +52.5] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech --profiles lte-bad)
- [-3.8, +32.9] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech)
- [-3.4, +32.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech --profiles lte)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
