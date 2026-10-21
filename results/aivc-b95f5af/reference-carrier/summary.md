### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 829.8 ms (-63.6/-1.0) | - | +29.5 |
| greeting | late | fail | fail | 200 OK to agent speech: 3029.6 ms (-63.6/-1.0) | agent speaks within 2000 ms | +29.6 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 1.3 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 18.9 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 1.3 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2218.9 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 1.0 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3898.4 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 34.2 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: 0.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 29.0 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: 0.0 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.3 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (125 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (125 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 1.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.3 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 35.0 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -3000.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 29.8 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3000.0 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x78cb8484->0x78cb8484, seq 5601->5603, clock -3000 ms); resume from inactive: same RTP stream (ssrc 0x78cb8484->0x78cb8484, seq 5751->5753, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 819.3 ms (-63.6/-1.0) | - | +19.0 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.8 ms (-0.4/+0.4)<br>digit to agent speech: 828.6 ms (-63.6/-1.0) | - | +27.6 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.9 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| refer | good | pass | pass | end of the request to REFER: 1310.1 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 1.9 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1313.3 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1312.5 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1029.7 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1313.1 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 830.7 ms (-63.6/-1.0) | - | +29.8 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1314.2 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 2 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1318.4 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60015.1 ms (-0.4/+0.4) | - | - |
| timer | unsupported | inconclusive | inconclusive | - | Session-Expires in the 2xx (timers not supported (RFC 4028 9, optional; the caller may refresh alone)) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| compact-headers | good | pass | pass | end of the question to agent speech: 1105.6 ms (-44.6/+3.2) | - | +27.4 |
| compact-headers | long-names | fail | fail | - | call completed (SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass | end of the question to agent speech: 1105.5 ms (-44.6/+3.2) | - | +27.5 |
| sdp-ssrc | strict | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass | end of the question to agent speech: 1106.6 ms (-44.6/+3.2) | - | +27.5 |
| late-offer | rejects | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass | end of the question to agent speech: 1165.6 ms (-44.6/+3.2) | - | +27.5 |
| ptime-30 | 20ms-only | fail | fail | - | agent replies within 10000 ms | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1105.4 ms (-44.6/+3.2) | - | +27.5 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>end of the question to agent speech: 1105.6 ms (-44.6/+3.2) | - | +27.5 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 3 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1105.4 ms (-44.6/+3.2) | - | +27.5 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 1.1 ms (-0.4/+0.4)<br>end of the question to agent speech: 1105.6 ms (-44.6/+3.2) | 2xx offers the call's codec (no SDP) | +27.5 |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 867.9 ms (-67.6/+0.8) | - | +32.0 |
| greeting | late | fail | fail | 200 OK to agent speech: 3068.5 ms (-67.6/+0.8) | agent speaks within 2000 ms | +26.3 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 1.3 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 61.4 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 1.1 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2218.9 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 0.9 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3974.7 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 69.9 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -1.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 2.5 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 66.7 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -5.5 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 2.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (125 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (125 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 72.2 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -3001.2 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 72.4 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3003.4 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x71efd70c->0x71efd70c, seq 2184->2186, clock -3001 ms); resume from inactive: same RTP stream (ssrc 0x71efd70c->0x71efd70c, seq 2334->2336, clock -3003 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 919.7 ms (-67.6/+0.8) | - | +43.2 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.8 ms (-0.4/+0.4)<br>digit to agent speech: 872.2 ms (-67.6/+0.8) | - | +35.9 |
| dtmf-info | deaf | fail | fail | INFO to its response: 1.0 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| refer | good | pass | pass | end of the request to REFER: 1349.8 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 1.5 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1350.6 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1352.5 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1030.1 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1354.8 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 872.9 ms (-67.6/+0.8) | - | +33.9 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1352.3 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 2 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1352.7 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 1.7 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60002.3 ms (-0.4/+0.4) | - | - |
| timer | unsupported | inconclusive | inconclusive | - | Session-Expires in the 2xx (timers not supported (RFC 4028 9, optional; the caller may refresh alone)) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| compact-headers | good | pass | pass | end of the question to agent speech: 1188.9 ms (-43.3/+3.6) | - | +36.3 |
| compact-headers | long-names | fail | fail | - | call completed (SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass | end of the question to agent speech: 1187.1 ms (-43.3/+3.6) | - | +29.7 |
| sdp-ssrc | strict | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass | end of the question to agent speech: 1180.7 ms (-43.3/+3.6) | - | +24.4 |
| late-offer | rejects | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass | end of the question to agent speech: 1286.9 ms (-43.3/+3.6) | - | +34.7 |
| ptime-30 | 20ms-only | fail | fail | - | agent replies within 10000 ms | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1185.2 ms (-43.3/+3.6) | - | +25.2 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>end of the question to agent speech: 1188.5 ms (-43.3/+3.6) | - | +24.4 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 60 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 1.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1184.4 ms (-43.3/+3.6) | - | +38.4 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 0.9 ms (-0.4/+0.4)<br>end of the question to agent speech: 1207.7 ms (-43.3/+3.6) | 2xx offers the call's codec (no SDP) | +27.6 |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 841.7 ms (-109.8/+11.4) | - | +12.0 |
| greeting | late | fail | fail | 200 OK to agent speech: 3081.7 ms (-109.8/+11.4) | agent speaks within 2000 ms | +36.5 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 1.3 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 45.7 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 1.5 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2200.8 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 0.9 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3912.6 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 2.2 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 33.8 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: 5.2 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 48.6 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -16.2 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 1.9 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.6 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (114 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (121 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 44.9 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -2994.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 85.5 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3004.4 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x849ce70c->0x849ce70c, seq 35485->35487, clock -2994 ms); resume from inactive: same RTP stream (ssrc 0x849ce70c->0x849ce70c, seq 35632->35639, clock -3004 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 904.3 ms (-109.8/+11.4) | - | +19.1 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.8 ms (-0.4/+0.4)<br>digit to agent speech: 828.6 ms (-109.8/+11.4) | - | +8.4 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.8 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| refer | good | pass | pass | end of the request to REFER: 1352.8 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 1.5 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1353.9 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1371.3 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1029.8 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1354.7 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 881.7 ms (-109.8/+11.4) | - | -12.0 (1/1 outside the bar) |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1351.2 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 2 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1374.4 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 1.8 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60010.6 ms (-0.4/+0.4) | - | - |
| timer | unsupported | inconclusive | inconclusive | - | Session-Expires in the 2xx (timers not supported (RFC 4028 9, optional; the caller may refresh alone)) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 1.4 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| compact-headers | good | pass | pass | end of the question to agent speech: 1286.9 ms (-60.9/+15.5) | - | -2.5 |
| compact-headers | long-names | fail | fail | - | call completed (SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass | end of the question to agent speech: 1202.9 ms (-60.9/+15.5) | - | -12.5 |
| sdp-ssrc | strict | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass | end of the question to agent speech: 1212.5 ms (-60.9/+15.5) | - | +55.2 |
| late-offer | rejects | fail | fail | - | call completed (SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass | end of the question to agent speech: 1243.2 ms (-60.9/+15.5) | - | -2.0 |
| ptime-30 | 20ms-only | fail | fail | - | agent replies within 10000 ms | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1239.5 ms (-60.9/+15.5) | - | +39.0 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 1.5 ms (-0.4/+0.4)<br>end of the question to agent speech: 1190.9 ms (-60.9/+15.5) | - | +112.8 (1/1 outside the bar) |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 1.4 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 88 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 1.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1238.2 ms (-60.9/+15.5) | - | +104.6 (1/1 outside the bar) |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 1.0 ms (-0.4/+0.4)<br>end of the question to agent speech: 1280.6 ms (-60.9/+15.5) | 2xx offers the call's codec (no SDP) | +71.6 (1/1 outside the bar) |

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
| clean | 15 | 0.2 [0.1, 0.2] | 0.03 [0.01, 0.03] |
| lte | 15 | 15.4 [10.9, 19.4] | 3.35 [3.00, 3.55] |
| lte-bad | 15 | 108.1 [83.5, 121.4] | 20.20 [16.27, 21.18] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.
