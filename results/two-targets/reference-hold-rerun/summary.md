### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.5 [0.3, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 109.5 [28.2, 240.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -1.3 [-33.1, 11.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 62.2 [28.9, 136.9] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 2.1 [-9.7, 23.2] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.5 [0.2, 0.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.5 [0.4, 1.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.3, 0.7] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 117 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 118 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.3, 0.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 63.1 [30.7, 110.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -2995.1 [-3032.5, -2985.3] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 0.7] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.5 [0.3, 1.9] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 83.8 [41.8, 116.6] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3001.5 [-3013.4, -2932.3] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0xcb8b0f6d->0xcb8b0f6d, seq 42373->42374, clock -2993 ms); resume from inactive: same RTP stream (10/10: ssrc 0xcb8b0f6d->0xcb8b0f6d, seq 42523->42524, clock -2994 ms) | - |

Every case proven over 10 repeat(s): good passes, bad fails.

Error bars: true value = measured - error, error within

- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
