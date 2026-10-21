### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 830.2 ms (-63.6/-1.0) | - | +29.4 |
| greeting | late | fail | fail | 200 OK to agent speech: 3030.2 ms (-63.6/-1.0) | agent speaks within 2000 ms | +29.5 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 0.3 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 17.9 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2218.0 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 0.4 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3931.3 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (3 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 35.6 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: 0.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.5 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 33.7 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: 0.0 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (125 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (125 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 36.1 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -3000.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 34.3 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3000.0 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x7705b78c->0x7705b78c, seq 39637->39638, clock -3000 ms); resume from inactive: same RTP stream (ssrc 0x7705b78c->0x7705b78c, seq 39787->39788, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 828.0 ms (-63.6/-1.0) | - | +27.9 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.3 ms (-0.4/+0.4)<br>digit to agent speech: 827.4 ms (-63.6/-1.0) | - | +27.0 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.3 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| refer | good | pass | pass | end of the request to REFER: 1314.1 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 0.4 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1315.8 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1311.2 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1024.7 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1311.9 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 821.2 ms (-63.6/-1.0) | - | +20.9 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1310.6 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 41 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1312.1 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| codec-pcmu | good | pass | pass | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail | - | answer has PCMU alone (8); agent RTP is PCMU (payload types 8) | - |
| codec-pcma | good | pass | pass | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail | - | answer has PCMA alone (0); agent RTP is PCMA (payload types 0) | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60006.7 ms (-0.4/+0.4) | - | - |
| timer | unsupported | inconclusive | inconclusive | - | Session-Expires in the 2xx (timers not supported (RFC 4028 9, optional; the caller may refresh alone)) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1104.5 ms (-44.6/+3.2) | - | +27.5 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1104.5 ms (-44.6/+3.2) | - | +27.5 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 3 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1104.2 ms (-44.6/+3.2) | - | +27.5 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1104.3 ms (-44.6/+3.2) | 2xx offers the call's codec (no SDP) | +27.5 |
| hold-zero | good | pass | pass | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: 2xx to agent RTP: 36.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: RTP clock drift: 0.0 ms (-0.4/+0.4) | - | - |
| hold-zero | ignores-address | fail | fail | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4) | c=0.0.0.0 hold: no agent RTP (125 packets) | - |
| codec-change | good | pass | pass | end of the question to agent speech: 1124.6 ms (-64.9/-1.1) | - | +27.5 |
| codec-change | stale | fail | fail | - | answer has PCMA alone (0); agent RTP is PCMA after it (payload types 0); agent replies within 10000 ms | - |

Every case proven over 1 repeat(s): good passes, bad fails.

Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-3.2, +44.6] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
- [+1.0, +63.6] ms: webrtcvad first onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5)
- [+1.1, +64.9] ms: webrtcvad first onset, p5..p95, PCMA, clean (calibrate --speech, seeds 1-5)

Wall-clock steps during the run: none.

SIP over TLS: TLSv1.3 TLS_AES_256_GCM_SHA384 (37 calls)

SRTP: AES_CM_128_HMAC_SHA1_80 (36 calls), none (1 calls)
SRTP packets that did not authenticate: 0

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 15 | 0.1 [0.1, 10.2] | 0.01 [0.01, 0.02] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.
