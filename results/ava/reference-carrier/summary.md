### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 829.8 ms (-63.6/-1.0) | - | +29.5 |
| greeting | late | fail | fail | 200 OK to agent speech: 3029.8 ms (-63.6/-1.0) | agent speaks within 2000 ms | +29.5 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 1.3 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 19.0 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 1.4 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2219.1 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 1.2 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 4016.3 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 34.4 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: 0.1 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 30.6 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: 0.0 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.8 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (125 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (125 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 34.5 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -3000.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 2.2 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 28.8 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3000.1 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0xf0c8dd11->0xf0c8dd11, seq 26873->26875, clock -3000 ms); resume from inactive: same RTP stream (ssrc 0xf0c8dd11->0xf0c8dd11, seq 27023->27025, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 819.3 ms (-63.6/-1.0) | - | +19.0 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.9 ms (-0.4/+0.4)<br>digit to agent speech: 828.3 ms (-63.6/-1.0) | - | +27.3 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.9 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| refer | good | pass | pass | end of the request to REFER: 1311.0 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 1.8 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1316.8 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1309.4 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1030.0 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1309.6 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 823.7 ms (-63.6/-1.0) | - | +22.7 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1312.9 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 2 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1311.7 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60008.3 ms (-0.4/+0.4) | - | - |
| timer | unsupported | fail | fail | - | Session-Expires in the 2xx (timers not supported) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 1.4 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| compact-headers | good | pass | pass | end of the question to agent speech: 1105.5 ms (-44.6/+3.2) | - | +27.5 |
| compact-headers | long-names | fail | fail | - | call completed (SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass | end of the question to agent speech: 1105.4 ms (-44.6/+3.2) | - | +27.4 |
| sdp-ssrc | strict | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass | end of the question to agent speech: 1096.7 ms (-44.6/+3.2) | - | +17.5 |
| late-offer | rejects | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass | end of the question to agent speech: 1165.6 ms (-44.6/+3.2) | - | +27.5 |
| ptime-30 | 20ms-only | fail | fail | - | agent replies within 10000 ms | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1105.3 ms (-44.6/+3.2) | - | +27.5 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1105.4 ms (-44.6/+3.2) | - | +27.5 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 2 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1105.6 ms (-44.6/+3.2) | - | +27.5 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 1.2 ms (-0.4/+0.4)<br>end of the question to agent speech: 1105.6 ms (-44.6/+3.2) | 2xx offers the call's codec (no SDP) | +27.5 |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 870.0 ms (-67.6/+0.8) | - | +35.1 |
| greeting | late | fail | fail | 200 OK to agent speech: 3073.0 ms (-67.6/+0.8) | agent speaks within 2000 ms | +34.2 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 1.3 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 55.0 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 1.4 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2216.7 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 1.0 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3989.8 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 72.0 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: 1.5 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 68.1 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -1.4 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.8 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.8 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (125 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (125 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 2.7 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 75.4 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -2998.3 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 2.1 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 72.2 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3000.6 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0xee63d2c0->0xee63d2c0, seq 5704->5706, clock -2998 ms); resume from inactive: same RTP stream (ssrc 0xee63d2c0->0xee63d2c0, seq 5854->5856, clock -3001 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 913.3 ms (-67.6/+0.8) | - | +27.7 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-info | good | pass | pass | INFO to its response: 1.0 ms (-0.4/+0.4)<br>digit to agent speech: 871.1 ms (-67.6/+0.8) | - | +32.4 |
| dtmf-info | deaf | fail | fail | INFO to its response: 1.0 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| refer | good | pass | pass | end of the request to REFER: 1352.0 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 2.2 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1349.7 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1352.0 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1031.4 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1350.7 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 864.2 ms (-67.6/+0.8) | - | +26.9 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1354.3 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 2 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1350.4 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60017.6 ms (-0.4/+0.4) | - | - |
| timer | unsupported | fail | fail | - | Session-Expires in the 2xx (timers not supported) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 1.7 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| compact-headers | good | pass | pass | end of the question to agent speech: 1185.7 ms (-43.3/+3.6) | - | +26.2 |
| compact-headers | long-names | fail | fail | - | call completed (SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass | end of the question to agent speech: 1177.3 ms (-43.3/+3.6) | - | +16.6 |
| sdp-ssrc | strict | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass | end of the question to agent speech: 1186.2 ms (-43.3/+3.6) | - | +30.0 |
| late-offer | rejects | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass | end of the question to agent speech: 1302.5 ms (-43.3/+3.6) | - | +21.0 |
| ptime-30 | 20ms-only | fail | fail | - | agent replies within 10000 ms | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1184.7 ms (-43.3/+3.6) | - | +25.0 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>end of the question to agent speech: 1205.9 ms (-43.3/+3.6) | - | +29.7 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 1.8 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 56 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 1.2 ms (-0.4/+0.4)<br>end of the question to agent speech: 1205.2 ms (-43.3/+3.6) | - | +26.0 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 1.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1204.7 ms (-43.3/+3.6) | 2xx offers the call's codec (no SDP) | +29.6 |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 830.6 ms (-109.8/+11.4) | - | +9.5 |
| greeting | late | fail | fail | 200 OK to agent speech: 3059.1 ms (-109.8/+11.4) | agent speaks within 2000 ms | +42.2 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 1.9 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 35.5 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 1.3 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2256.3 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 1.0 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3972.3 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 1.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 62.0 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -7.7 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 29.2 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: 16.8 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (123 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (118 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 62.1 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -3005.2 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.8 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 96.5 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3005.4 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x6fcb3ece->0x6fcb3ece, seq 25839->25841, clock -3005 ms); resume from inactive: same RTP stream (ssrc 0x6fcb3ece->0x6fcb3ece, seq 25989->25991, clock -3005 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 893.4 ms (-109.8/+11.4) | - | +9.8 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.9 ms (-0.4/+0.4)<br>digit to agent speech: 872.5 ms (-109.8/+11.4) | - | +37.6 |
| dtmf-info | deaf | fail | fail | INFO to its response: 1.1 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| refer | good | pass | pass | end of the request to REFER: 1373.7 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 1.6 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1391.3 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1371.9 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1030.5 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1347.8 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 903.1 ms (-109.8/+11.4) | - | +4.7 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1330.5 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 2 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1373.8 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60003.7 ms (-0.4/+0.4) | - | - |
| timer | unsupported | fail | fail | - | Session-Expires in the 2xx (timers not supported) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 1.4 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| compact-headers | good | pass | pass | end of the question to agent speech: 1167.8 ms (-60.9/+15.5) | - | +24.0 |
| compact-headers | long-names | fail | fail | - | call completed (SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass | end of the question to agent speech: 1202.1 ms (-60.9/+15.5) | - | +22.2 |
| sdp-ssrc | strict | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass | end of the question to agent speech: 1304.0 ms (-60.9/+15.5) | - | +0.0 |
| late-offer | rejects | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass | end of the question to agent speech: 1293.0 ms (-60.9/+15.5) | - | +63.8 (1/1 outside the bar) |
| ptime-30 | 20ms-only | fail | fail | - | agent replies within 10000 ms | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1238.8 ms (-60.9/+15.5) | - | +66.5 (1/1 outside the bar) |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 1.9 ms (-0.4/+0.4)<br>end of the question to agent speech: 1241.0 ms (-60.9/+15.5) | - | +38.4 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 69 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>end of the question to agent speech: 1284.4 ms (-60.9/+15.5) | - | +88.4 (1/1 outside the bar) |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 1.0 ms (-0.4/+0.4)<br>end of the question to agent speech: 1265.3 ms (-60.9/+15.5) | 2xx offers the call's codec (no SDP) | +70.3 (1/1 outside the bar) |

Every case proven over 1 repeat(s): good passes, bad fails.

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
| clean | 15 | 0.2 [0.1, 0.8] | 0.02 [0.01, 0.03] |
| lte | 15 | 14.6 [13.2, 18.7] | 3.31 [2.85, 3.55] |
| lte-bad | 15 | 106.5 [97.1, 120.6] | 20.21 [19.13, 21.33] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.
