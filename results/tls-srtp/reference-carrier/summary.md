### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 829.5 ms (-63.6/-1.0) | - | +29.5 |
| greeting | late | fail | fail | 200 OK to agent speech: 3029.6 ms (-63.6/-1.0) | agent speaks within 2000 ms | +29.5 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 1.6 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 17.3 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 1.4 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2217.4 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 1.3 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3924.8 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (3 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 32.9 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: 0.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.8 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 28.5 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -0.1 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (125 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (125 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 32.9 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -3000.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 28.6 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3000.0 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x4c3943f0->0x4c3943f0, seq 23683->23685, clock -3000 ms); resume from inactive: same RTP stream (ssrc 0x4c3943f0->0x4c3943f0, seq 23833->23835, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 827.6 ms (-63.6/-1.0) | - | +27.3 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-info | good | pass | pass | INFO to its response: 1.2 ms (-0.4/+0.4)<br>digit to agent speech: 826.9 ms (-63.6/-1.0) | - | +25.8 |
| dtmf-info | deaf | fail | fail | INFO to its response: 1.0 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| refer | good | pass | pass | end of the request to REFER: 1311.3 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 2.2 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1312.4 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1309.7 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1029.8 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1311.9 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 820.0 ms (-63.6/-1.0) | - | +19.1 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1310.8 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 2 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1314.5 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60005.2 ms (-0.4/+0.4) | - | - |
| timer | unsupported | fail | fail | - | Session-Expires in the 2xx (timers not supported) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 1.6 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| compact-headers | good | pass | pass | end of the question to agent speech: 1103.5 ms (-44.6/+3.2) | - | +27.5 |
| compact-headers | long-names | fail | fail | - | call completed (SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass | end of the question to agent speech: 1103.7 ms (-44.6/+3.2) | - | +27.5 |
| sdp-ssrc | strict | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass | end of the question to agent speech: 1101.9 ms (-44.6/+3.2) | - | +27.4 |
| late-offer | rejects | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass | end of the question to agent speech: 1183.3 ms (-44.6/+3.2) | - | +27.5 |
| ptime-30 | 20ms-only | fail | fail | - | agent replies within 10000 ms | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1104.0 ms (-44.6/+3.2) | - | +27.5 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 2.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1103.9 ms (-44.6/+3.2) | - | +27.6 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 2.7 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 0 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>end of the question to agent speech: 1103.4 ms (-44.6/+3.2) | - | +27.5 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 1.9 ms (-0.4/+0.4)<br>end of the question to agent speech: 1103.1 ms (-44.6/+3.2) | 2xx offers the call's codec (no SDP) | +27.5 |

Every case proven over 1 repeat(s): good passes, bad fails.

Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-3.2, +44.6] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
- [+1.0, +63.6] ms: webrtcvad first onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5)

Wall-clock steps during the run: none.

SIP over TLS: TLSv1.3 TLS_AES_256_GCM_SHA384 (37 calls)

SRTP: AES_CM_128_HMAC_SHA1_80 (33 calls), none (4 calls)
SRTP packets that did not authenticate: 0

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 15 | 0.2 [0.1, 0.3] | 0.04 [0.02, 0.04] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.
