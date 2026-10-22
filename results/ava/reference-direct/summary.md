### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 830.2 ms (-63.6/-1.0) | - | +29.5 |
| greeting | late | fail | fail | 200 OK to agent speech: 3030.2 ms (-63.6/-1.0) | agent speaks within 2000 ms | +29.5 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 19.5 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 0.3 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2219.1 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 0.3 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 4017.9 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 36.0 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: 0.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 33.3 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -0.0 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (125 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (125 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 36.9 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -3000.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 34.9 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3000.0 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x3968074->0x3968074, seq 36254->36255, clock -3000 ms); resume from inactive: same RTP stream (ssrc 0x3968074->0x3968074, seq 36404->36405, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 829.5 ms (-63.6/-1.0) | - | +29.4 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.2 ms (-0.4/+0.4)<br>digit to agent speech: 828.7 ms (-63.6/-1.0) | - | +28.4 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.2 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| refer | good | pass | pass | end of the request to REFER: 1310.6 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 0.3 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1311.9 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1308.5 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1025.8 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1307.5 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 827.1 ms (-63.6/-1.0) | - | +26.9 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1307.0 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 0 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1309.8 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| codec-pcmu | good | pass | pass | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail | - | answer has PCMU alone (8); agent RTP is PCMU (payload types 8) | - |
| codec-pcma | good | pass | pass | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail | - | answer has PCMA alone (0); agent RTP is PCMA (payload types 0) | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 0.5 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60007.7 ms (-0.4/+0.4) | - | - |
| timer | unsupported | inconclusive | inconclusive | - | Session-Expires in the 2xx (timers not supported (RFC 4028 9, optional; the caller may refresh alone)) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1105.9 ms (-44.6/+3.2) | - | +27.5 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| large-invite | good | pass | pass | end of the question to agent speech: 1105.3 ms (-44.6/+3.2) | - | +27.5 |
| large-invite | udp-only | fail | fail | end of the question to agent speech: 1105.9 ms (-44.6/+3.2) | INVITE over TCP answered 2xx (ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) | +27.5 |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1105.9 ms (-44.6/+3.2) | - | +27.5 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 4 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1095.9 ms (-44.6/+3.2) | - | +17.5 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1105.8 ms (-44.6/+3.2) | 2xx offers the call's codec (no SDP) | +27.5 |
| hold-zero | good | pass | pass | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: 2xx to agent RTP: 36.6 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: RTP clock drift: -0.0 ms (-0.4/+0.4) | - | - |
| hold-zero | ignores-address | fail | fail | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.2 ms (-0.4/+0.4) | c=0.0.0.0 hold: no agent RTP (125 packets) | - |
| codec-change | good | pass | pass | end of the question to agent speech: 1125.9 ms (-64.9/-1.1) | - | +27.5 |
| codec-change | stale | fail | fail | - | answer has PCMA alone (0); agent RTP is PCMA after it (payload types 0); agent replies within 10000 ms | - |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 872.4 ms (-67.6/+0.8) | - | +23.3 |
| greeting | late | fail | fail | 200 OK to agent speech: 3068.0 ms (-67.6/+0.8) | agent speaks within 2000 ms | +30.4 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 61.5 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 0.3 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2198.0 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 0.3 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3974.9 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 78.9 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -0.7 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 70.6 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3.2 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 0.5 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.2 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (120 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (117 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 76.9 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -2993.3 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 78.1 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3003.0 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x18cee4e1->0x18cee4e1, seq 39005->39006, clock -2993 ms); resume from inactive: same RTP stream (ssrc 0x18cee4e1->0x18cee4e1, seq 39155->39156, clock -3003 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 898.5 ms (-67.6/+0.8) | - | +28.1 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.2 ms (-0.4/+0.4)<br>digit to agent speech: 869.6 ms (-67.6/+0.8) | - | +28.8 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.2 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| refer | good | pass | pass | end of the request to REFER: 1351.5 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 0.3 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1352.0 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1354.0 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1027.3 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1349.2 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 863.3 ms (-67.6/+0.8) | - | +21.3 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1350.5 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 0 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1347.4 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| codec-pcmu | good | pass | pass | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail | - | answer has PCMU alone (8); agent RTP is PCMU (payload types 8) | - |
| codec-pcma | good | pass | pass | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail | - | answer has PCMA alone (0); agent RTP is PCMA (payload types 0) | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60013.0 ms (-0.4/+0.4) | - | - |
| timer | unsupported | inconclusive | inconclusive | - | Session-Expires in the 2xx (timers not supported (RFC 4028 9, optional; the caller may refresh alone)) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1183.9 ms (-43.3/+3.6) | - | +23.4 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| large-invite | good | pass | pass | end of the question to agent speech: 1184.0 ms (-43.3/+3.6) | - | +25.4 |
| large-invite | udp-only | fail | fail | end of the question to agent speech: 1185.4 ms (-43.3/+3.6) | INVITE over TCP answered 2xx (ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) | +24.8 |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1175.1 ms (-43.3/+3.6) | - | +15.6 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 54 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1161.8 ms (-43.3/+3.6) | - | +24.9 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 0.7 ms (-0.4/+0.4)<br>end of the question to agent speech: 1208.0 ms (-43.3/+3.6) | 2xx offers the call's codec (no SDP) | +30.4 |
| hold-zero | good | pass | pass | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 1.0 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: 2xx to agent RTP: 81.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: RTP clock drift: 0.5 ms (-0.4/+0.4) | - | - |
| hold-zero | ignores-address | fail | fail | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | c=0.0.0.0 hold: no agent RTP (124 packets) | - |
| codec-change | good | pass | pass | end of the question to agent speech: 1227.6 ms (-67.7/+2.5) | - | +32.4 |
| codec-change | stale | fail | fail | - | answer has PCMA alone (0); agent RTP is PCMA after it (payload types 0); agent replies within 10000 ms | - |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 847.2 ms (-109.8/+11.4) | - | +21.5 |
| greeting | late | fail | fail | 200 OK to agent speech: 3071.3 ms (-109.8/+11.4) | agent speaks within 2000 ms | +9.5 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 16.2 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2202.8 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 0.4 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 4069.9 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 64.3 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -17.1 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 110.7 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -22.1 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (117 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (118 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 59.2 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -2984.7 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 59.4 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3000.0 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x9537f3af->0x9537f3af, seq 58987->58988, clock -2985 ms); resume from inactive: same RTP stream (ssrc 0x9537f3af->0x9537f3af, seq 59137->59138, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 849.5 ms (-109.8/+11.4) | - | +22.0 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.2 ms (-0.4/+0.4)<br>digit to agent speech: 856.6 ms (-109.8/+11.4) | - | +8.0 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.2 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| refer | good | pass | pass | end of the request to REFER: 1351.8 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 0.3 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1368.4 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1375.2 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1041.7 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1396.0 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 878.4 ms (-109.8/+11.4) | - | +31.5 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1349.6 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 0 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1393.4 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| codec-pcmu | good | pass | pass | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail | - | answer has PCMU alone (8); agent RTP is PCMU (payload types 8) | - |
| codec-pcma | good | pass | pass | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail | - | answer has PCMA alone (0); agent RTP is PCMA (payload types 0) | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60013.8 ms (-0.4/+0.4) | - | - |
| timer | unsupported | inconclusive | inconclusive | - | Session-Expires in the 2xx (timers not supported (RFC 4028 9, optional; the caller may refresh alone)) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1346.1 ms (-60.9/+15.5) | - | +67.9 (1/1 outside the bar) |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| large-invite | good | pass | pass | end of the question to agent speech: 1263.0 ms (-60.9/+15.5) | - | -2.5 |
| large-invite | udp-only | fail | fail | end of the question to agent speech: 1292.3 ms (-60.9/+15.5) | INVITE over TCP answered 2xx (ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) | +66.7 (1/1 outside the bar) |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1244.8 ms (-60.9/+15.5) | - | -12.5 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 90 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1275.3 ms (-60.9/+15.5) | - | +40.0 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1206.1 ms (-60.9/+15.5) | 2xx offers the call's codec (no SDP) | +25.7 |
| hold-zero | good | pass | pass | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: 2xx to agent RTP: 54.1 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: RTP clock drift: 6.6 ms (-0.4/+0.4) | - | - |
| hold-zero | ignores-address | fail | fail | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | c=0.0.0.0 hold: no agent RTP (122 packets) | - |
| codec-change | good | pass | pass | end of the question to agent speech: 1182.4 ms (-102.9/+13.1) | - | -12.5 |
| codec-change | stale | fail | fail | - | answer has PCMA alone (0); agent RTP is PCMA after it (payload types 0); agent replies within 10000 ms | - |

Every case proven over 1 repeat(s): good passes, bad fails.

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
| clean | 16 | 0.1 [0.1, 5.1] | 0.01 [0.01, 0.02] |
| lte | 16 | 14.6 [10.4, 18.1] | 3.30 [2.43, 3.64] |
| lte-bad | 16 | 107.2 [77.0, 119.5] | 20.16 [16.23, 21.65] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.
