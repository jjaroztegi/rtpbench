### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 810.6 [800.2, 830.2] ms (-63.6/-1.0) n=10 | - | +9.6 [-0.6, +29.5] (3/10 outside the bar) |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3010.2 [3000.2, 3030.3] ms (-63.6/-1.0) n=10 | agent speaks within 2000 ms (10/10) | +9.5 [-0.6, +29.7] (3/10 outside the bar) |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.2 [0.2, 0.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 19.3 [0.9, 20.0] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.2 [0.2, 0.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2219.2 [2218.8, 2219.4] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 4124.3 [3987.6, 4208.4] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 1.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 36.7 [34.1, 37.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.0 [-0.0, 0.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 34.4 [31.7, 35.2] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.0 [-0.0, 0.0] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.3 [0.3, 1.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 36.7 [36.1, 37.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3000.0 [-3000.0, -3000.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 34.3 [33.1, 35.0] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3000.0 [-3000.0, -3000.0] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0xf1f146a6->0xf1f146a6, seq 38322->38323, clock -3000 ms); resume from inactive: same RTP stream (10/10: ssrc 0xf1f146a6->0xf1f146a6, seq 38472->38473, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 809.5 [799.6, 849.6] ms (-63.6/-1.0) n=10 | - | +9.4 [-0.6, +49.5] (1/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.2 [0.2, 0.3] ms (-0.4/+0.4) n=10<br>digit to agent speech: 817.8 [798.7, 849.6] ms (-63.6/-1.0) n=10 | - | +17.4 [-1.6, +49.2] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.2 [0.2, 0.8] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1438.3 [1315.8, 1484.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.3 [0.2, 2.0] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1429.5 [1310.6, 1476.7] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1432.5 [1318.7, 1474.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1030.8 [-1044.6, -1027.0] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1433.5 [1313.9, 1480.2] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 818.7 [797.1, 846.5] ms (-63.6/-1.0) n=10 | - | +18.1 [-3.1, +46.1] (1/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1437.4 [1314.0, 1468.5] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1430.3 [1301.6, 1473.9] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| codec-pcmu | good | pass | pass 10/10 | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU (10/10: payload types 8) | - |
| codec-pcma | good | pass | pass 10/10 | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA (10/10: payload types 0) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.8] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 60008.6 [60002.2, 60013.9] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1226.5 [1105.8, 1286.7] ms (-44.6/+3.2) n=10 | - | +12.2 [+0.0, +27.5] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| large-invite | good | pass | pass 10/10 | end of the question to agent speech: 1226.4 [1104.4, 1287.6] ms (-44.6/+3.2) n=10 | - | +12.2 [+0.0, +27.5] |
| large-invite | udp-only | fail | fail 10/10 | end of the question to agent speech: 1226.6 [1105.7, 1286.6] ms (-44.6/+3.2) n=10 | INVITE over TCP answered 2xx (10/10: ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) | +12.2 [+0.0, +27.5] |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1226.6 [1105.9, 1286.6] ms (-44.6/+3.2) n=10 | - | +12.2 [+0.0, +27.5] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 1.3] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 3 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1226.6 [1105.9, 1286.4] ms (-44.6/+3.2) n=10 | - | +12.2 [+0.0, +27.5] |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1226.7 [1105.8, 1286.5] ms (-44.6/+3.2) n=10 | 2xx offers the call's codec (10/10: no SDP) | +12.2 [+0.0, +27.5] |
| hold-zero | good | pass | pass 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.4 [0.3, 0.7] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: 2xx to agent RTP: 36.6 [35.2, 37.3] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: RTP clock drift: 0.0 [-0.0, 0.0] ms (-0.4/+0.4) n=10 | - | - |
| hold-zero | ignores-address | fail | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 [0.3, 0.8] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) | - |
| codec-change | good | pass | pass 10/10 | end of the question to agent speech: 1237.9 [1125.9, 1286.6] ms (-64.9/-1.1) n=10 | - | +13.0 [+0.0, +27.5] (1/10 outside the bar) |
| codec-change | stale | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) | - |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 849.5 [834.6, 874.6] ms (-67.6/+0.8) n=10 | - | +9.5 [-0.6, +30.7] |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3056.1 [3041.3, 3073.6] ms (-67.6/+0.8) n=10 | agent speaks within 2000 ms (10/10) | +9.5 [-0.6, +29.7] |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.2 [0.2, 0.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 59.3 [54.1, 63.1] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.2 [0.2, 0.3] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2201.2 [2177.4, 2221.9] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 0.3 [0.3, 0.7] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 4054.8 [3980.7, 4144.0] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 76.5 [72.8, 82.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.6 [-3.0, 2.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 74.3 [70.8, 76.1] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -1.0 [-3.2, 1.8] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.3 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.3, 1.3] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.3, 2.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 122 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 76.5 [74.3, 81.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3001.4 [-3004.0, -2998.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 73.8 [70.1, 78.5] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -2999.3 [-3004.1, -2997.0] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0xa1603951->0xa1603951, seq 8288->8289, clock -2998 ms); resume from inactive: same RTP stream (10/10: ssrc 0xa1603951->0xa1603951, seq 8438->8439, clock -3001 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 896.9 [880.5, 923.5] ms (-67.6/+0.8) n=10 | - | +13.9 [-0.9, +47.4] (1/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.2 [0.2, 0.3] ms (-0.4/+0.4) n=10<br>digit to agent speech: 858.4 [837.7, 890.0] ms (-67.6/+0.8) n=10 | - | +12.5 [-2.6, +49.7] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.2 [0.2, 0.3] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1477.2 [1348.7, 1509.9] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.3 [0.3, 1.2] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1468.6 [1349.2, 1529.4] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1474.6 [1347.4, 1512.2] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1028.8 [-1043.0, -1026.2] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1473.0 [1349.4, 1510.8] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 849.4 [839.1, 884.6] ms (-67.6/+0.8) n=10 | - | +9.3 [+0.8, +46.6] |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1470.8 [1344.9, 1515.6] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 0 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1467.6 [1351.7, 1531.5] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| codec-pcmu | good | pass | pass 10/10 | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU (10/10: payload types 8) | - |
| codec-pcma | good | pass | pass 10/10 | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA (10/10: payload types 0) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 60009.2 [60001.2, 60019.6] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1311.7 [1180.3, 1350.0] ms (-43.3/+3.6) n=10 | - | +13.2 [+0.0, +22.6] |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| large-invite | good | pass | pass 10/10 | end of the question to agent speech: 1313.4 [1187.1, 1372.7] ms (-43.3/+3.6) n=10 | - | +9.5 [-0.2, +33.6] |
| large-invite | udp-only | fail | fail 10/10 | end of the question to agent speech: 1311.0 [1189.9, 1362.2] ms (-43.3/+3.6) n=10 | INVITE over TCP answered 2xx (10/10: ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) | +11.5 [+0.0, +32.3] |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1299.7 [1201.9, 1367.4] ms (-43.3/+3.6) n=10 | - | +10.2 [-1.7, +22.8] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.7] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 56 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.8] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1305.2 [1208.9, 1364.1] ms (-43.3/+3.6) n=10 | - | +12.9 [-0.3, +31.9] |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1306.7 [1205.6, 1365.6] ms (-43.3/+3.6) n=10 | 2xx offers the call's codec (10/10: no SDP) | +11.0 [+0.0, +49.8] (1/10 outside the bar) |
| hold-zero | good | pass | pass 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: 2xx to agent RTP: 77.6 [72.4, 81.0] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: RTP clock drift: -0.6 [-3.9, 3.2] ms (-0.4/+0.4) n=10 | - | - |
| hold-zero | ignores-address | fail | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 125 packets) | - |
| codec-change | good | pass | pass 10/10 | end of the question to agent speech: 1304.8 [1206.3, 1362.1] ms (-67.7/+2.5) n=10 | - | +11.4 [-0.9, +26.0] |
| codec-change | stale | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) | - |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 853.8 [826.3, 952.9] ms (-109.8/+11.4) n=10 | - | +9.5 [-0.5, +122.2] (1/10 outside the bar) |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3063.1 [3016.1, 3132.8] ms (-109.8/+11.4) n=10 | agent speaks within 2000 ms (10/10) | +4.8 [-0.5, +49.4] |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.2 [0.2, 0.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 53.0 [27.8, 107.5] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.2 [0.2, 0.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2193.2 [2107.4, 2279.9] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 0.3 [0.3, 0.3] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 3957.6 [3901.5, 4010.9] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 73.7 [37.3, 150.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.6 [-18.2, 20.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.2, 0.3] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 72.1 [35.0, 129.9] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.9 [-23.1, 15.2] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.3, 1.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.2, 0.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.2, 0.3] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 107 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 112 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.3 [0.3, 0.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 75.5 [36.7, 120.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3003.3 [-3016.6, -2987.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.2, 0.3] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 75.8 [35.6, 122.4] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -2997.1 [-3014.8, -2977.1] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x3df89b0d->0x3df89b0d, seq 40035->40038, clock -3000 ms); resume from inactive: same RTP stream (10/10: ssrc 0x3df89b0d->0x3df89b0d, seq 40185->40186, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 905.7 [839.8, 938.9] ms (-109.8/+11.4) n=10 | - | +0.7 [-14.4, +65.0] (2/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.2 [0.2, 0.3] ms (-0.4/+0.4) n=10<br>digit to agent speech: 857.0 [838.6, 898.5] ms (-109.8/+11.4) n=10 | - | +8.3 [-2.4, +56.7] |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.2 [0.2, 0.2] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1496.8 [1329.3, 1544.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.3 [0.2, 3.4] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1488.3 [1368.4, 1518.2] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1475.1 [1366.8, 1525.0] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1025.3 [-1040.4, -1024.0] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1478.4 [1392.0, 1539.8] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 851.9 [821.1, 899.1] ms (-109.8/+11.4) n=10 | - | -2.0 [-17.6, +24.3] (1/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1473.5 [1371.4, 1535.3] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 0 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1461.4 [1334.3, 1514.8] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| codec-pcmu | good | pass | pass 10/10 | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU (10/10: payload types 8) | - |
| codec-pcma | good | pass | pass 10/10 | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA (10/10: payload types 0) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 60014.0 [60003.2, 60019.6] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |
| ssrc-change | good | pass | pass 10/10 | end of the question to agent speech: 1360.7 [1165.7, 1443.4] ms (-60.9/+15.5) n=10 | - | +19.3 [-7.0, +79.5] (2/10 outside the bar) |
| ssrc-change | first-ssrc | fail | fail 10/10 | - | agent replies within 10000 ms (10/10) | - |
| large-invite | good | pass | pass 10/10 | end of the question to agent speech: 1300.3 [1246.8, 1427.5] ms (-60.9/+15.5) n=10 | - | +3.6 [-7.0, +33.6] |
| large-invite | udp-only | fail | fail 10/10 | end of the question to agent speech: 1343.7 [1270.7, 1459.0] ms (-60.9/+15.5) n=10 | INVITE over TCP answered 2xx (10/10: ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) | +3.6 [-3.0, +90.9] (1/10 outside the bar) |
| reinvite | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1343.9 [1179.2, 1462.5] ms (-60.9/+15.5) n=10 | - | +9.2 [-2.5, +58.4] |
| reinvite | one-way | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10 | media undisturbed by the refresh (10/10: agent RTP stops 41 ms after the 2xx); agent replies within 10000 ms (10/10) | - |
| reinvite-nosdp | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1307.3 [1195.9, 1447.6] ms (-60.9/+15.5) n=10 | - | +3.6 [-8.6, +42.3] |
| reinvite-nosdp | no-offer | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1341.3 [1174.6, 1406.7] ms (-60.9/+15.5) n=10 | 2xx offers the call's codec (10/10: no SDP) | -1.2 [-7.0, +46.2] |
| hold-zero | good | pass | pass 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: 2xx to agent RTP: 71.3 [39.0, 119.1] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: RTP clock drift: 1.4 [-13.1, 14.2] ms (-0.4/+0.4) n=10 | - | - |
| hold-zero | ignores-address | fail | fail 10/10 | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 [0.3, 0.7] ms (-0.4/+0.4) n=10<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 [0.3, 0.3] ms (-0.4/+0.4) n=10 | c=0.0.0.0 hold: no agent RTP (10/10: 118 packets) | - |
| codec-change | good | pass | pass 10/10 | end of the question to agent speech: 1357.6 [1265.3, 1474.4] ms (-102.9/+13.1) n=10 | - | +1.6 [-17.0, +30.3] (1/10 outside the bar) |
| codec-change | stale | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA after it (10/10: payload types 0); agent replies within 10000 ms (10/10) | - |

Every case proven over 10 repeat(s): good passes, bad fails.

Error bars: true value = measured - error, error within

- [-131.0, +14.1] ms: webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech, seeds 1-5)
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
