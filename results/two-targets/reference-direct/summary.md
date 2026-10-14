### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 810.5 [800.3, 840.3] ms (-32.9/+3.8) n=10 | - | +8.9 [-2.0, +38.6] (1/10 outside the bar) |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3013.0 [3000.3, 3037.2] ms (-32.9/+3.8) n=10 | agent speaks within 2000 ms (10/10) | +8.4 [-0.8, +29.4] |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.2 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 19.3 [19.1, 20.2] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.2 [0.1, 1.0] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2219.0 [2178.3, 2219.5] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 0.4 [0.4, 0.7] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 3697.6 [3566.6, 4468.2] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 0.5 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 36.2 [29.2, 37.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.0 [-0.0, 0.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.5 [0.3, 1.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.7 [0.3, 1.3] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 32.8 [25.8, 39.9] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.0 [-0.1, 0.0] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.6 [0.3, 1.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.6 [0.3, 1.6] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.5 [0.2, 3.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.5 [0.3, 1.2] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.6 [0.3, 9.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.6 [0.3, 11.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 31.2 [26.3, 36.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3000.0 [-3000.0, -2960.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 1.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.5 [0.3, 5.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 27.4 [21.7, 34.7] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3000.0 [-3000.0, -2960.0] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x46509dd6->0x46509dd6, seq 12476->12477, clock -3000 ms); resume from inactive: same RTP stream (10/10: ssrc 0x46509dd6->0x46509dd6, seq 12626->12627, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 811.5 [799.3, 849.2] ms (-32.9/+3.8) n=10 | - | +11.2 [-0.9, +49.0] (1/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.4 [0.2, 66.6] ms (-0.4/+0.4) n=10<br>digit to agent speech: 818.7 [798.8, 888.6] ms (-32.9/+3.8) n=10 | - | +16.9 [-1.6, +46.0] (2/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.3 [0.2, 4.6] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1431.7 [1313.8, 1479.3] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.4 [0.3, 6.2] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1430.2 [1300.5, 1475.3] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1429.6 [1322.4, 1474.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1063.2 [-1124.1, -1030.7] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1437.8 [1319.5, 1478.4] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 813.3 [798.3, 846.7] ms (-32.9/+3.8) n=10 | - | +11.0 [-2.1, +46.2] (1/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1436.8 [1306.0, 1482.8] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1435.4 [1318.3, 1480.5] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| codec-pcmu | good | pass | pass 10/10 | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU (10/10: payload types 8) | - |
| codec-pcma | good | pass | pass 10/10 | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA (10/10: payload types 0) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.3, 2.8] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 59873.5 [59846.9, 59937.7] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.6 [0.4, 2.1] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1227.3 [1106.0, 1286.6] ms (-32.9/+3.8) n=10 | - | +12.2 [+0.0, +27.5] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.6 [0.3, 1.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1226.5 [1105.3, 1286.7] ms (-32.9/+3.8) n=10 | - | +12.4 [+0.0, +27.5] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.7 [0.3, 1.7] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 4 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.5 [0.3, 3.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1227.6 [1094.9, 1286.7] ms (-32.9/+3.8) n=10 | - | +13.0 [+0.0, +22.5] |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.5 [0.4, 6.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1226.2 [1119.7, 1286.6] ms (-32.9/+3.8) n=10 | 2xx offers the call's codec (10/10: no SDP) | +8.5 [-3.8, +20.6] (1/10 outside the bar) |
| hold-zero | good | pass | pass 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.5 [0.3, 13.3] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 [0.2, 1.6] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: 2xx to agent RTP: 33.4 [28.4, 37.3] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: RTP clock drift: 0.0 [-0.0, 0.1] ms (-0.4/+0.4) n=10 | - | - |
| hold-zero | ignores-address | fail | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 0.9] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 [0.2, 0.8] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) | - |
| codec-change | good | pass | pass 10/10 | end of the question to agent speech: 1228.1 [1146.8, 1286.7] ms (-24.3/+88.1) n=10 | - | +13.0 [+0.0, +29.6] (2/10 outside the bar) |
| codec-change | stale | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) | - |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 849.3 [839.0, 877.3] ms (-32.3/+3.4) n=10 | - | +9.3 [-4.5, +37.0] (3/10 outside the bar) |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3059.8 [3037.6, 3073.6] ms (-32.3/+3.4) n=10 | agent speaks within 2000 ms (10/10) | +12.2 [-3.2, +36.0] (1/10 outside the bar) |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.3 [0.2, 0.6] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 61.5 [55.9, 64.2] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.3 [0.2, 0.6] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2213.0 [2195.7, 2222.1] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 0.5 [0.3, 1.5] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 3781.6 [3485.2, 4796.0] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 0.6 [0.3, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.5 [0.3, 1.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 75.1 [62.4, 88.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.7 [-3.3, 5.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.2, 10.2] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.3, 2.5] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 70.6 [61.2, 77.7] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.5 [-4.4, 3.8] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.6 [0.4, 4.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.3, 4.8] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.5 [0.3, 14.1] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.3, 1.8] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 123 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.5 [0.4, 0.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.5 [0.4, 0.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 75.7 [60.5, 83.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3001.0 [-3006.4, -2940.7] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 1.1] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.5 [0.3, 2.0] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 68.6 [56.6, 80.6] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -2996.3 [-3022.1, -2917.3] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x5114442c->0x5114442c, seq 61809->61810, clock -2999 ms); resume from inactive: same RTP stream (10/10: ssrc 0x5114442c->0x5114442c, seq 61959->61960, clock -2998 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 895.8 [877.9, 920.7] ms (-32.3/+3.4) n=10 | - | +16.9 [-5.5, +35.8] (3/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.3 [0.2, 0.7] ms (-0.4/+0.4) n=10<br>digit to agent speech: 856.9 [843.5, 885.3] ms (-32.3/+3.4) n=10 | - | +16.6 [-2.8, +44.5] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.3 [0.2, 7.7] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1474.3 [1354.8, 1522.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.4 [0.3, 10.3] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1472.9 [1345.5, 1518.6] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1469.7 [1345.2, 1519.4] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1064.7 [-1118.8, -1029.5] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1473.5 [1347.3, 1524.7] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 855.5 [839.2, 882.2] ms (-32.3/+3.4) n=10 | - | +12.3 [-1.6, +39.6] (1/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1471.8 [1363.8, 1515.5] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1462.6 [1348.9, 1519.5] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| codec-pcmu | good | pass | pass 10/10 | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU (10/10: payload types 8) | - |
| codec-pcma | good | pass | pass 10/10 | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA (10/10: payload types 0) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.8 [0.3, 4.3] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 59878.4 [59849.9, 59939.5] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.5 [0.3, 0.8] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1309.9 [1185.5, 1367.4] ms (-32.3/+3.4) n=10 | - | +10.8 [-4.8, +27.5] (1/10 outside the bar) |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.5 [0.4, 1.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1312.0 [1204.1, 1368.7] ms (-32.3/+3.4) n=10 | - | +6.4 [+0.0, +17.2] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.5 [0.3, 1.3] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 50 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1304.1 [1181.3, 1366.6] ms (-32.3/+3.4) n=10 | - | +10.9 [+0.0, +20.9] |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 2.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1292.9 [1232.1, 1370.1] ms (-32.3/+3.4) n=10 | 2xx offers the call's codec (10/10: no SDP) | +9.4 [+0.0, +30.9] |
| hold-zero | good | pass | pass 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 6.4] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 [0.2, 0.8] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: 2xx to agent RTP: 74.4 [59.2, 81.8] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: RTP clock drift: 1.4 [-2.3, 3.6] ms (-0.4/+0.4) n=10 | - | - |
| hold-zero | ignores-address | fail | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 2.8] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 [0.3, 0.8] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 120 packets) | - |
| codec-change | good | pass | pass 10/10 | end of the question to agent speech: 1310.5 [1230.6, 1372.1] ms (-25.2/+87.6) n=10 | - | +13.2 [-3.2, +28.4] (1/10 outside the bar) |
| codec-change | stale | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) | - |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 849.0 [828.7, 897.4] ms (-52.5/+16.7) n=10 | - | +8.7 [-1.9, +37.4] |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3064.0 [3000.3, 3104.9] ms (-52.5/+16.7) n=10 | agent speaks within 2000 ms (10/10) | +9.3 [-0.7, +58.0] (1/10 outside the bar) |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.3 [0.2, 0.9] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 70.2 [38.5, 104.7] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.2 [0.2, 0.7] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2205.6 [2108.4, 2222.5] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 0.5 [0.4, 1.2] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 4130.4 [3595.9, 5262.1] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (9/10: 1 packets) | - |
| hold | good | pass | flips: pass 9, fail 1 | sendonly hold: re-INVITE to 2xx: 0.5 [0.3, 9.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.3, 1.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 78.8 [35.5, 141.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -1.9 [-57.5, 16.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 0.8] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.2, 1.0] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 80.4 [30.6, 149.3] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3.5 [-24.6, 14.6] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (1/10: ssrc 0xd0e2c1c->0xd0e2c1c, seq 33722->33723, clock -58 ms) | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.5 [0.3, 2.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.5 [0.3, 1.3] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.6 [0.3, 0.7] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.5 [0.3, 1.0] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 116 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 112 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.5 [0.3, 0.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.5 [0.3, 0.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 53.2 [29.7, 139.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -2991.9 [-3017.3, -2978.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 0.8] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.5 [0.3, 1.2] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 77.1 [45.9, 116.8] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -2999.9 [-3015.1, -2991.6] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0xecba28db->0xecba28db, seq 35424->35429, clock -3017 ms); resume from inactive: same RTP stream (10/10: ssrc 0xecba28db->0xecba28db, seq 35572->35573, clock -2997 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 908.7 [867.9, 966.1] ms (-52.5/+16.7) n=10 | - | +9.9 [-13.4, +66.9] (1/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.3 [0.2, 0.7] ms (-0.4/+0.4) n=10<br>digit to agent speech: 867.2 [810.0, 980.3] ms (-52.5/+16.7) n=10 | - | +7.9 [-1.5, +98.6] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.3 [0.2, 32.1] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1484.1 [1364.1, 1514.2] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.4 [0.3, 3.8] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1473.9 [1384.3, 1513.7] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1476.2 [1350.6, 1527.5] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1047.8 [-1076.5, -1025.2] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1474.4 [1354.8, 1553.7] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 878.0 [832.2, 904.1] ms (-52.5/+16.7) n=10 | - | +9.1 [-4.2, +102.5] (2/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1497.5 [1351.5, 1514.0] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 0 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1475.1 [1368.1, 1544.8] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| codec-pcmu | good | pass | pass 10/10 | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU (10/10: payload types 8) | - |
| codec-pcma | good | pass | pass 10/10 | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA (10/10: payload types 0) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.6 [0.4, 2.6] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 59884.1 [59846.2, 59931.9] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.7 [0.6, 8.0] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1342.2 [1168.3, 1432.8] ms (-52.5/+16.7) n=10 | - | +0.0 [-8.6, +27.0] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.5 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1368.8 [1224.9, 1500.2] ms (-52.5/+16.7) n=10 | - | +15.4 [-13.1, +70.9] (2/10 outside the bar) |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.5 [0.3, 0.9] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 131 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.6 [0.3, 4.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1370.6 [1251.8, 1421.2] ms (-52.5/+16.7) n=10 | - | +42.6 [-3.0, +96.4] (4/10 outside the bar) |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 1.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1337.5 [1237.2, 1395.3] ms (-52.5/+16.7) n=10 | 2xx offers the call's codec (10/10: no SDP) | +2.0 [-8.6, +55.3] (1/10 outside the bar) |
| hold-zero | good | pass | pass 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 0.9] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.5 [0.3, 1.2] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: 2xx to agent RTP: 76.0 [35.1, 102.8] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: RTP clock drift: 1.6 [-23.0, 15.7] ms (-0.4/+0.4) n=10 | - | - |
| hold-zero | ignores-address | fail | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.5 [0.3, 1.7] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.4 [0.3, 1.8] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 121 packets) | - |
| codec-change | good | pass | pass 10/10 | end of the question to agent speech: 1327.4 [1212.7, 1411.8] ms (-35.1/+96.9) n=10 | - | +0.0 [-17.0, +73.0] (1/10 outside the bar) |
| codec-change | stale | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) | - |

Every case NOT proven over 10 repeat(s): good passes, bad fails.

Error bars: true value = measured - error, error within

- [-96.9, +35.1] ms: webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech --profiles lte-bad)
- [-88.1, +24.3] ms: webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech)
- [-87.6, +25.2] ms: webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech --profiles lte)
- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-16.7, +52.5] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech --profiles lte-bad)
- [-3.8, +32.9] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech)
- [-3.4, +32.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech --profiles lte)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
