### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 810.3 [800.2, 830.8] ms (-32.9/+3.8) n=10 | - | +9.5 [-0.5, +29.5] |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3010.2 [3000.1, 3030.2] ms (-32.9/+3.8) n=10 | agent speaks within 2000 ms (10/10) | +9.5 [-0.5, +29.5] |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.2 [0.2, 0.9] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 19.3 [18.1, 19.4] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.2 [0.2, 0.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2219.3 [2219.2, 2219.9] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 0.3 [0.2, 0.5] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 4097.4 [3997.2, 4299.2] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 36.3 [35.9, 37.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.0 [-0.0, 0.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 33.8 [33.1, 35.0] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.0 [-0.0, 0.0] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.2, 0.7] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.2, 1.4] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 1.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 36.8 [35.6, 37.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3000.0 [-3000.0, -3000.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 34.5 [33.7, 35.5] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3000.0 [-3000.0, -3000.0] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0xc55b1f11->0xc55b1f11, seq 26036->26037, clock -3000 ms); resume from inactive: same RTP stream (10/10: ssrc 0xc55b1f11->0xc55b1f11, seq 26186->26187, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 819.2 [799.4, 849.3] ms (-32.9/+3.8) n=10 | - | +19.1 [-0.8, +49.1] (1/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.2 [0.2, 0.5] ms (-0.4/+0.4) n=10<br>digit to agent speech: 818.3 [798.3, 847.9] ms (-32.9/+3.8) n=10 | - | +18.0 [-2.1, +47.5] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.2 [0.2, 0.4] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1436.4 [1301.5, 1474.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.3 [0.3, 1.0] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1426.9 [1302.2, 1476.5] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1426.8 [1312.8, 1472.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1030.9 [-1048.2, -1027.1] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1428.4 [1310.9, 1471.2] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 813.8 [798.1, 845.6] ms (-32.9/+3.8) n=10 | - | +13.4 [-2.1, +45.2] (1/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1431.9 [1307.7, 1478.1] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 0 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1428.3 [1318.1, 1484.3] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| codec-pcmu | good | pass | pass 10/10 | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU (10/10: payload types 8) | - |
| codec-pcma | good | pass | pass 10/10 | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA (10/10: payload types 0) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 60011.1 [60000.6, 60019.0] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1232.7 [1095.9, 1286.7] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +17.5] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| large-invite | good | pass | pass 10/10 | end of the question to agent speech: 1228.9 [1105.8, 1286.6] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.5] |
| large-invite | udp-only | fail | fail 10/10 | end of the question to agent speech: 1226.6 [1105.3, 1286.7] ms (-32.9/+3.8) n=10 | INVITE over TCP answered 2xx (10/10: ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) | +12.2 [+0.0, +27.5] |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1226.7 [1105.8, 1286.7] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.5] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.2, 0.5] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 2 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1226.6 [1105.8, 1286.5] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.5] |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1226.3 [1105.8, 1286.5] ms (-32.9/+3.8) n=10 | 2xx offers the call's codec (10/10: no SDP) | +12.2 [+0.0, +27.5] |
| hold-zero | good | pass | pass 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 [0.3, 0.9] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: 2xx to agent RTP: 36.5 [35.0, 37.4] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: RTP clock drift: -0.0 [-0.0, 0.0] ms (-0.4/+0.4) n=10 | - | - |
| hold-zero | ignores-address | fail | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) | - |
| codec-change | good | pass | pass 10/10 | end of the question to agent speech: 1227.8 [1125.7, 1286.6] ms (-24.3/+88.1) n=10 | - | +13.0 [+0.0, +27.5] (2/10 outside the bar) |
| codec-change | stale | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) | - |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 855.4 [843.9, 868.0] ms (-32.3/+3.4) n=10 | - | +9.5 [-0.5, +29.6] |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3050.7 [3035.5, 3075.1] ms (-32.3/+3.4) n=10 | agent speaks within 2000 ms (10/10) | +9.5 [-0.5, +39.3] (2/10 outside the bar) |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.2 [0.2, 0.3] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 58.4 [55.6, 63.5] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.2 [0.2, 0.3] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2201.7 [2196.9, 2218.6] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 0.3 [0.3, 0.7] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 4066.3 [3985.7, 4287.3] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 78.0 [74.2, 83.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.4 [-1.4, 3.3] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 73.6 [66.1, 78.3] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.7 [-3.2, 3.2] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.3, 1.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 123 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 78.5 [75.2, 81.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3001.9 [-3004.4, -3000.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.3, 0.9] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.3, 1.8] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 73.7 [69.4, 79.3] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -2999.1 [-3006.1, -2996.1] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x124e6679->0x124e6679, seq 48573->48574, clock -3004 ms); resume from inactive: same RTP stream (10/10: ssrc 0x124e6679->0x124e6679, seq 48723->48724, clock -2999 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 890.0 [876.5, 927.8] ms (-32.3/+3.4) n=10 | - | +10.4 [-6.5, +40.4] (2/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.2 [0.2, 0.7] ms (-0.4/+0.4) n=10<br>digit to agent speech: 859.2 [846.6, 888.7] ms (-32.3/+3.4) n=10 | - | +15.9 [-1.8, +52.4] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.2 [0.2, 0.4] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1464.0 [1348.1, 1512.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.3 [0.2, 1.0] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1473.1 [1360.1, 1513.9] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1468.0 [1356.7, 1513.4] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1031.3 [-1063.1, -1028.0] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1465.2 [1359.5, 1515.7] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 860.3 [833.4, 884.2] ms (-32.3/+3.4) n=10 | - | +18.8 [-4.1, +48.1] (2/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1471.0 [1349.7, 1512.7] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 0 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1468.2 [1345.9, 1518.3] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| codec-pcmu | good | pass | pass 10/10 | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU (10/10: payload types 8) | - |
| codec-pcma | good | pass | pass 10/10 | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA (10/10: payload types 0) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.4, 0.6] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 60007.1 [60002.7, 60015.7] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1310.8 [1186.2, 1364.2] ms (-32.3/+3.4) n=10 | - | +12.3 [-2.1, +42.3] (1/10 outside the bar) |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| large-invite | good | pass | pass 10/10 | end of the question to agent speech: 1308.0 [1183.7, 1395.5] ms (-32.3/+3.4) n=10 | - | +4.8 [+0.0, +31.6] |
| large-invite | udp-only | fail | fail 10/10 | end of the question to agent speech: 1305.0 [1183.9, 1376.0] ms (-32.3/+3.4) n=10 | INVITE over TCP answered 2xx (10/10: ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) | +11.9 [+0.0, +25.8] |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1310.2 [1209.3, 1374.1] ms (-32.3/+3.4) n=10 | - | +15.7 [-4.8, +46.9] (2/10 outside the bar) |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 1.6] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 48 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.8] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1308.0 [1208.3, 1369.6] ms (-32.3/+3.4) n=10 | - | +10.3 [+0.0, +31.0] |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1301.8 [1131.1, 1365.5] ms (-32.3/+3.4) n=10 | 2xx offers the call's codec (10/10: no SDP) | +8.6 [+0.0, +27.1] |
| hold-zero | good | pass | pass 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 [0.3, 0.8] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: 2xx to agent RTP: 77.0 [72.9, 80.7] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: RTP clock drift: -0.7 [-4.2, 4.6] ms (-0.4/+0.4) n=10 | - | - |
| hold-zero | ignores-address | fail | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 122 packets) | - |
| codec-change | good | pass | pass 10/10 | end of the question to agent speech: 1317.8 [1197.4, 1382.5] ms (-25.2/+87.6) n=10 | - | +10.4 [+0.0, +20.1] |
| codec-change | stale | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) | - |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 867.2 [841.6, 891.4] ms (-52.5/+16.7) n=10 | - | +9.4 [-0.5, +27.0] |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3045.8 [3013.2, 3149.7] ms (-52.5/+16.7) n=10 | agent speaks within 2000 ms (10/10) | +9.4 [-0.5, +88.3] (2/10 outside the bar) |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.2 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 68.3 [55.9, 99.4] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.2 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2203.3 [2126.7, 2263.9] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 4127.6 [3973.3, 4258.5] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 91.7 [41.9, 128.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -6.4 [-17.6, 12.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 69.7 [52.6, 125.9] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3.7 [-20.6, 4.8] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.3, 0.8] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 124 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 118 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 61.1 [36.5, 168.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -2999.8 [-3011.2, -2985.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.3, 1.5] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 58.7 [35.3, 114.1] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3001.8 [-3016.5, -2989.4] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0xfac0630c->0xfac0630c, seq 28468->28469, clock -2993 ms); resume from inactive: same RTP stream (10/10: ssrc 0xfac0630c->0xfac0630c, seq 28618->28619, clock -2998 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 884.3 [846.0, 948.0] ms (-52.5/+16.7) n=10 | - | -0.3 [-9.7, +98.4] (1/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.2 [0.2, 0.3] ms (-0.4/+0.4) n=10<br>digit to agent speech: 874.9 [847.3, 919.1] ms (-52.5/+16.7) n=10 | - | +7.7 [-4.7, +23.7] |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.2 [0.2, 1.4] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1463.4 [1374.8, 1497.6] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1460.2 [1333.9, 1494.1] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1463.5 [1401.7, 1539.2] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1041.7 [-1052.7, -1029.9] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1464.8 [1357.0, 1514.0] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 871.1 [842.4, 947.0] ms (-52.5/+16.7) n=10 | - | +9.9 [-9.0, +90.9] (2/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1491.7 [1354.3, 1557.6] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 0 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1472.3 [1336.9, 1496.0] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| codec-pcmu | good | pass | pass 10/10 | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU (10/10: payload types 8) | - |
| codec-pcma | good | pass | pass 10/10 | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA (10/10: payload types 0) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 60011.0 [60001.0, 60020.6] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.7] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1360.7 [1200.5, 1426.1] ms (-52.5/+16.7) n=10 | - | +5.8 [-3.5, +44.5] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| large-invite | good | pass | pass 10/10 | end of the question to agent speech: 1348.3 [1218.1, 1409.7] ms (-52.5/+16.7) n=10 | - | +7.0 [-17.0, +41.2] (1/10 outside the bar) |
| large-invite | udp-only | fail | fail 10/10 | end of the question to agent speech: 1341.4 [1238.1, 1419.2] ms (-52.5/+16.7) n=10 | INVITE over TCP answered 2xx (10/10: ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) | +1.6 [-17.0, +46.6] (1/10 outside the bar) |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 1.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1310.3 [1251.9, 1403.8] ms (-52.5/+16.7) n=10 | - | +0.3 [-17.0, +51.6] (1/10 outside the bar) |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 27 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1341.9 [1211.0, 1427.5] ms (-52.5/+16.7) n=10 | - | +0.0 [-7.0, +59.9] (1/10 outside the bar) |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 1.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1363.0 [1289.1, 1418.9] ms (-52.5/+16.7) n=10 | 2xx offers the call's codec (10/10: no SDP) | +2.0 [-17.0, +51.9] (1/10 outside the bar) |
| hold-zero | good | pass | pass 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: 2xx to agent RTP: 62.8 [33.7, 124.2] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: RTP clock drift: -0.1 [-19.2, 13.0] ms (-0.4/+0.4) n=10 | - | - |
| hold-zero | ignores-address | fail | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 [0.3, 0.6] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 121 packets) | - |
| codec-change | good | pass | pass 10/10 | end of the question to agent speech: 1310.5 [1199.0, 1424.0] ms (-35.1/+96.9) n=10 | - | +4.0 [-8.6, +68.5] (2/10 outside the bar) |
| codec-change | stale | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) | - |

Every case proven over 10 repeat(s): good passes, bad fails.

Error bars: true value = measured - error, error within

- [-96.9, +35.1] ms: webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech --profiles lte-bad)
- [-88.1, +24.3] ms: webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech)
- [-87.6, +25.2] ms: webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech --profiles lte)
- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-16.7, +52.5] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech --profiles lte-bad)
- [-3.8, +32.9] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech)
- [-3.4, +32.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech --profiles lte)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)

Wall-clock steps during the run: none.
