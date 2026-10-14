### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 6, fail 4 | 200 OK to agent speech: 1367.8 [1212.5, 4881.3] ms (-24.3/+88.1) n=10 | agent speaks within 2000 ms (4/10) |
| bye | pass 10/10 | BYE to its response: 1.5 [1.4, 10.2] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 0.6 [-18.2, 8.7] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 7 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 3.2 [1.9, 6.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.3 [1.8, 7.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 8.9 [-0.1, 17.7] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: 0.0 [-0.3, 0.2] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 3.1 [1.9, 36.1] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 4.2 [2.1, 8.7] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 10.5 [4.3, 16.5] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.0 [-0.2, 0.6] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 29903.4 [28948.9, 30556.1] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 408 Request Timeout); agent reacts within 5000 ms (10/10) |
| refer | flips: pass 9, fail 1 | end of the request to REFER: 2133.1 [1387.7, 4140.1] ms (-17.0/+17.0) n=9<br>final NOTIFY to agent BYE: 2054.3 [1137.1, 3657.6] ms (-0.4/+0.4) n=9 | agent transfers (REFER) (1/10) |
| refer-fail | fail 10/10 | end of the request to REFER: 1565.5 [1447.3, 1874.3] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 1311.5 [424.9, 1659.9] ms (-24.3/+88.1) n=6 | agent keeps the call for 10 s (10/10: BYE 3524 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| compact-headers | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) |
| sdp-ssrc | fail 10/10 | - | call completed (10/10: INVITE timed out) |
| late-offer | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1046.9 [977.7, 1138.1] ms (-24.3/+88.1) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1004.2 [958.5, 1149.6] ms (-24.3/+88.1) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 2.3 [1.7, 9.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1049.1 [947.6, 4609.4] ms (-24.3/+88.1) n=10 | - |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 9, fail 1 | 200 OK to agent speech: 1351.6 [1194.7, 3376.9] ms (-25.2/+87.6) n=10 | agent speaks within 2000 ms (1/10) |
| bye | pass 10/10 | BYE to its response: 1.9 [1.0, 7.0] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 37.6 [18.0, 48.7] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 11 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.3 [1.8, 3.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 3.1 [1.8, 14.3] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 48.3 [40.3, 64.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.3 [-5.5, 5.7] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 3.0 [1.7, 7.7] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.4 [1.6, 3.9] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 48.6 [38.7, 59.4] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -1.3 [-37.6, 3.7] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 29612.2 [29008.4, 30446.2] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 408 Request Timeout); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1608.5 [1486.5, 4227.7] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1833.5 [1326.7, 2315.0] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1901.5 [1662.6, 6494.1] ms (-17.0/+17.0) n=9<br>failure NOTIFY to agent speech: 497.9 [70.6, 1694.5] ms (-25.2/+87.6) n=6 | agent keeps the call for 10 s (9/10: BYE 2594 ms after it); agent speaks within 5000 ms (9/10); agent transfers (REFER) (1/10) |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1139.4 [1027.8, 4457.7] ms (-25.2/+87.6) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1080.2 [969.9, 2262.9] ms (-25.2/+87.6) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 3.0 [1.7, 7.2] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1155.3 [1002.5, 3191.4] ms (-25.2/+87.6) n=10 | - |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 7, fail 3 | 200 OK to agent speech: 1398.9 [1279.2, 6021.7] ms (-35.1/+96.9) n=10 | agent speaks within 2000 ms (3/10) |
| bye | flips: pass 9, inconclusive 1 | BYE to its response: 1.3 [0.9, 6.7] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 23.3 [-20.1, 43.2] ms (-0.4/+0.4) n=10 | agent was talking at the BYE (1/10) |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 13 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 2.6 [2.1, 8.0] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 2.6 [1.8, 13.6] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 52.9 [-4.9, 63.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.3 [-27.5, 25.7] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 2.4 [1.7, 4.2] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 2.8 [1.7, 6.1] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 57.9 [10.1, 130.9] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: 2.5 [-25.3, 11.0] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 29691.3 [29276.4, 30274.8] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 408 Request Timeout); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 2023.5 [1486.6, 2432.8] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1991.4 [1475.8, 3230.7] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 1573.1 [1437.5, 5114.0] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 687.0 [445.9, 1094.4] ms (-35.1/+96.9) n=4 | agent keeps the call for 10 s (10/10: BYE 1398 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1158.6 [1019.5, 6024.7] ms (-35.1/+96.9) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1119.8 [1014.8, 1447.0] ms (-35.1/+96.9) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 3.1 [2.0, 28.3] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1155.9 [1009.2, 1255.7] ms (-35.1/+96.9) n=10 | - |


Error bars: true value = measured - error, error within

- [-96.9, +35.1] ms: webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech --profiles lte-bad)
- [-88.1, +24.3] ms: webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech)
- [-87.6, +25.2] ms: webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech --profiles lte)
- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
