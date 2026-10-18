### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 809.9 [799.9, 829.9] ms (-63.6/-1.0) n=10 | - | +9.6 [-0.9, +29.5] (3/10 outside the bar) |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3009.8 [2999.8, 3030.0] ms (-63.6/-1.0) n=10 | agent speaks within 2000 ms (10/10) | +9.5 [-0.8, +29.5] (3/10 outside the bar) |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 1.1 [1.0, 1.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 18.7 [16.9, 19.0] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.9 [0.8, 1.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2218.7 [2218.4, 2218.9] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 1.2 [0.9, 3.6] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 4145.1 [4048.5, 4242.2] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 1.3 [1.1, 2.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.3 [1.1, 1.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 33.6 [32.2, 35.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.0 [-0.0, 0.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.3 [0.9, 1.7] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.3 [1.0, 1.5] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 29.3 [27.5, 32.0] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.0 [-0.1, 0.0] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.3 [1.1, 2.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.4 [1.1, 2.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.2 [1.0, 2.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.1 [1.1, 1.6] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.3 [1.0, 1.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.2 [1.1, 2.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 34.3 [33.0, 34.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3000.0 [-3000.0, -3000.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.2 [1.1, 1.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.3 [1.1, 1.8] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 30.0 [27.7, 31.1] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3000.0 [-3000.1, -3000.0] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x2fa64019->0x2fa64019, seq 48010->48012, clock -3000 ms); resume from inactive: same RTP stream (10/10: ssrc 0x2fa64019->0x2fa64019, seq 48160->48162, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 818.9 [799.0, 849.1] ms (-63.6/-1.0) n=10 | - | +18.6 [-1.2, +48.7] (1/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.5 [0.4, 0.8] ms (-0.4/+0.4) n=10<br>digit to agent speech: 817.7 [797.4, 847.9] ms (-63.6/-1.0) n=10 | - | +17.0 [-3.2, +47.3] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.5 [0.4, 0.7] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1430.2 [1303.1, 1470.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1.2 [0.9, 3.1] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1433.5 [1302.5, 1482.4] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1438.1 [1307.7, 1469.0] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1034.2 [-1055.4, -1030.7] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1435.3 [1303.9, 1483.2] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 813.1 [798.2, 851.0] ms (-63.6/-1.0) n=10 | - | +12.6 [-2.4, +48.8] (1/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1432.7 [1310.8, 1472.7] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1439.5 [1307.9, 1471.2] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.4 [1.1, 2.7] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 60011.4 [60001.6, 60019.9] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.4 [1.0, 2.5] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| compact-headers | good | pass | pass 10/10 | end of the question to agent speech: 1228.5 [1105.4, 1286.3] ms (-44.6/+3.2) n=10 | - | +12.1 [+0.0, +27.5] |
| compact-headers | long-names | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass 10/10 | end of the question to agent speech: 1225.5 [1105.3, 1287.2] ms (-44.6/+3.2) n=10 | - | +13.0 [+0.0, +44.2] |
| sdp-ssrc | strict | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass 10/10 | end of the question to agent speech: 1226.8 [1106.3, 1287.0] ms (-44.6/+3.2) n=10 | - | +12.2 [+0.0, +27.5] |
| late-offer | rejects | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass 10/10 | end of the question to agent speech: 1292.6 [1163.0, 1327.3] ms (-44.6/+3.2) n=10 | - | +12.2 [+0.0, +27.5] |
| ptime-30 | 20ms-only | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1228.5 [1103.7, 1286.2] ms (-44.6/+3.2) n=10 | - | +12.2 [+0.0, +27.5] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.3 [1.2, 1.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1232.5 [1105.4, 1286.3] ms (-44.6/+3.2) n=10 | - | +12.2 [+0.0, +27.5] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.4 [1.0, 6.8] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 15 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.1 [0.9, 1.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1226.3 [1105.5, 1286.3] ms (-44.6/+3.2) n=10 | - | +12.2 [+0.0, +27.5] |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.9 [0.6, 1.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1226.2 [1105.6, 1286.3] ms (-44.6/+3.2) n=10 | 2xx offers the call's codec (10/10: no SDP) | +12.2 [+0.0, +27.6] |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 853.7 [838.4, 871.8] ms (-67.6/+0.8) n=10 | - | +9.5 [-0.5, +32.8] |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3052.7 [3036.2, 3072.5] ms (-67.6/+0.8) n=10 | agent speaks within 2000 ms (10/10) | +9.4 [-0.6, +32.1] |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 1.0 [0.8, 2.0] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 59.0 [57.7, 62.8] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.9 [0.9, 1.1] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2198.9 [2182.0, 2218.3] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 1.1 [0.9, 2.2] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 4055.9 [3989.6, 4176.6] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 1.1 [1.0, 1.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.2 [1.0, 1.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 73.7 [69.2, 76.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.5 [-3.2, 3.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.2 [1.0, 2.7] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.2 [1.0, 1.5] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 70.3 [68.2, 72.5] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.8 [-1.0, 5.7] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.1 [1.0, 5.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.2 [1.0, 1.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.2 [0.9, 1.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.1 [1.0, 1.3] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 124 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 123 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.2 [1.1, 1.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.1 [1.0, 3.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 74.5 [72.7, 77.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3000.2 [-3003.1, -2995.8] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.1 [1.0, 1.6] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.2 [1.0, 1.5] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 70.6 [67.1, 77.4] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3000.0 [-3003.2, -2997.2] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0xe3a8e7c1->0xe3a8e7c1, seq 19644->19646, clock -2996 ms); resume from inactive: same RTP stream (10/10: ssrc 0xe3a8e7c1->0xe3a8e7c1, seq 19794->19796, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 896.3 [877.5, 916.2] ms (-67.6/+0.8) n=10 | - | +14.3 [-6.2, +46.0] (1/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.5 [0.5, 0.7] ms (-0.4/+0.4) n=10<br>digit to agent speech: 855.5 [837.6, 889.0] ms (-67.6/+0.8) n=10 | - | +13.6 [-2.6, +50.9] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.5 [0.4, 0.6] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1466.0 [1354.1, 1508.6] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1.0 [0.9, 1.3] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1459.4 [1341.4, 1529.2] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1463.4 [1349.8, 1510.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1031.4 [-1038.4, -1030.5] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1473.8 [1347.7, 1512.2] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 855.4 [842.4, 889.9] ms (-67.6/+0.8) n=10 | - | +14.8 [-2.7, +50.8] (2/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1473.9 [1350.2, 1514.8] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1475.2 [1351.8, 1528.5] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.2 [1.1, 1.3] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 60009.4 [60003.7, 60016.4] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.3 [1.1, 2.1] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| compact-headers | good | pass | pass 10/10 | end of the question to agent speech: 1298.3 [1174.4, 1365.2] ms (-43.3/+3.6) n=10 | - | +11.9 [+0.0, +17.1] |
| compact-headers | long-names | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass 10/10 | end of the question to agent speech: 1299.2 [1173.0, 1366.5] ms (-43.3/+3.6) n=10 | - | +12.3 [-1.2, +17.8] |
| sdp-ssrc | strict | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass 10/10 | end of the question to agent speech: 1308.0 [1184.3, 1350.9] ms (-43.3/+3.6) n=10 | - | +14.8 [+0.0, +22.8] |
| late-offer | rejects | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass 10/10 | end of the question to agent speech: 1345.6 [1242.7, 1407.1] ms (-43.3/+3.6) n=10 | - | +9.9 [+0.0, +17.0] |
| ptime-30 | 20ms-only | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1320.7 [1181.2, 1345.3] ms (-43.3/+3.6) n=10 | - | +11.7 [+0.0, +27.7] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.2 [1.0, 2.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1312.6 [1190.4, 1363.7] ms (-43.3/+3.6) n=10 | - | +8.2 [+0.0, +29.0] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.2 [1.0, 1.8] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 58 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.0 [0.9, 1.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1317.5 [1187.8, 1368.7] ms (-43.3/+3.6) n=10 | - | +8.9 [+0.0, +28.5] |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.7 [0.6, 1.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1307.3 [1186.4, 1348.9] ms (-43.3/+3.6) n=10 | 2xx offers the call's codec (10/10: no SDP) | +11.3 [+0.0, +24.3] |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 856.4 [811.7, 912.0] ms (-109.8/+11.4) n=10 | - | -0.2 [-0.5, +49.7] |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3061.0 [2999.8, 3086.9] ms (-109.8/+11.4) n=10 | agent speaks within 2000 ms (10/10) | +9.5 [-0.5, +38.2] |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.8 [0.7, 1.1] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 73.8 [8.5, 104.9] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.9 [0.8, 0.9] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2193.6 [2145.8, 2265.6] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 1.0 [0.9, 1.2] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 3910.3 [3896.5, 4040.2] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (9/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 1.1 [1.0, 1.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.1 [1.0, 1.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 76.1 [34.6, 162.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.2 [-16.1, 14.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.0 [0.9, 1.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.0 [1.0, 1.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 64.3 [44.6, 119.3] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -1.8 [-14.5, 23.8] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.1 [1.0, 1.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.0 [0.9, 1.2] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.0 [0.9, 1.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.0 [0.9, 1.2] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 119 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 120 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.1 [0.9, 1.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.1 [1.0, 1.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 76.6 [49.5, 135.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -2994.5 [-3015.8, -2981.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.0 [1.0, 1.8] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.1 [1.0, 1.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 78.8 [38.7, 114.8] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3000.0 [-3005.2, -2976.3] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0xf79d655b->0xf79d655b, seq 59579->59581, clock -3016 ms); resume from inactive: same RTP stream (10/10: ssrc 0xf79d655b->0xf79d655b, seq 59729->59731, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 896.5 [817.4, 949.3] ms (-109.8/+11.4) n=10 | - | +1.2 [-10.7, +57.1] |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.4 [0.4, 0.5] ms (-0.4/+0.4) n=10<br>digit to agent speech: 872.9 [833.3, 929.8] ms (-109.8/+11.4) n=10 | - | +15.4 [+0.0, +57.0] |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.5 [0.4, 0.6] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1479.5 [1368.1, 1535.3] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.9 [0.8, 1.6] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1480.6 [1368.3, 1521.9] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1472.7 [1348.7, 1556.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1029.8 [-1031.5, -1029.0] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1445.6 [1368.8, 1512.5] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 858.1 [805.3, 898.2] ms (-109.8/+11.4) n=10 | - | +11.0 [-14.1, +62.0] (1/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1465.6 [1391.0, 1525.4] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1463.3 [1391.8, 1534.6] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.1 [1.1, 1.3] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 60015.9 [60002.5, 60020.4] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.1 [1.0, 1.2] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| compact-headers | good | pass | pass 10/10 | end of the question to agent speech: 1336.2 [1198.1, 1446.7] ms (-60.9/+15.5) n=10 | - | +1.6 [-17.0, +89.6] (2/10 outside the bar) |
| compact-headers | long-names | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass 10/10 | end of the question to agent speech: 1334.8 [1282.2, 1408.9] ms (-60.9/+15.5) n=10 | - | +12.5 [-12.5, +68.6] (1/10 outside the bar) |
| sdp-ssrc | strict | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass 10/10 | end of the question to agent speech: 1302.2 [1219.0, 1530.4] ms (-60.9/+15.5) n=10 | - | -0.4 [-12.5, +86.1] (1/10 outside the bar) |
| late-offer | rejects | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass 10/10 | end of the question to agent speech: 1399.3 [1245.8, 1473.0] ms (-60.9/+15.5) n=10 | - | +2.7 [-7.0, +44.7] |
| ptime-30 | 20ms-only | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1356.2 [1188.5, 1401.2] ms (-60.9/+15.5) n=10 | - | +3.6 [-17.0, +21.1] (1/10 outside the bar) |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.0 [1.0, 1.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1336.8 [1124.4, 1435.3] ms (-60.9/+15.5) n=10 | - | -1.2 [-9.5, +62.3] (1/10 outside the bar) |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.1 [1.0, 1.4] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 44 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.9 [0.8, 1.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1342.9 [1220.1, 1390.5] ms (-60.9/+15.5) n=10 | - | +7.2 [-7.0, +73.5] (1/10 outside the bar) |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.6 [0.6, 0.8] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1335.8 [1258.7, 1451.4] ms (-60.9/+15.5) n=10 | 2xx offers the call's codec (10/10: no SDP) | +3.9 [-8.6, +68.8] (1/10 outside the bar) |

Every case proven over 10 repeat(s): good passes, bad fails.

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
