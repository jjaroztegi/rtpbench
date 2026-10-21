### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| invite-retransmit | pass 10/10 | INVITE to the 2xx: 2.1 [1.8, 2.3] ms (-0.4/+0.4) n=10<br>INVITE copy to the agent's response: 0.2 [0.2, 0.2] ms (-0.4/+0.4) n=10 | - |
| refer-lost | pass 10/10 | end of the request to REFER: 1502.5 [1502.2, 1503.2] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 12.9 [2.9, 21.1] ms (-0.4/+0.4) n=10<br>REFER to its copy: 501.9 [433.2, 557.8] ms (-0.4/+0.4) n=10 | - |
| bye-lost | pass 10/10 | BYE to its copy: 476.6 [436.6, 575.3] ms (-0.4/+0.4) n=10 | - |


Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)

Wall-clock steps during the run: none.

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 20 | 1.1 [0.9, 1.2] | 0.15 [0.06, 0.32] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.
