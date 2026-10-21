### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| invite-retransmit | pass 10/10 | INVITE to the 2xx: 4.9 [4.5, 9.0] ms (-0.4/+0.4) n=10<br>INVITE copy to the agent's response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | - |
| refer-lost | pass 10/10 | end of the request to REFER: 5878.8 [5873.7, 5896.3] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>REFER to its copy: 500.2 [499.6, 500.8] ms (-0.4/+0.4) n=10 | - |
| bye-lost | pass 10/10 | BYE to its copy: 500.5 [499.5, 500.8] ms (-0.4/+0.4) n=10 | - |


Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)

Wall-clock steps during the run: none.

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 30 | 180.9 [81.6, 220.2] | 1.37 [1.03, 1.64] |

Pauses: where the agent stopped sending RTP for a second or more and went on with the same stream, outside a hold (silence suppression, RFC 3551 4.1), median [min, max]: per call; how far the RTP clock fell behind across each, ms (the pause less what the timestamps advanced: 0 if they kept time, as RFC 3550 5.1 requires); and how many packets after one carry the marker bit, as 4.1 asks. A carrier that hangs up on RTP inactivity may hang up on these.

| profile | calls | pauses | clock behind | marker |
| --- | --- | --- | --- | --- |
| clean | 30 | 1 [0, 1] | 0 [0, 1] | 20/20 |
