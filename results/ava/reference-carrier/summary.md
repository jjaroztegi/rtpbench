### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 829.8 ms (-63.6/-1.0) | - | +29.5 |
| greeting | late | fail | fail | 200 OK to agent speech: 3029.9 ms (-63.6/-1.0) | agent speaks within 2000 ms | +29.5 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 1.4 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 15.5 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 1.5 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2214.0 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 1.3 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3977.5 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 31.5 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: 0.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 25.9 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: 0.0 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (125 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (125 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 31.2 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -3000.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 26.7 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3000.0 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x2e230df9->0x2e230df9, seq 24933->24935, clock -3000 ms); resume from inactive: same RTP stream (ssrc 0x2e230df9->0x2e230df9, seq 25083->25085, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 826.6 ms (-63.6/-1.0) | - | +26.3 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-rfc4733 | no-events | unsupported | unsupported | - | telephone-event negotiated | - |
| dtmf-info | good | pass | pass | INFO to its response: 1.0 ms (-0.4/+0.4)<br>digit to agent speech: 825.1 ms (-63.6/-1.0) | - | +23.9 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.9 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| dtmf-info | declines | unsupported | unsupported | INFO to its response: 0.9 ms (-0.4/+0.4) | INFO answered 2xx (SIP/2.0 405 Method Not Allowed) | - |
| refer | good | pass | pass | end of the request to REFER: 1318.1 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 2.4 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1315.6 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1317.7 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1030.1 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1315.7 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 824.8 ms (-63.6/-1.0) | - | +23.8 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1313.2 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 2 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1314.4 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60016.3 ms (-0.4/+0.4) | - | - |
| timer | unsupported | unsupported | unsupported | - | Session-Expires in the 2xx (timers not supported (RFC 4028 9, optional; the caller may refresh alone)) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| compact-headers | good | pass | pass | end of the question to agent speech: 1101.7 ms (-44.6/+3.2) | - | +27.5 |
| compact-headers | long-names | fail | fail | - | call completed (SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass | end of the question to agent speech: 1102.4 ms (-44.6/+3.2) | - | +27.5 |
| sdp-ssrc | strict | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass | end of the question to agent speech: 1102.8 ms (-44.6/+3.2) | - | +27.5 |
| late-offer | rejects | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass | end of the question to agent speech: 1162.2 ms (-44.6/+3.2) | - | +27.5 |
| ptime-30 | 20ms-only | fail | fail | - | agent replies within 10000 ms | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1102.8 ms (-44.6/+3.2) | - | +27.5 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>end of the question to agent speech: 1102.7 ms (-44.6/+3.2) | - | +27.5 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 1.4 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 19 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1102.4 ms (-44.6/+3.2) | - | +27.5 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 1.1 ms (-0.4/+0.4)<br>end of the question to agent speech: 1102.0 ms (-44.6/+3.2) | 2xx offers the call's codec (no SDP) | +27.5 |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 875.0 ms (-67.6/+0.8) | - | +32.7 |
| greeting | late | fail | fail | 200 OK to agent speech: 3072.3 ms (-67.6/+0.8) | agent speaks within 2000 ms | +32.8 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 1.6 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 55.5 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 1.5 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2214.5 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 0.9 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3957.9 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 1.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 68.5 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: 0.3 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 72.7 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: 4.5 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (125 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (125 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 67.7 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -3000.8 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 62.4 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -2994.7 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x41ae6938->0x41ae6938, seq 47003->47005, clock -3001 ms); resume from inactive: same RTP stream (ssrc 0x41ae6938->0x41ae6938, seq 47153->47155, clock -2995 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 910.1 ms (-67.6/+0.8) | - | +34.6 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-rfc4733 | no-events | unsupported | unsupported | - | telephone-event negotiated | - |
| dtmf-info | good | pass | pass | INFO to its response: 1.1 ms (-0.4/+0.4)<br>digit to agent speech: 865.7 ms (-67.6/+0.8) | - | +23.0 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.9 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| dtmf-info | declines | unsupported | unsupported | INFO to its response: 0.8 ms (-0.4/+0.4) | INFO answered 2xx (SIP/2.0 405 Method Not Allowed) | - |
| refer | good | pass | pass | end of the request to REFER: 1356.8 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 1.5 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1356.3 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1357.2 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1031.6 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1358.5 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 865.8 ms (-67.6/+0.8) | - | +23.1 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1355.1 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 2 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1356.1 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60017.3 ms (-0.4/+0.4) | - | - |
| timer | unsupported | unsupported | unsupported | - | Session-Expires in the 2xx (timers not supported (RFC 4028 9, optional; the caller may refresh alone)) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| compact-headers | good | pass | pass | end of the question to agent speech: 1181.5 ms (-43.3/+3.6) | - | +28.6 |
| compact-headers | long-names | fail | fail | - | call completed (SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass | end of the question to agent speech: 1171.2 ms (-43.3/+3.6) | - | +9.9 |
| sdp-ssrc | strict | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass | end of the question to agent speech: 1184.6 ms (-43.3/+3.6) | - | +31.6 |
| late-offer | rejects | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass | end of the question to agent speech: 1245.8 ms (-43.3/+3.6) | - | +32.8 |
| ptime-30 | 20ms-only | fail | fail | - | agent replies within 10000 ms | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1184.7 ms (-43.3/+3.6) | - | +29.9 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>end of the question to agent speech: 1182.5 ms (-43.3/+3.6) | - | +23.4 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 52 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 1.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1177.8 ms (-43.3/+3.6) | - | +20.6 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 1.0 ms (-0.4/+0.4)<br>end of the question to agent speech: 1201.3 ms (-43.3/+3.6) | 2xx offers the call's codec (no SDP) | +26.7 |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 859.2 ms (-109.8/+11.4) | - | +17.5 |
| greeting | late | fail | fail | 200 OK to agent speech: 3066.1 ms (-109.8/+11.4) | agent speaks within 2000 ms | +31.3 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 1.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 75.3 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 1.6 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2257.6 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 1.0 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 4012.3 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 86.5 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -0.2 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 49.7 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -0.0 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (119 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (124 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 59.8 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -2975.2 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.8 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 68.1 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3004.7 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x245650bc->0x245650bc, seq 35544->35546, clock -2975 ms); resume from inactive: same RTP stream (ssrc 0x245650bc->0x245650bc, seq 35694->35696, clock -3005 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 922.5 ms (-109.8/+11.4) | - | +9.8 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-rfc4733 | no-events | unsupported | unsupported | - | telephone-event negotiated | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.8 ms (-0.4/+0.4)<br>digit to agent speech: 843.6 ms (-109.8/+11.4) | - | +4.6 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.9 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| dtmf-info | declines | unsupported | unsupported | INFO to its response: 0.8 ms (-0.4/+0.4) | INFO answered 2xx (SIP/2.0 405 Method Not Allowed) | - |
| refer | good | pass | pass | end of the request to REFER: 1355.9 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 1.5 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1379.1 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1337.9 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1031.0 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1354.6 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 879.1 ms (-109.8/+11.4) | - | +33.0 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1356.2 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 2 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1334.7 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60017.7 ms (-0.4/+0.4) | - | - |
| timer | unsupported | unsupported | unsupported | - | Session-Expires in the 2xx (timers not supported (RFC 4028 9, optional; the caller may refresh alone)) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| compact-headers | good | pass | pass | end of the question to agent speech: 1186.9 ms (-60.9/+15.5) | - | +49.9 |
| compact-headers | long-names | fail | fail | - | call completed (SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass | end of the question to agent speech: 1194.4 ms (-60.9/+15.5) | - | +9.9 |
| sdp-ssrc | strict | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass | end of the question to agent speech: 1198.4 ms (-60.9/+15.5) | - | +15.6 |
| late-offer | rejects | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass | end of the question to agent speech: 1319.6 ms (-60.9/+15.5) | - | -12.5 |
| ptime-30 | 20ms-only | fail | fail | - | agent replies within 10000 ms | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1186.9 ms (-60.9/+15.5) | - | -2.5 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1200.4 ms (-60.9/+15.5) | - | +65.4 (1/1 outside the bar) |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 1.7 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 149 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1269.6 ms (-60.9/+15.5) | - | +81.8 (1/1 outside the bar) |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 1.2 ms (-0.4/+0.4)<br>end of the question to agent speech: 1247.8 ms (-60.9/+15.5) | 2xx offers the call's codec (no SDP) | -12.5 |

Every case proven over 1 repeat(s): good passes, bad fails, a decline is unsupported.

Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-15.5, +60.9] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5)
- [-11.4, +109.8] ms: webrtcvad first onset, p5..p95, PCMU, lte-bad (calibrate --speech, seeds 1-5)
- [-3.6, +43.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5)
- [-3.2, +44.6] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5)
- [-0.8, +67.6] ms: webrtcvad first onset, p5..p95, PCMU, lte (calibrate --speech, seeds 1-5)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
- [+1.0, +63.6] ms: webrtcvad first onset, p5..p95, PCMU, clean (calibrate --speech, seeds 1-5)

Wall-clock steps during the run: none.

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 15 | 0.1 [0.1, 0.2] | 0.02 [0.01, 0.03] |
| lte | 15 | 15.3 [13.2, 19.2] | 3.23 [2.78, 3.56] |
| lte-bad | 15 | 106.8 [93.0, 122.8] | 20.12 [18.82, 20.89] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.
