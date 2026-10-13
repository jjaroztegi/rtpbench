### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 810.2 [800.1, 830.4] ms (-32.9/+3.8) n=10 | - | +9.3 [-0.6, +29.5] |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3010.2 [3000.1, 3030.2] ms (-32.9/+3.8) n=10 | agent speaks within 2000 ms (10/10) | +9.5 [-1.0, +29.5] |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.2 [0.2, 0.8] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 19.4 [18.8, 19.9] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.2 [0.2, 0.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2219.4 [2219.1, 2219.5] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 3525.2 [3471.6, 3638.8] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.2, 0.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.3, 2.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 36.1 [32.0, 37.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.0 [-0.0, 0.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.3, 1.6] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 31.3 [23.3, 35.1] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 0.0 [-0.0, 0.0] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.3 [0.3, 0.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.3, 0.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.2, 2.2] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 125 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 125 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.3 [0.3, 3.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.2, 0.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 36.6 [29.0, 39.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3000.0 [-3020.0, -2960.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 34.5 [25.3, 36.4] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3000.0 [-3000.0, -2980.0] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x9e9b63a5->0x9e9b63a5, seq 55620->55621, clock -3000 ms); resume from inactive: same RTP stream (10/10: ssrc 0x9e9b63a5->0x9e9b63a5, seq 55770->55771, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 809.7 [799.4, 849.7] ms (-32.9/+3.8) n=10 | - | +9.6 [-0.6, +49.5] (1/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.2 [0.2, 0.3] ms (-0.4/+0.4) n=10<br>digit to agent speech: 818.3 [798.5, 848.6] ms (-32.9/+3.8) n=10 | - | +17.9 [-1.8, +48.3] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.3 [0.2, 1.2] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1427.2 [1312.0, 1482.5] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.3 [0.2, 1.1] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1436.0 [1304.0, 1484.8] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1425.9 [1317.7, 1482.5] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1000.8 [-1001.6, -1000.7] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1425.3 [1307.9, 1487.7] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 816.2 [795.1, 847.9] ms (-32.9/+3.8) n=10 | - | +15.3 [-5.4, +47.5] (2/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1429.8 [1311.0, 1482.3] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 0 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1428.1 [1299.9, 1477.5] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| codec-pcmu | good | pass | pass 10/10 | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU (10/10: payload types 8) | - |
| codec-pcma | good | pass | pass 10/10 | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA (10/10: payload types 0) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 2.1] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 59957.1 [59912.9, 59984.8] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 1.1] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 855.8 [838.5, 875.3] ms (-32.3/+3.4) n=10 | - | +9.3 [-0.8, +39.8] (1/10 outside the bar) |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3052.6 [3038.5, 3070.4] ms (-32.3/+3.4) n=10 | agent speaks within 2000 ms (10/10) | +9.4 [-0.6, +31.5] |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.2 [0.2, 0.6] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 58.9 [56.6, 64.4] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.2 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2199.9 [2196.6, 2239.8] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 0.4 [0.3, 1.5] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 3553.7 [3461.5, 4163.7] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (10/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.2, 1.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.2, 0.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 76.6 [70.2, 85.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.5 [-1.8, 2.1] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.2, 0.5] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.2, 0.8] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 74.5 [63.5, 80.2] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -1.5 [-5.0, 2.3] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.2, 0.5] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.2, 1.0] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 124 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 123 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.2, 1.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 75.6 [65.8, 79.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -3001.6 [-3004.2, -2998.8] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.2, 0.6] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.3, 1.1] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 74.1 [67.0, 78.8] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3000.8 [-3022.0, -2996.8] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0x8987b60a->0x8987b60a, seq 49340->49341, clock -3001 ms); resume from inactive: same RTP stream (10/10: ssrc 0x8987b60a->0x8987b60a, seq 49490->49491, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 894.6 [874.7, 930.1] ms (-32.3/+3.4) n=10 | - | +9.0 [-3.0, +49.0] (1/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.2 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>digit to agent speech: 856.3 [836.3, 888.6] ms (-32.3/+3.4) n=10 | - | +13.4 [-2.0, +50.1] (1/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.2 [0.2, 0.3] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1466.4 [1356.2, 1526.4] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.3 [0.2, 0.4] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1470.7 [1344.0, 1521.2] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1459.8 [1341.4, 1531.3] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1001.1 [-1001.7, -1000.5] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1478.1 [1354.1, 1518.8] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 857.2 [837.4, 886.4] ms (-32.3/+3.4) n=10 | - | +14.6 [-6.6, +44.2] (2/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1470.6 [1342.3, 1513.5] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 0 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1469.0 [1357.2, 1520.1] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| codec-pcmu | good | pass | pass 10/10 | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU (10/10: payload types 8) | - |
| codec-pcma | good | pass | pass 10/10 | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA (10/10: payload types 0) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 0.6] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 59966.6 [59911.3, 59972.4] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.2, 0.6] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass 10/10 | 200 OK to agent speech: 873.7 [815.2, 890.3] ms (-52.5/+16.7) n=10 | - | +9.4 [-0.9, +55.4] (1/10 outside the bar) |
| greeting | late | fail | fail 10/10 | 200 OK to agent speech: 3057.5 [3010.9, 3105.0] ms (-52.5/+16.7) n=10 | agent speaks within 2000 ms (10/10) | +9.0 [-1.1, +40.1] |
| greeting | silent | fail | fail 10/10 | - | agent speaks first (10/10) | - |
| bye | good | pass | pass 10/10 | BYE to its response: 0.2 [0.2, 0.3] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 46.8 [19.5, 118.3] ms (-0.4/+0.4) n=10 | - | - |
| bye | linger | fail | fail 10/10 | BYE to its response: 0.2 [0.2, 0.5] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 2199.4 [2162.2, 2259.1] ms (-0.4/+0.4) n=10 | agent RTP stops within 500 ms (10/10) | - |
| cancel | good | pass | pass 10/10 | CANCEL to the INVITE's final response: 0.3 [0.3, 0.5] ms (-0.4/+0.4) n=10 | - | - |
| cancel | answers | fail | fail 10/10 | CANCEL to the INVITE's final response: 3584.4 [3496.4, 4231.0] ms (-0.4/+0.4) n=10 | INVITE ended 487 (10/10: SIP/2.0 200 OK); no agent RTP after the CANCEL (9/10: 1 packets) | - |
| hold | good | pass | pass 10/10 | sendonly hold: re-INVITE to 2xx: 0.3 [0.3, 0.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.2, 0.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 78.2 [40.9, 230.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.8 [-14.5, 16.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.4 [0.2, 0.7] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.2, 0.8] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 74.3 [32.7, 109.1] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.5 [-22.9, 18.5] ms (-0.4/+0.4) n=10 | - | - |
| hold | ignore | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 1.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.3 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.3 [0.2, 0.5] ms (-0.4/+0.4) n=10 | sendonly hold: answer recvonly or inactive (10/10: sendrecv); sendonly hold: no agent RTP (10/10: 113 packets); inactive hold: answer inactive (10/10: sendrecv); inactive hold: no agent RTP (10/10: 122 packets) | - |
| hold | clock | fail | fail 10/10 | sendonly hold: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 0.4 [0.3, 0.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 71.0 [33.1, 107.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -2999.5 [-3015.0, -2964.9] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 0.3 [0.3, 1.2] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 0.4 [0.2, 0.8] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 62.4 [29.0, 165.1] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -3000.0 [-3007.7, -2968.7] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (10/10: ssrc 0xe8aca57a->0xe8aca57a, seq 14620->14621, clock -2965 ms); resume from inactive: same RTP stream (10/10: ssrc 0xe8aca57a->0xe8aca57a, seq 14769->14774, clock -2987 ms) | - |
| dtmf-rfc4733 | good | pass | pass 10/10 | digit to agent speech: 917.0 [849.8, 958.6] ms (-52.5/+16.7) n=10 | - | +17.3 [-18.6, +76.8] (3/10 outside the bar) |
| dtmf-rfc4733 | deaf | fail | fail 10/10 | - | agent reacts within 5000 ms (10/10) | - |
| dtmf-info | good | pass | pass 10/10 | INFO to its response: 0.2 [0.2, 0.4] ms (-0.4/+0.4) n=10<br>digit to agent speech: 861.7 [834.5, 900.8] ms (-52.5/+16.7) n=10 | - | +4.1 [-13.6, +76.0] (2/10 outside the bar) |
| dtmf-info | deaf | fail | fail 10/10 | INFO to its response: 0.3 [0.2, 0.4] ms (-0.4/+0.4) n=10 | agent reacts within 5000 ms (10/10) | - |
| refer | good | pass | pass 10/10 | end of the request to REFER: 1477.1 [1300.7, 1530.6] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 0.4 [0.3, 0.7] ms (-0.4/+0.4) n=10 | - | - |
| refer | stays | fail | fail 10/10 | end of the request to REFER: 1475.6 [1367.5, 1525.6] ms (-17.0/+17.0) n=10 | agent hangs up within 10 s (10/10) | - |
| refer | early | fail | fail 10/10 | end of the request to REFER: 1467.3 [1339.2, 1500.3] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: -1000.8 [-1001.9, -1000.4] ms (-0.4/+0.4) n=10 | NOTIFY (SIP/2.0 100 Trying) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (10/10: SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass 10/10 | end of the request to REFER: 1459.3 [1341.7, 1529.1] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 855.0 [842.9, 885.3] ms (-52.5/+16.7) n=10 | - | +6.0 [-17.2, +36.7] (1/10 outside the bar) |
| refer-fail | hangs-up | fail | fail 10/10 | end of the request to REFER: 1470.5 [1377.5, 1535.6] ms (-17.0/+17.0) n=10 | agent keeps the call for 10 s (10/10: BYE 1 ms after it); agent speaks within 5000 ms (10/10) | - |
| refer-fail | silent | fail | fail 10/10 | end of the request to REFER: 1488.3 [1364.0, 1524.0] ms (-17.0/+17.0) n=10 | agent speaks within 5000 ms (10/10) | - |
| codec-pcmu | good | pass | pass 10/10 | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail 10/10 | - | answer has PCMU alone (10/10: 8); agent RTP is PCMU (10/10: payload types 8) | - |
| codec-pcma | good | pass | pass 10/10 | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail 10/10 | - | answer has PCMA alone (10/10: 0); agent RTP is PCMA (10/10: payload types 0) | - |
| timer | good | pass | pass 10/10 | refresh re-INVITE to 2xx: 0.5 [0.3, 1.2] ms (-0.4/+0.4) n=10<br>refresh 2xx to agent BYE: 59953.1 [59912.1, 59980.4] ms (-0.4/+0.4) n=10 | - | - |
| timer | unsupported | fail | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) | - |
| timer | no-expiry | fail | fail 10/10 | refresh re-INVITE to 2xx: 0.4 [0.3, 2.5] ms (-0.4/+0.4) n=10 | agent ends the session in (45, 90] s (10/10) | - |

Every case proven over 10 repeat(s): good passes, bad fails.

Error bars: true value = measured - error, error within

- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-16.7, +52.5] ms: webrtcvad onset, p5..p95, PCMU, lte-bad (calibrate --speech --profiles lte-bad)
- [-3.8, +32.9] ms: webrtcvad onset, p5..p95, PCMU, clean (calibrate --speech)
- [-3.4, +32.3] ms: webrtcvad onset, p5..p95, PCMU, lte (calibrate --speech --profiles lte)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
