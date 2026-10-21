### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| invite-retransmit | pass 10/10 | INVITE to the 2xx: 343.1 [316.3, 357.5] ms (-0.4/+0.4) n=10<br>INVITE copy to the agent's response: 92.9 [66.0, 106.9] ms (-0.4/+0.4) n=10 | - |
| refer-lost | pass 10/10 | end of the request to REFER: 1649.5 [1643.5, 1660.0] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1000.8 [1000.7, 1001.3] ms (-0.4/+0.4) n=10<br>REFER to its copy: 501.0 [500.5, 501.1] ms (-0.4/+0.4) n=10 | - |
| bye-lost | pass 10/10 | BYE to its copy: 500.9 [500.4, 501.0] ms (-0.4/+0.4) n=10 | - |


Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)

Wall-clock steps during the run: none.

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 30 | 20.7 [0.6, 21.1] | 0.12 [0.07, 0.44] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.
