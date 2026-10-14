### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 810.0 [798.6, 830.3] ms (-32.9/+3.8) n=10 | - | +9.2 [-3.1, +29.4] |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3009.9 [2998.7, 3039.9] ms (-32.9/+3.8) n=10 | agent speaks within 2000 ms (10/10) | +9.4 [-5.9, +38.2] (2/10 outside the bar) |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 1.1 [0.8, 4.3] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 18.3 [11.6, 18.9] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 1.2 [0.9, 2.8] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2218.7 [2138.5, 2231.1] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 2.2 [1.2, 19.5] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 3784.1 [3547.0, 4907.0] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 2.3 [1.3, 13.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.0 [1.5, 7.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 29.6 [19.8, 33.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.0 [-0.1, 0.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.1 [1.2, 9.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.6 [1.5, 6.3] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 29.9 [22.1, 37.1] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.0 [-0.1, 0.1] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.0 [1.6, 15.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.0 [1.2, 9.8] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.9 [1.3, 37.1] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.2 [1.5, 24.0] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.3 [1.2, 7.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.7 [1.1, 45.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 29.8 [21.4, 35.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3000.0 [-3040.0, -2960.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.8 [1.3, 4.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.8 [1.6, 4.0] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 30.7 [24.9, 38.7] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3000.0 [-3020.0, -2840.0] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x9ace7842->0x9ace7842, seq 42615->42617, clock -2960 ms); resume from inactive: same RTP stream (10/10: ssrc 0x9ace7842->0x9ace7842, seq 42765->42767, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 818.2 [798.3, 847.8] ms (-32.9/+3.8) n=10 | - | +17.6 [-2.5, +44.9] (1/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.9 [0.5, 13.9] ms (-0.4/+0.4) n=10<br>digit to agent speech: 815.7 [793.2, 847.4] ms (-32.9/+3.8) n=10 | - | +14.3 [-7.9, +43.4] (2/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.8 [0.5, 1.0] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1431.1 [1310.9, 1476.6] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1.6 [1.0, 19.0] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1436.3 [1304.0, 1478.0] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1440.4 [1303.8, 1477.1] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1060.1 [-1373.6, -1027.9] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1429.5 [1308.4, 1481.0] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 813.3 [797.3, 845.1] ms (-32.9/+3.8) n=10 | - | +12.5 [-4.4, +44.1] (2/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1431.2 [1303.4, 1476.7] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1427.0 [1311.2, 1474.0] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 2.6 [1.2, 9.3] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 59879.3 [59851.9, 59930.7] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 2.6 [1.3, 10.3] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| compact-headers | good | pass | pass 10/10 | end of the question to agent speech: 1238.4 [1123.6, 1286.3] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.7] |
| compact-headers | long-names | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass 10/10 | end of the question to agent speech: 1226.5 [1108.1, 1286.3] ms (-32.9/+3.8) n=10 | - | +12.5 [+0.0, +24.2] |
| sdp-ssrc | strict | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass 10/10 | end of the question to agent speech: 1227.4 [1096.6, 1287.3] ms (-32.9/+3.8) n=10 | - | +11.9 [+0.0, +17.6] |
| late-offer | rejects | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass 10/10 | end of the question to agent speech: 1294.9 [1193.7, 1363.9] ms (-32.9/+3.8) n=10 | - | +8.5 [+0.0, +27.5] |
| ptime-30 | 20ms-only | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1227.3 [1105.5, 1286.2] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.6] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 2.0 [1.4, 12.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1231.4 [1096.5, 1286.0] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +19.1] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.8 [1.3, 7.1] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 6 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.7 [0.9, 6.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1228.2 [1094.5, 1286.3] ms (-32.9/+3.8) n=10 | - | +15.0 [+0.0, +44.0] (1/10 outside the bar) |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.1 [0.8, 2.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1224.9 [1099.6, 1286.1] ms (-32.9/+3.8) n=10 | 2xx offers the call's codec (10/10: no SDP) | +8.5 [+0.0, +24.6] |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 850.6 [841.9, 881.1] ms (-32.3/+3.4) n=10 | - | +9.1 [-0.9, +38.9] (1/10 outside the bar) |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3056.4 [3035.1, 3073.7] ms (-32.3/+3.4) n=10 | agent speaks within 2000 ms (10/10) | +13.8 [-0.9, +31.0] |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 1.5 [1.0, 3.1] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 58.9 [53.1, 60.1] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 1.1 [0.9, 3.9] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2197.8 [2191.1, 2221.4] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 2.1 [1.4, 35.6] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 3976.7 [3559.7, 5316.1] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (9/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 1.9 [1.4, 39.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.7 [1.4, 4.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 70.0 [59.3, 76.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.4 [-4.3, 2.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.9 [1.6, 17.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.7 [1.3, 5.8] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 75.5 [63.4, 101.5] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.1 [-2.7, 3.7] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.8 [1.2, 13.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.0 [1.3, 6.8] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.0 [1.1, 14.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.2 [1.5, 3.4] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 123 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.9 [1.3, 7.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.0 [1.4, 4.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 64.9 [59.3, 75.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -2998.1 [-3023.7, -2938.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.2 [1.2, 4.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.8 [1.3, 3.0] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 72.6 [65.2, 79.2] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3004.3 [-3023.7, -2920.1] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0xd5452ece->0xd5452ece, seq 46497->46499, clock -3024 ms); resume from inactive: same RTP stream (10/10: ssrc 0xd5452ece->0xd5452ece, seq 46645->46647, clock -3022 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 894.1 [877.9, 944.2] ms (-32.3/+3.4) n=10 | - | +12.6 [-2.1, +42.8] (1/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.9 [0.5, 2.3] ms (-0.4/+0.4) n=10<br>digit to agent speech: 854.9 [837.0, 891.2] ms (-32.3/+3.4) n=10 | - | +12.4 [-6.2, +54.9] (2/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.7 [0.6, 1.8] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1473.8 [1342.3, 1523.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 2.0 [0.9, 26.9] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1467.2 [1337.6, 1530.3] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1480.1 [1351.2, 1509.6] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1061.3 [-1208.7, -1034.2] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1467.3 [1347.0, 1531.6] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 856.4 [838.9, 884.9] ms (-32.3/+3.4) n=10 | - | +16.0 [-7.1, +45.4] (2/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1472.1 [1355.3, 1520.2] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1473.8 [1338.5, 1519.0] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 2.0 [1.4, 2.8] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 59881.1 [59851.8, 59940.2] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 3.5 [1.4, 7.8] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| compact-headers | good | pass | pass 10/10 | end of the question to agent speech: 1303.8 [1174.5, 1368.9] ms (-32.3/+3.4) n=10 | - | +11.2 [+0.0, +40.8] (1/10 outside the bar) |
| compact-headers | long-names | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass 10/10 | end of the question to agent speech: 1310.4 [1206.9, 1374.0] ms (-32.3/+3.4) n=10 | - | +9.6 [-4.7, +30.2] (1/10 outside the bar) |
| sdp-ssrc | strict | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass 10/10 | end of the question to agent speech: 1308.6 [1190.2, 1355.7] ms (-32.3/+3.4) n=10 | - | +13.3 [+0.0, +33.7] (1/10 outside the bar) |
| late-offer | rejects | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass 10/10 | end of the question to agent speech: 1378.1 [1279.8, 1445.0] ms (-32.3/+3.4) n=10 | - | +11.5 [+0.0, +34.8] (1/10 outside the bar) |
| ptime-30 | 20ms-only | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1318.6 [1180.3, 1377.9] ms (-32.3/+3.4) n=10 | - | +14.4 [-2.0, +46.5] (2/10 outside the bar) |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.9 [1.3, 3.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1306.5 [1188.3, 1392.1] ms (-32.3/+3.4) n=10 | - | +6.3 [+0.0, +29.3] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.8 [1.3, 4.7] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 48 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.7 [1.1, 2.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1320.3 [1180.3, 1353.9] ms (-32.3/+3.4) n=10 | - | +14.1 [+0.0, +23.4] |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.0 [0.7, 1.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1310.7 [1182.1, 1367.1] ms (-32.3/+3.4) n=10 | 2xx offers the call's codec (10/10: no SDP) | +10.3 [+0.0, +26.4] |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 869.8 [809.5, 1018.6] ms (-52.5/+16.7) n=10 | - | +9.6 [-2.1, +159.8] (3/10 outside the bar) |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3052.2 [3018.9, 3099.1] ms (-52.5/+16.7) n=10 | agent speaks within 2000 ms (10/10) | +8.9 [-1.6, +81.2] (2/10 outside the bar) |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 1.4 [0.9, 5.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 75.7 [10.1, 102.2] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 2.0 [1.0, 7.3] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2191.5 [2131.7, 2265.0] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 1.8 [1.6, 15.8] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 3910.9 [3539.8, 4503.1] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (9/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 2.0 [1.4, 12.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.6 [1.2, 4.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 64.2 [29.7, 111.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.5 [-17.5, 16.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.0 [1.4, 6.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.8 [1.3, 3.0] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 43.4 [29.7, 124.3] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.1 [-25.1, 23.1] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.1 [1.4, 4.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.0 [1.5, 7.8] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.7 [1.2, 17.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.9 [1.1, 5.3] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 123 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 115 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.1 [1.3, 3.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.2 [1.3, 17.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 76.8 [23.0, 136.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -2992.1 [-3014.7, -2953.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.6 [1.6, 8.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.9 [1.2, 4.1] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 58.6 [19.9, 134.5] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3000.9 [-3058.8, -2989.1] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x33b26a65->0x33b26a65, seq 21035->21037, clock -2988 ms); resume from inactive: same RTP stream (10/10: ssrc 0x33b26a65->0x33b26a65, seq 21185->21187, clock -2999 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 897.7 [835.7, 986.9] ms (-52.5/+16.7) n=10 | - | -0.1 [-15.0, +43.6] |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.8 [0.6, 1.3] ms (-0.4/+0.4) n=10<br>digit to agent speech: 868.3 [808.1, 908.9] ms (-52.5/+16.7) n=10 | - | +4.5 [-8.2, +70.3] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.9 [0.5, 1.9] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1483.4 [1331.1, 1543.4] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1.6 [1.0, 51.2] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1457.2 [1337.4, 1523.9] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1489.8 [1323.3, 1564.1] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1064.8 [-1114.6, -1026.6] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1490.0 [1380.0, 1544.5] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 874.5 [836.2, 896.7] ms (-52.5/+16.7) n=10 | - | +42.6 [-11.0, +72.1] (3/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1454.6 [1386.3, 1564.3] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1478.8 [1388.1, 1553.6] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 2.9 [1.6, 8.7] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 59885.2 [59847.2, 59937.2] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 4.0 [2.2, 27.1] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| compact-headers | good | pass | pass 10/10 | end of the question to agent speech: 1356.1 [1278.9, 1404.0] ms (-52.5/+16.7) n=10 | - | +6.6 [-16.9, +55.6] (2/10 outside the bar) |
| compact-headers | long-names | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass 10/10 | end of the question to agent speech: 1346.5 [1287.6, 1553.7] ms (-52.5/+16.7) n=10 | - | +11.6 [-8.6, +104.6] (2/10 outside the bar) |
| sdp-ssrc | strict | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass 10/10 | end of the question to agent speech: 1338.4 [1163.0, 1401.6] ms (-52.5/+16.7) n=10 | - | +3.1 [-17.0, +35.1] (1/10 outside the bar) |
| late-offer | rejects | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass 10/10 | end of the question to agent speech: 1393.3 [1257.5, 1470.9] ms (-52.5/+16.7) n=10 | - | +3.6 [-8.4, +69.1] (1/10 outside the bar) |
| ptime-30 | 20ms-only | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1329.9 [1221.9, 1395.7] ms (-52.5/+16.7) n=10 | - | +1.6 [-3.5, +36.8] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 2.0 [1.3, 26.8] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1323.7 [1193.4, 1443.5] ms (-52.5/+16.7) n=10 | - | +3.6 [-17.0, +42.9] (1/10 outside the bar) |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 2.4 [1.3, 5.5] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 102 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.7 [1.1, 9.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1346.2 [1166.6, 1462.8] ms (-52.5/+16.7) n=10 | - | +1.6 [-17.0, +82.0] (2/10 outside the bar) |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.0 [0.7, 6.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1364.9 [1165.9, 1409.8] ms (-52.5/+16.7) n=10 | 2xx offers the call's codec (10/10: no SDP) | +3.6 [-16.4, +45.1] |

Every case proven over 10 repeat(s): good passes, bad fails.

Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-16.7, +52.5] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech --profiles lte-bad)
- [-3.8, +32.9] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech)
- [-3.4, +32.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech --profiles lte)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
