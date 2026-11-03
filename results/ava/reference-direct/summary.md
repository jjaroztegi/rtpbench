### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 830.2 ms (-63.6/-1.0) | - | +29.7 |
| greeting | late | fail | fail | 200 OK to agent speech: 3030.2 ms (-63.6/-1.0) | agent speaks within 2000 ms | +29.5 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 15.6 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2216.2 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 0.3 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3972.2 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 33.5 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: 0.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 30.4 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: 0.0 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (125 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (125 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 0.5 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 32.1 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -3000.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 29.5 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3000.0 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x2fb62380->0x2fb62380, seq 12801->12802, clock -3000 ms); resume from inactive: same RTP stream (ssrc 0x2fb62380->0x2fb62380, seq 12951->12952, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 825.9 ms (-63.6/-1.0) | - | +25.8 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-rfc4733 | no-events | unsupported | unsupported | - | telephone-event negotiated | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.2 ms (-0.4/+0.4)<br>digit to agent speech: 825.0 ms (-63.6/-1.0) | - | +24.6 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.2 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| dtmf-info | declines | unsupported | unsupported | INFO to its response: 0.2 ms (-0.4/+0.4) | INFO answered 2xx (SIP/2.0 405 Method Not Allowed) | - |
| refer | good | pass | pass | end of the request to REFER: 1302.5 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 0.3 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1317.2 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1317.3 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1040.7 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1316.5 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 824.0 ms (-63.6/-1.0) | - | +23.6 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1318.6 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 0 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1300.1 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| codec-pcmu | good | pass | pass | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail | - | answer has PCMU (8); agent RTP is PCMU (payload types 8) | - |
| codec-pcmu | declines | unsupported | unsupported | - | PCMU-only offer answered 2xx (SIP/2.0 488 Not Acceptable Here) | - |
| codec-pcma | good | pass | pass | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail | - | answer has PCMA (0); agent RTP is PCMA (payload types 0) | - |
| codec-pcma | declines | unsupported | unsupported | - | PCMA-only offer answered 2xx (SIP/2.0 488 Not Acceptable Here) | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60006.6 ms (-0.4/+0.4) | - | - |
| timer | unsupported | unsupported | unsupported | - | Session-Expires in the 2xx (timers not supported (RFC 4028 9, optional; the caller may refresh alone)) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1103.0 ms (-44.6/+3.2) | - | +27.5 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| large-invite | good | pass | pass | end of the question to agent speech: 1103.3 ms (-44.6/+3.2) | - | +27.5 |
| large-invite | udp-only | fail | fail | end of the question to agent speech: 1101.7 ms (-44.6/+3.2) | INVITE over TCP answered 2xx (no TCP listener on port 5060 (connection refused); over UDP then: SIP/2.0 200 OK) | +27.5 |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1117.8 ms (-44.6/+3.2) | - | +27.5 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 1.4 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 0 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1102.0 ms (-44.6/+3.2) | - | +27.5 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 0.6 ms (-0.4/+0.4)<br>end of the question to agent speech: 1102.3 ms (-44.6/+3.2) | 2xx offers the call's codec (no SDP) | +27.5 |
| hold-zero | good | pass | pass | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: 2xx to agent RTP: 34.9 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: RTP clock drift: -0.0 ms (-0.4/+0.4) | - | - |
| hold-zero | ignores-address | fail | fail | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4) | c=0.0.0.0 hold: no agent RTP (125 packets) | - |
| codec-change | good | pass | pass | end of the question to agent speech: 1143.0 ms (-64.9/-1.1) | - | +27.5 |
| codec-change | stale | fail | fail | - | answer has PCMA (0); agent RTP is PCMA after it (payload types 0); agent replies within 10000 ms | - |
| codec-change | declines | unsupported | unsupported | end of the question to agent speech: 1102.9 ms (-44.6/+3.2) | PCMA re-INVITE answered 2xx (SIP/2.0 488 Not Acceptable Here) | +27.5 |
| refer-lost | good | pass | pass | end of the request to REFER: 1316.8 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 0.3 ms (-0.4/+0.4)<br>REFER to its copy: 502.8 ms (-0.4/+0.4) | - | - |
| refer-lost | once | fail | fail | end of the request to REFER: 1314.0 ms (-17.0/+17.0) | agent hangs up within 10 s; REFER resent within 1000 ms (timer E) (none; nor did the agent speak again after its timer F) | - |
| bye-lost | good | pass | pass | BYE to its copy: 502.6 ms (-0.4/+0.4) | - | - |
| bye-lost | once | fail | fail | - | BYE resent within 1000 ms (timer E) (none) | - |
| invite-retransmit | good | pass | pass | INVITE to the 2xx: 3163.2 ms (-0.4/+0.4)<br>INVITE copy to the agent's response: 0.3 ms (-0.4/+0.4) | - | - |
| invite-retransmit | rejects | fail | fail | INVITE to the 2xx: 3188.2 ms (-0.4/+0.4)<br>INVITE copy to the agent's response: 0.2 ms (-0.4/+0.4) | one final response to the INVITE (503 Service Unavailable without a To-tag, then 200 OK) | - |
| invite-retransmit | ignores | fail | fail | INVITE to the 2xx: 3160.7 ms (-0.4/+0.4)<br>INVITE copy to the agent's response: 2659.7 ms (-0.4/+0.4) | INVITE copy answered within 1000 ms (200 OK after 2660 ms) | - |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 869.8 ms (-67.6/+0.8) | - | +28.7 |
| greeting | late | fail | fail | 200 OK to agent speech: 3103.0 ms (-67.6/+0.8) | agent speaks within 2000 ms | +63.2 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 59.4 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 0.3 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2214.4 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 0.3 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3975.9 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 0.5 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 74.2 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: 0.3 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 65.5 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -6.8 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (124 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (123 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 75.1 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -2998.5 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 72.4 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3003.3 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x7e09606c->0x7e09606c, seq 56222->56223, clock -2998 ms); resume from inactive: same RTP stream (ssrc 0x7e09606c->0x7e09606c, seq 56372->56373, clock -3003 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 904.8 ms (-67.6/+0.8) | - | +26.6 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-rfc4733 | no-events | unsupported | unsupported | - | telephone-event negotiated | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.2 ms (-0.4/+0.4)<br>digit to agent speech: 958.4 ms (-67.6/+0.8) | - | +120.7 (1/1 outside the bar) |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.2 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| dtmf-info | declines | unsupported | unsupported | INFO to its response: 0.2 ms (-0.4/+0.4) | INFO answered 2xx (SIP/2.0 405 Method Not Allowed) | - |
| refer | good | pass | pass | end of the request to REFER: 1355.8 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 0.3 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1356.6 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1355.8 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1025.5 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1358.5 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 860.7 ms (-67.6/+0.8) | - | +18.5 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1353.5 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 0 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1339.4 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| codec-pcmu | good | pass | pass | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail | - | answer has PCMU (8); agent RTP is PCMU (payload types 8) | - |
| codec-pcmu | declines | unsupported | unsupported | - | PCMU-only offer answered 2xx (SIP/2.0 488 Not Acceptable Here) | - |
| codec-pcma | good | pass | pass | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail | - | answer has PCMA (0); agent RTP is PCMA (payload types 0) | - |
| codec-pcma | declines | unsupported | unsupported | - | PCMA-only offer answered 2xx (SIP/2.0 488 Not Acceptable Here) | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60008.8 ms (-0.4/+0.4) | - | - |
| timer | unsupported | unsupported | unsupported | - | Session-Expires in the 2xx (timers not supported (RFC 4028 9, optional; the caller may refresh alone)) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 0.5 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1173.2 ms (-43.3/+3.6) | - | +19.4 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| large-invite | good | pass | pass | end of the question to agent speech: 1185.6 ms (-43.3/+3.6) | - | +26.8 |
| large-invite | udp-only | fail | fail | end of the question to agent speech: 1179.5 ms (-43.3/+3.6) | INVITE over TCP answered 2xx (no TCP listener on port 5060 (connection refused); over UDP then: SIP/2.0 200 OK) | +23.1 |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1202.4 ms (-43.3/+3.6) | - | +22.5 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 51 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1199.2 ms (-43.3/+3.6) | - | +21.5 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1174.4 ms (-43.3/+3.6) | 2xx offers the call's codec (no SDP) | +16.2 |
| hold-zero | good | pass | pass | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: 2xx to agent RTP: 73.6 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: RTP clock drift: -1.1 ms (-0.4/+0.4) | - | - |
| hold-zero | ignores-address | fail | fail | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | c=0.0.0.0 hold: no agent RTP (125 packets) | - |
| codec-change | good | pass | pass | end of the question to agent speech: 1206.3 ms (-67.7/+2.5) | - | +29.7 |
| codec-change | stale | fail | fail | - | answer has PCMA (0); agent RTP is PCMA after it (payload types 0); agent replies within 10000 ms | - |
| codec-change | declines | unsupported | unsupported | end of the question to agent speech: 1203.8 ms (-43.3/+3.6) | PCMA re-INVITE answered 2xx (SIP/2.0 488 Not Acceptable Here) | +28.9 |
| refer-lost | good | pass | pass | end of the request to REFER: 1334.5 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 0.3 ms (-0.4/+0.4)<br>REFER to its copy: 502.7 ms (-0.4/+0.4) | - | - |
| refer-lost | once | fail | fail | end of the request to REFER: 1354.5 ms (-17.0/+17.0) | agent hangs up within 10 s; REFER resent within 1000 ms (timer E) (none; nor did the agent speak again after its timer F) | - |
| bye-lost | good | pass | pass | BYE to its copy: 502.9 ms (-0.4/+0.4) | - | - |
| bye-lost | once | fail | fail | - | BYE resent within 1000 ms (timer E) (none) | - |
| invite-retransmit | good | pass | pass | INVITE to the 2xx: 3142.2 ms (-0.4/+0.4)<br>INVITE copy to the agent's response: 0.2 ms (-0.4/+0.4) | - | - |
| invite-retransmit | rejects | fail | fail | INVITE to the 2xx: 3124.3 ms (-0.4/+0.4)<br>INVITE copy to the agent's response: 0.2 ms (-0.4/+0.4) | one final response to the INVITE (503 Service Unavailable without a To-tag, then 200 OK) | - |
| invite-retransmit | ignores | fail | fail | INVITE to the 2xx: 3179.7 ms (-0.4/+0.4)<br>INVITE copy to the agent's response: 2678.9 ms (-0.4/+0.4) | INVITE copy answered within 1000 ms (200 OK after 2679 ms) | - |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 868.7 ms (-109.8/+11.4) | - | +18.3 |
| greeting | late | fail | fail | 200 OK to agent speech: 3082.2 ms (-109.8/+11.4) | agent speaks within 2000 ms | +43.2 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 42.4 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 0.3 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2200.5 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 0.3 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3955.3 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 164.5 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -11.4 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 83.1 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: 1.3 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (122 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (115 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 110.1 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -2987.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 54.3 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3008.9 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0xec36f901->0xec36f901, seq 50260->50261, clock -2987 ms); resume from inactive: same RTP stream (ssrc 0xec36f901->0xec36f901, seq 50410->50411, clock -3009 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 915.6 ms (-109.8/+11.4) | - | +71.4 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-rfc4733 | no-events | unsupported | unsupported | - | telephone-event negotiated | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.2 ms (-0.4/+0.4)<br>digit to agent speech: 870.1 ms (-109.8/+11.4) | - | +3.4 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.2 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| dtmf-info | declines | unsupported | unsupported | INFO to its response: 0.2 ms (-0.4/+0.4) | INFO answered 2xx (SIP/2.0 405 Method Not Allowed) | - |
| refer | good | pass | pass | end of the request to REFER: 1375.2 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 0.3 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1377.6 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1335.6 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1025.6 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1358.3 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 901.8 ms (-109.8/+11.4) | - | +70.9 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1391.7 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 0 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1336.9 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| codec-pcmu | good | pass | pass | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail | - | answer has PCMU (8); agent RTP is PCMU (payload types 8) | - |
| codec-pcmu | declines | unsupported | unsupported | - | PCMU-only offer answered 2xx (SIP/2.0 488 Not Acceptable Here) | - |
| codec-pcma | good | pass | pass | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail | - | answer has PCMA (0); agent RTP is PCMA (payload types 0) | - |
| codec-pcma | declines | unsupported | unsupported | - | PCMA-only offer answered 2xx (SIP/2.0 488 Not Acceptable Here) | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60011.0 ms (-0.4/+0.4) | - | - |
| timer | unsupported | unsupported | unsupported | - | Session-Expires in the 2xx (timers not supported (RFC 4028 9, optional; the caller may refresh alone)) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1262.1 ms (-60.9/+15.5) | - | +7.5 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| large-invite | good | pass | pass | end of the question to agent speech: 1230.2 ms (-60.9/+15.5) | - | +15.6 |
| large-invite | udp-only | fail | fail | end of the question to agent speech: 1213.4 ms (-60.9/+15.5) | INVITE over TCP answered 2xx (no TCP listener on port 5060 (connection refused); over UDP then: SIP/2.0 200 OK) | +4.5 |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1186.6 ms (-60.9/+15.5) | - | +19.3 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 0.5 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 39 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1201.8 ms (-60.9/+15.5) | - | -2.5 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1233.4 ms (-60.9/+15.5) | 2xx offers the call's codec (no SDP) | +20.7 |
| hold-zero | good | pass | pass | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: 2xx to agent RTP: 35.7 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: RTP clock drift: 2.0 ms (-0.4/+0.4) | - | - |
| hold-zero | ignores-address | fail | fail | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | c=0.0.0.0 hold: no agent RTP (122 packets) | - |
| codec-change | good | pass | pass | end of the question to agent speech: 1254.9 ms (-102.9/+13.1) | - | +18.9 |
| codec-change | stale | fail | fail | - | answer has PCMA (0); agent RTP is PCMA after it (payload types 0); agent replies within 10000 ms | - |
| codec-change | declines | unsupported | unsupported | end of the question to agent speech: 1333.7 ms (-60.9/+15.5) | PCMA re-INVITE answered 2xx (SIP/2.0 488 Not Acceptable Here) | +89.6 (1/1 outside the bar) |
| refer-lost | good | pass | pass | end of the request to REFER: 1359.0 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 0.3 ms (-0.4/+0.4)<br>REFER to its copy: 502.9 ms (-0.4/+0.4) | - | - |
| refer-lost | once | fail | fail | end of the request to REFER: 1391.9 ms (-17.0/+17.0) | agent hangs up within 10 s; REFER resent within 1000 ms (timer E) (none; nor did the agent speak again after its timer F) | - |
| bye-lost | good | pass | pass | BYE to its copy: 503.3 ms (-0.4/+0.4) | - | - |
| bye-lost | once | fail | fail | - | BYE resent within 1000 ms (timer E) (none) | - |
| invite-retransmit | good | pass | pass | INVITE to the 2xx: 3203.1 ms (-0.4/+0.4)<br>INVITE copy to the agent's response: 0.2 ms (-0.4/+0.4) | - | - |
| invite-retransmit | rejects | fail | fail | INVITE to the 2xx: 3127.7 ms (-0.4/+0.4)<br>INVITE copy to the agent's response: 0.3 ms (-0.4/+0.4) | one final response to the INVITE (503 Service Unavailable without a To-tag, then 200 OK) | - |
| invite-retransmit | ignores | fail | fail | INVITE to the 2xx: 3173.7 ms (-0.4/+0.4)<br>INVITE copy to the agent's response: 2672.8 ms (-0.4/+0.4) | INVITE copy answered within 1000 ms (200 OK after 2673 ms) | - |

Every case proven over 1 repeat(s): good passes, bad fails, a decline is unsupported.

Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-15.5, +60.9] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5)
- [-13.1, +102.9] ms: webrtcvad first onset, p5..p95, PCMA, lte-bad (calibrate --speech, seeds 1-5)
- [-11.4, +109.8] ms: webrtcvad first onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5)
- [-3.6, +43.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5)
- [-3.2, +44.6] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5)
- [-2.5, +67.7] ms: webrtcvad first onset, p5..p95, PCMA, lte (calibrate --speech, seeds 1-5)
- [-0.8, +67.6] ms: webrtcvad first onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
- [+1.0, +63.6] ms: webrtcvad first onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5)
- [+1.1, +64.9] ms: webrtcvad first onset, p5..p95, PCMA, clean (calibrate --speech, seeds 1-5)

Wall-clock steps during the run: none.

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 19 | 0.1 [0.1, 4.2] | 0.01 [0.01, 0.02] |
| lte | 19 | 15.2 [11.3, 25.5] | 3.35 [3.11, 3.74] |
| lte-bad | 19 | 105.2 [92.1, 120.6] | 20.09 [15.76, 22.22] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.
