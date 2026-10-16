### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 810.0 [799.8, 830.2] ms (-32.9/+3.8) n=10 | - | +9.5 [-0.5, +30.0] |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3009.8 [2999.8, 3029.9] ms (-32.9/+3.8) n=10 | agent speaks within 2000 ms (10/10) | +9.5 [-0.6, +29.5] |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 1.0 [0.8, 1.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 18.8 [16.2, 19.0] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.9 [0.8, 1.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2218.9 [2218.7, 2219.1] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 1.2 [1.0, 2.3] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 4117.8 [4028.9, 4215.0] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 1.2 [1.0, 1.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.2 [1.0, 1.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 34.5 [33.9, 35.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.0 [-0.0, 0.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.2 [0.9, 2.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.2 [1.0, 1.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 30.0 [28.9, 31.0] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.0 [-0.0, 0.0] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.2 [0.9, 1.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.2 [1.0, 1.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.2 [1.1, 3.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.3 [1.1, 2.1] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.3 [1.0, 3.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.2 [1.0, 2.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 33.8 [31.5, 35.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3000.0 [-3000.0, -3000.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.1 [1.0, 2.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.2 [1.0, 1.8] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 29.7 [26.5, 31.8] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3000.0 [-3000.0, -2999.9] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x4ad69e4e->0x4ad69e4e, seq 34855->34857, clock -3000 ms); resume from inactive: same RTP stream (10/10: ssrc 0x4ad69e4e->0x4ad69e4e, seq 35005->35007, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 819.1 [799.2, 848.9] ms (-32.9/+3.8) n=10 | - | +18.7 [-1.1, +48.6] (1/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.5 [0.4, 0.7] ms (-0.4/+0.4) n=10<br>digit to agent speech: 817.8 [798.2, 847.9] ms (-32.9/+3.8) n=10 | - | +17.1 [-2.5, +46.5] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.6 [0.4, 0.9] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1439.3 [1319.3, 1468.0] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1.2 [0.8, 1.9] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1430.3 [1300.5, 1476.0] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1426.2 [1310.3, 1474.9] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1039.3 [-1092.9, -1031.9] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1429.0 [1300.5, 1482.3] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 816.6 [793.9, 848.3] ms (-32.9/+3.8) n=10 | - | +16.0 [-6.8, +47.7] (2/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1432.2 [1312.3, 1476.9] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 2 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1427.8 [1317.0, 1477.3] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.4 [1.1, 1.5] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 60012.9 [60003.7, 60019.8] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.3 [1.1, 1.9] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| compact-headers | good | pass | pass 10/10 | end of the question to agent speech: 1226.4 [1105.0, 1286.0] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.5] |
| compact-headers | long-names | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass 10/10 | end of the question to agent speech: 1234.9 [1105.2, 1287.3] ms (-32.9/+3.8) n=10 | - | +12.1 [+0.0, +27.6] |
| sdp-ssrc | strict | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass 10/10 | end of the question to agent speech: 1227.2 [1106.3, 1285.7] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.5] |
| late-offer | rejects | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass 10/10 | end of the question to agent speech: 1301.1 [1165.0, 1326.3] ms (-32.9/+3.8) n=10 | - | +12.1 [+0.0, +27.5] |
| ptime-30 | 20ms-only | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1225.8 [1105.5, 1286.5] ms (-32.9/+3.8) n=10 | - | +12.0 [+0.0, +27.5] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.3 [1.1, 1.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1232.5 [1105.1, 1286.3] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.5] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.2 [1.0, 2.2] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 17 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.1 [0.8, 1.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1226.2 [1105.5, 1286.3] ms (-32.9/+3.8) n=10 | - | +11.9 [+0.0, +27.6] |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.8 [0.6, 1.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1232.5 [1105.4, 1286.3] ms (-32.9/+3.8) n=10 | 2xx offers the call's codec (10/10: no SDP) | +12.2 [+0.0, +27.6] |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 851.2 [833.6, 872.7] ms (-32.3/+3.4) n=10 | - | +9.4 [-0.5, +34.6] (2/10 outside the bar) |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3053.4 [3034.9, 3071.2] ms (-32.3/+3.4) n=10 | agent speaks within 2000 ms (10/10) | +9.4 [-0.5, +32.8] (1/10 outside the bar) |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 1.0 [0.9, 1.6] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 57.9 [49.7, 63.3] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 1.1 [0.9, 2.0] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2217.5 [2196.7, 2221.6] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 1.1 [0.9, 1.3] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 4069.1 [3975.4, 4270.5] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 1.3 [1.1, 1.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.3 [1.0, 2.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 75.2 [68.2, 83.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.4 [-7.1, 2.3] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.3 [1.0, 1.6] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.3 [1.0, 1.6] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 69.7 [60.6, 77.5] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.6 [-4.6, 2.2] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.3 [1.1, 2.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.2 [1.1, 2.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.1 [1.0, 1.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.1 [1.0, 2.6] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 124 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 124 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.2 [1.0, 1.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.3 [1.0, 2.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 73.8 [69.6, 77.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3000.9 [-3004.3, -2996.2] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.2 [1.0, 3.6] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.3 [1.1, 3.1] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 69.4 [60.8, 75.3] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3000.1 [-3003.7, -2995.4] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x6ba95e20->0x6ba95e20, seq 64750->64752, clock -3001 ms); resume from inactive: same RTP stream (10/10: ssrc 0x6ba95e20->0x6ba95e20, seq 64900->64902, clock -3001 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 898.0 [872.6, 920.3] ms (-32.3/+3.4) n=10 | - | +13.9 [-12.6, +45.0] (2/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.6 [0.4, 0.8] ms (-0.4/+0.4) n=10<br>digit to agent speech: 854.5 [835.8, 889.7] ms (-32.3/+3.4) n=10 | - | +15.6 [-5.4, +50.5] (2/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.5 [0.5, 1.1] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1471.3 [1349.6, 1517.6] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1.0 [0.9, 1.6] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1473.3 [1363.0, 1520.3] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1473.6 [1342.4, 1518.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1035.8 [-1052.5, -1030.5] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1473.3 [1342.6, 1520.5] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 855.4 [829.8, 886.5] ms (-32.3/+3.4) n=10 | - | +15.0 [-6.5, +49.8] (3/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1477.0 [1358.4, 1517.9] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 2 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1471.7 [1339.2, 1518.7] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.4 [1.1, 2.0] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 60008.6 [60002.2, 60014.6] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.3 [1.1, 3.0] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| compact-headers | good | pass | pass 10/10 | end of the question to agent speech: 1326.0 [1188.2, 1376.1] ms (-32.3/+3.4) n=10 | - | +8.0 [+0.0, +17.6] |
| compact-headers | long-names | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass 10/10 | end of the question to agent speech: 1325.7 [1184.3, 1361.2] ms (-32.3/+3.4) n=10 | - | +9.5 [+0.0, +24.5] |
| sdp-ssrc | strict | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass 10/10 | end of the question to agent speech: 1333.1 [1178.7, 1373.3] ms (-32.3/+3.4) n=10 | - | +10.9 [+0.0, +41.0] (1/10 outside the bar) |
| late-offer | rejects | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass 10/10 | end of the question to agent speech: 1362.9 [1264.8, 1405.4] ms (-32.3/+3.4) n=10 | - | +6.7 [+0.0, +27.2] |
| ptime-30 | 20ms-only | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1315.7 [1205.9, 1364.9] ms (-32.3/+3.4) n=10 | - | +8.5 [+0.0, +28.9] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.5 [1.0, 3.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1306.2 [1188.1, 1366.2] ms (-32.3/+3.4) n=10 | - | +9.3 [-2.4, +30.0] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.2 [1.1, 2.4] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 43 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.1 [0.9, 2.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1308.9 [1195.1, 1384.4] ms (-32.3/+3.4) n=10 | - | +9.9 [+0.0, +18.7] |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.8 [0.7, 1.0] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1306.7 [1203.5, 1367.3] ms (-32.3/+3.4) n=10 | 2xx offers the call's codec (10/10: no SDP) | +11.4 [+0.0, +19.7] |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 872.1 [844.0, 911.1] ms (-52.5/+16.7) n=10 | - | +9.3 [-0.6, +69.9] (1/10 outside the bar) |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3041.8 [2999.9, 3087.0] ms (-52.5/+16.7) n=10 | agent speaks within 2000 ms (10/10) | +9.4 [-0.6, +75.7] (1/10 outside the bar) |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 1.1 [0.8, 1.3] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 60.6 [27.7, 108.5] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 1.0 [0.9, 4.0] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2207.7 [2151.9, 2296.1] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 1.2 [1.0, 1.7] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 4106.1 [4008.5, 4253.6] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 1.3 [1.1, 4.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.3 [1.1, 4.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 71.7 [30.5, 119.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 1.3 [-22.3, 12.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.3 [1.2, 1.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.3 [1.1, 1.5] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 56.1 [24.8, 107.4] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.0 [-14.5, 22.0] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.3 [1.1, 2.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.3 [1.1, 3.7] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.2 [1.0, 2.6] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.3 [1.0, 1.6] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 118 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 123 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 1.3 [1.1, 1.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 1.2 [1.0, 1.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 63.1 [32.3, 118.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3004.6 [-3016.5, -2973.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 1.4 [1.0, 2.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 1.4 [1.0, 4.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 80.6 [37.7, 137.3] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -2998.8 [-3007.0, -2971.7] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x551173df->0x551173df, seq 18481->18483, clock -2995 ms); resume from inactive: same RTP stream (10/10: ssrc 0x551173df->0x551173df, seq 18631->18633, clock -2972 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 895.3 [851.5, 974.6] ms (-52.5/+16.7) n=10 | - | +6.4 [-6.5, +69.2] (3/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.6 [0.5, 0.8] ms (-0.4/+0.4) n=10<br>digit to agent speech: 855.6 [828.4, 893.7] ms (-52.5/+16.7) n=10 | - | +7.1 [-3.0, +56.7] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.5 [0.5, 0.8] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1483.9 [1350.6, 1559.9] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1.1 [0.9, 1.6] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1464.0 [1344.2, 1524.7] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1476.7 [1382.8, 1536.4] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1034.4 [-1054.8, -1031.3] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1486.7 [1346.9, 1546.4] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 871.7 [849.0, 919.2] ms (-52.5/+16.7) n=10 | - | +2.9 [-8.9, +69.3] (1/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1462.9 [1413.6, 1532.1] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1498.8 [1318.9, 1539.9] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.2 [1.1, 1.5] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 60009.7 [60002.2, 60018.6] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.2 [1.1, 1.8] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| compact-headers | good | pass | pass 10/10 | end of the question to agent speech: 1309.1 [1184.5, 1397.2] ms (-52.5/+16.7) n=10 | - | +1.9 [-8.6, +20.9] |
| compact-headers | long-names | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) | - |
| sdp-ssrc | good | pass | pass 10/10 | end of the question to agent speech: 1352.7 [1234.3, 1422.0] ms (-52.5/+16.7) n=10 | - | -1.2 [-17.0, +51.3] (1/10 outside the bar) |
| sdp-ssrc | strict | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| late-offer | good | pass | pass 10/10 | end of the question to agent speech: 1322.8 [1199.0, 1460.5] ms (-52.5/+16.7) n=10 | - | -1.2 [-8.6, +62.7] (1/10 outside the bar) |
| late-offer | rejects | fail | fail 10/10 | - | call completed (10/10: SIP/2.0 488 Not Acceptable Here) | - |
| ptime-30 | good | pass | pass 10/10 | end of the question to agent speech: 1357.8 [1280.8, 1453.4] ms (-52.5/+16.7) n=10 | - | -4.2 [-16.1, +4.0] |
| ptime-30 | 20ms-only | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1356.6 [1244.0, 1426.9] ms (-52.5/+16.7) n=10 | - | +5.6 [-7.0, +112.4] (3/10 outside the bar) |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.2 [1.0, 1.8] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1312.2 [1239.6, 1453.4] ms (-52.5/+16.7) n=10 | - | +14.7 [-17.0, +81.7] (2/10 outside the bar) |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 1.2 [0.9, 1.9] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 53 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 1.0 [0.9, 1.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1347.6 [1161.9, 1494.8] ms (-52.5/+16.7) n=10 | - | +3.1 [-17.0, +44.7] (1/10 outside the bar) |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.7 [0.6, 1.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1302.0 [1257.5, 1459.7] ms (-52.5/+16.7) n=10 | 2xx offers the call's codec (10/10: no SDP) | +1.6 [-8.6, +119.6] (2/10 outside the bar) |

Every case proven over 10 repeat(s): good passes, bad fails.

Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-16.7, +52.5] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech --profiles lte-bad)
- [-3.8, +32.9] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech)
- [-3.4, +32.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech --profiles lte)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)

Wall-clock steps during the run: none.
