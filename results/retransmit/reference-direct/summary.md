### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| invite-retransmit | good | pass | pass | INVITE to the 2xx: 3079.4 ms (-0.4/+0.4)<br>INVITE copy to the agent's response: 0.2 ms (-0.4/+0.4) | - | - |
| invite-retransmit | rejects | fail | fail | INVITE to the 2xx: 3131.8 ms (-0.4/+0.4)<br>INVITE copy to the agent's response: 0.3 ms (-0.4/+0.4) | one final response to the INVITE (503 Service Unavailable without a To-tag, then 200 OK) | - |
| invite-retransmit | ignores | fail | fail | INVITE to the 2xx: 3064.6 ms (-0.4/+0.4)<br>INVITE copy to the agent's response: 2563.7 ms (-0.4/+0.4) | INVITE copy answered within 1000 ms (200 OK after 2564 ms) | - |
| refer-lost | good | pass | pass | end of the request to REFER: 1300.8 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 0.3 ms (-0.4/+0.4)<br>REFER to its copy: 503.2 ms (-0.4/+0.4) | - | - |
| refer-lost | once | fail | fail | end of the request to REFER: 1301.2 ms (-17.0/+17.0) | agent hangs up within 10 s; REFER resent within 1000 ms (timer E) (none; nor did the agent speak again after its timer F) | - |
| bye-lost | good | pass | pass | BYE to its copy: 502.6 ms (-0.4/+0.4) | - | - |
| bye-lost | once | fail | fail | - | BYE resent within 1000 ms (timer E) (none) | - |

Every case proven over 1 repeat(s): good passes, bad fails.

Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)

Wall-clock steps during the run: none.

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 3 | 0.1 [0.1, 0.1] | 0.02 [0.02, 0.02] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.
