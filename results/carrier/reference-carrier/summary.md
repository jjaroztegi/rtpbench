### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 810.0 [799.8, 830.0] ms (-32.9/+3.8) n=10 | - | +9.3 [-1.2, +29.3] |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3009.9 [2999.8, 3039.2] ms (-32.9/+3.8) n=10 | agent speaks within 2000 ms (10/10) | +9.5 [-0.8, +38.8] (1/10 outside the bar) |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 1.0 [0.8, 1.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 19.0 [7.9, 19.2] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.9 [0.7, 1.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2218.9 [2158.7, 2219.1] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 1.4 [1.0, 1.7] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 3549.5 [3370.4, 4339.2] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 1.3 [1.1, 2.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.4 [1.1, 7.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 32.7 [24.7, 34.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.0 [-0.1, 0.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.4 [1.1, 2.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.5 [1.2, 1.8] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 27.8 [21.5, 39.4] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.0 [-0.1, 0.1] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.6 [1.1, 3.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.6 [1.1, 2.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.1 [1.0, 1.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.3 [1.0, 1.7] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.4 [1.1, 2.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.3 [1.1, 1.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 34.5 [25.1, 37.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3000.0 [-3000.1, -2959.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.4 [1.1, 1.6] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.2 [1.1, 2.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 30.2 [23.5, 38.7] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3000.0 [-3019.9, -2960.0] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x22294954->0x22294954, seq 27364->27367, clock -3000 ms); resume from inactive: same RTP stream (10/10: ssrc 0x22294954->0x22294954, seq 27515->27517, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 819.0 [799.3, 849.6] ms (-32.9/+3.8) n=10 | - | +18.7 [-1.0, +48.7] (1/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.5 [0.4, 0.8] ms (-0.4/+0.4) n=10<br>digit to agent speech: 817.5 [797.8, 844.8] ms (-32.9/+3.8) n=10 | - | +16.6 [-3.2, +44.0] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.6 [0.5, 0.8] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1428.9 [1310.6, 1477.3] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1.2 [0.9, 1.4] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1431.8 [1319.1, 1485.8] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1427.2 [1311.5, 1467.6] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1000.8 [-1001.2, -1000.0] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1434.9 [1310.5, 1473.6] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 817.1 [798.8, 842.0] ms (-32.9/+3.8) n=10 | - | +16.2 [-2.0, +41.1] (1/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1424.9 [1307.9, 1473.7] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1429.2 [1300.4, 1473.6] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.5 [1.1, 1.8] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 59929.0 [59897.9, 59947.2] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.3 [1.1, 2.2] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| compact-headers | good | pass | pass 10/10 | end of the question to agent speech: 1226.4 [1105.6, 1286.2] ms (-32.9/+3.8) n=10 | - | +12.1 [+0.0, +27.5] |
| compact-headers | long-names | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass 10/10 | end of the question to agent speech: 1232.5 [1105.7, 1287.4] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.4] |
| sdp-ssrc | strict | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass 10/10 | end of the question to agent speech: 1227.3 [1106.5, 1307.2] ms (-32.9/+3.8) n=10 | - | +12.1 [+0.0, +27.5] |
| late-offer | rejects | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass 10/10 | end of the question to agent speech: 1278.7 [1145.7, 1366.5] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.5] |
| ptime-30 | 20ms-only | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1226.5 [1105.5, 1287.1] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.5] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.3 [1.2, 2.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1226.3 [1105.7, 1286.3] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.5] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.5 [1.0, 2.0] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 17 ms after the 2xx); agent replies within 10000 ms (10/10) | - |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 852.1 [836.2, 879.1] ms (-32.3/+3.4) n=10 | - | +9.4 [-0.6, +36.1] (2/10 outside the bar) |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3054.3 [3040.2, 3070.6] ms (-32.3/+3.4) n=10 | agent speaks within 2000 ms (10/10) | +9.3 [-0.6, +29.0] |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.9 [0.7, 1.1] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 57.9 [54.4, 63.3] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.9 [0.7, 7.8] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2201.6 [2161.6, 2218.3] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 1.3 [1.0, 6.5] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 3543.3 [3404.9, 3622.2] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 1.4 [1.3, 6.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.3 [1.1, 1.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 74.6 [63.1, 79.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.6 [-38.5, 3.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.2 [1.1, 1.7] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.4 [1.2, 2.3] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 68.3 [64.2, 78.0] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.6 [-3.0, 1.7] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.4 [1.0, 2.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.4 [1.1, 1.6] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.2 [1.0, 1.8] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.5 [1.1, 1.7] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 126 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 122 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.3 [1.0, 1.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.3 [1.2, 1.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 72.2 [61.9, 83.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3000.2 [-3003.0, -2998.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.4 [1.0, 1.6] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.5 [1.3, 2.3] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 69.8 [60.5, 77.1] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -2999.9 [-3003.7, -2957.7] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x41719a5->0x41719a5, seq 61335->61337, clock -3001 ms); resume from inactive: same RTP stream (10/10: ssrc 0x41719a5->0x41719a5, seq 61485->61487, clock -2961 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 894.9 [867.9, 934.4] ms (-32.3/+3.4) n=10 | - | +12.9 [-9.2, +52.5] (3/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.6 [0.4, 0.7] ms (-0.4/+0.4) n=10<br>digit to agent speech: 853.1 [841.3, 887.4] ms (-32.3/+3.4) n=10 | - | +8.2 [-2.6, +43.6] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.7 [0.4, 0.9] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1472.0 [1357.9, 1510.3] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1.2 [0.9, 1.5] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1472.8 [1352.3, 1520.3] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1464.5 [1348.4, 1520.3] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1000.3 [-1001.1, -997.5] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1476.2 [1341.5, 1527.7] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 854.9 [833.9, 894.4] ms (-32.3/+3.4) n=10 | - | +11.9 [-7.4, +52.7] (2/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1467.8 [1349.5, 1522.1] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1471.1 [1362.0, 1515.2] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.4 [1.1, 1.8] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 59933.1 [59910.2, 59948.1] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.6 [1.3, 2.9] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| compact-headers | good | pass | pass 10/10 | end of the question to agent speech: 1296.7 [1125.7, 1367.0] ms (-32.3/+3.4) n=10 | - | +10.5 [-8.9, +24.5] (1/10 outside the bar) |
| compact-headers | long-names | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass 10/10 | end of the question to agent speech: 1309.8 [1186.0, 1369.2] ms (-32.3/+3.4) n=10 | - | +9.0 [-8.2, +26.9] (1/10 outside the bar) |
| sdp-ssrc | strict | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass 10/10 | end of the question to agent speech: 1316.7 [1184.2, 1349.4] ms (-32.3/+3.4) n=10 | - | +9.1 [+0.0, +23.0] |
| late-offer | rejects | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass 10/10 | end of the question to agent speech: 1353.7 [1212.6, 1409.3] ms (-32.3/+3.4) n=10 | - | +11.0 [+0.0, +31.5] |
| ptime-30 | 20ms-only | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1297.9 [1155.0, 1351.0] ms (-32.3/+3.4) n=10 | - | +9.8 [+0.0, +17.0] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.4 [1.2, 1.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1311.8 [1176.6, 1369.5] ms (-32.3/+3.4) n=10 | - | +11.5 [-1.2, +19.8] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.5 [1.3, 2.2] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 51 ms after the 2xx); agent replies within 10000 ms (10/10) | - |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 863.2 [821.1, 901.0] ms (-52.5/+16.7) n=10 | - | +0.0 [-0.8, +9.5] |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3039.6 [3012.9, 3078.8] ms (-52.5/+16.7) n=10 | agent speaks within 2000 ms (10/10) | +9.4 [-0.8, +20.0] |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.9 [0.8, 1.6] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 64.4 [-3.9, 105.3] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 1.0 [0.8, 1.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2185.8 [2138.5, 2234.5] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 1.3 [1.0, 2.1] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 3551.7 [3349.7, 3680.4] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (9/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 1.3 [1.2, 2.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.2 [1.0, 2.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 53.5 [37.4, 97.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.1 [-10.2, 15.7] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.1 [1.0, 1.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.3 [1.1, 2.2] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 75.0 [26.7, 158.3] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.7 [-29.9, 10.6] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.3 [1.0, 1.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.4 [1.0, 1.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.2 [1.0, 1.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.2 [1.0, 1.9] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 122 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 119 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.4 [1.1, 5.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.3 [1.0, 7.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 72.5 [45.8, 130.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3001.6 [-3032.8, -2991.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.2 [1.1, 2.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.4 [1.1, 5.1] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 53.6 [26.6, 102.2] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -2998.4 [-3020.0, -2940.1] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x6cf975e2->0x6cf975e2, seq 41335->41337, clock -2991 ms); resume from inactive: same RTP stream (10/10: ssrc 0x6cf975e2->0x6cf975e2, seq 41485->41487, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 929.0 [870.1, 1015.0] ms (-52.5/+16.7) n=10 | - | +47.5 [-9.7, +149.7] (4/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.6 [0.5, 0.8] ms (-0.4/+0.4) n=10<br>digit to agent speech: 869.0 [822.6, 951.1] ms (-52.5/+16.7) n=10 | - | +7.6 [-6.4, +60.4] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.5 [0.4, 1.2] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1474.9 [1384.1, 1565.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1.2 [0.9, 2.6] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1487.3 [1344.1, 1533.5] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1480.6 [1335.7, 1560.6] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1000.7 [-1002.5, -949.4] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1456.3 [1353.2, 1518.4] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 866.7 [826.5, 900.6] ms (-52.5/+16.7) n=10 | - | +12.3 [-14.6, +91.9] (2/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1474.0 [1382.3, 1536.4] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1469.4 [1383.5, 1534.6] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.4 [1.2, 1.7] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 59933.9 [59898.1, 59997.2] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.3 [1.1, 1.6] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| compact-headers | good | pass | pass 10/10 | end of the question to agent speech: 1355.0 [1171.7, 1458.4] ms (-52.5/+16.7) n=10 | - | +1.6 [-10.8, +57.4] (1/10 outside the bar) |
| compact-headers | long-names | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass 10/10 | end of the question to agent speech: 1343.2 [1213.2, 1425.1] ms (-52.5/+16.7) n=10 | - | +1.6 [-8.6, +71.5] (1/10 outside the bar) |
| sdp-ssrc | strict | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass 10/10 | end of the question to agent speech: 1361.6 [1267.5, 1484.9] ms (-52.5/+16.7) n=10 | - | +0.0 [-15.5, +85.9] (1/10 outside the bar) |
| late-offer | rejects | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass 10/10 | end of the question to agent speech: 1395.5 [1290.5, 1480.4] ms (-52.5/+16.7) n=10 | - | +3.6 [-17.0, +58.7] (3/10 outside the bar) |
| ptime-30 | 20ms-only | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1346.3 [1157.0, 1443.4] ms (-52.5/+16.7) n=10 | - | +1.6 [-8.6, +134.6] (1/10 outside the bar) |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.4 [1.1, 2.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1350.3 [1192.5, 1488.5] ms (-52.5/+16.7) n=10 | - | +4.5 [-12.4, +63.7] (2/10 outside the bar) |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.7 [1.2, 2.3] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 112 ms after the 2xx); agent replies within 10000 ms (10/10) | - |

Every case proven over 10 repeat(s): good passes, bad fails.

Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-16.7, +52.5] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech --profiles lte-bad)
- [-3.8, +32.9] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech)
- [-3.4, +32.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech --profiles lte)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
