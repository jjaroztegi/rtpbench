### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 7, fail 3 | 200 OK to agent speech: 1743.2 [1363.5, 2879.1] ms (-24.3/+88.1) n=10 | agent speaks within 2000 ms (3/10) |
| bye | pass 10/10 | BYE to its response: 3.0 [2.0, 17.8] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: -1.6 [-13.3, 8.3] ms (-0.4/+0.4) n=10 | - |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 51 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 7.8 [2.7, 509.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 13.8 [2.4, 47.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 2.8 [-0.9, 49.5] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.1 [-69.6, 0.3] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 8.9 [2.7, 19.7] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 14.2 [4.1, 47.9] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 8.4 [-0.4, 49.6] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.2 [-0.5, 1.1] ms (-0.4/+0.4) n=10 | resume from sendonly: same RTP stream (2/10: ssrc 0x7f3cc88c->0x7f3cc88c, seq 8883->8899, clock +0 ms); inactive hold: answer inactive (10/10: recvonly) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (9/10); call completed (1/10: SIP/2.0 500 Server Internal Error) |
| dtmf-info | fail 10/10 | INFO to its response: 29495.5 [28750.0, 30786.9] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 408 Request Timeout); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 1905.8 [1600.0, 4724.2] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1456.9 [30.0, 3351.2] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 2130.3 [1622.9, 7896.0] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 484.4 [153.8, 2436.9] ms (-24.3/+88.1) n=9 | agent keeps the call for 10 s (10/10: BYE 4478 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| compact-headers | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) |
| sdp-ssrc | fail 10/10 | - | call completed (10/10: INVITE timed out) |
| late-offer | fail 10/10 | - | call completed (10/10: SIP/2.0 500 Server Internal Error) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1246.2 [1057.4, 2153.7] ms (-24.3/+88.1) n=10 | - |
| ssrc-change | flips: pass 9, fail 1 | end of the question to agent speech: 2632.7 [951.5, 7260.3] ms (-24.3/+88.1) n=9 | agent replies within 10000 ms (1/10) |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 9.1 [2.8, 27.7] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1126.0 [963.3, 1228.3] ms (-24.3/+88.1) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |

### lte

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 6, fail 4 | 200 OK to agent speech: 1839.5 [1343.5, 2910.9] ms (-25.2/+87.6) n=10 | agent speaks within 2000 ms (4/10) |
| bye | pass 10/10 | BYE to its response: 3.7 [1.7, 40.3] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 42.5 [17.8, 62.2] ms (-0.4/+0.4) n=10 | - |
| cancel | flips: inconclusive 9, fail 1 | CANCEL to the INVITE's final response: 46.9 ms (-0.4/+0.4) n=1 | CANCEL sent while ringing (9/10: final response 93 ms after the first provisional, before a CANCEL); INVITE ended 487 (1/10: SIP/2.0 200 OK) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 10.4 [3.2, 169.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 18.3 [2.7, 176.8] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 45.1 [34.0, 62.1] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -0.1 [-76.8, 12.0] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 9.8 [1.9, 85.1] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 27.0 [7.1, 57.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 43.8 [32.5, 75.5] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -1.3 [-5.6, 2.2] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly); resume from sendonly: same RTP stream (1/10: ssrc 0x1ce1638e->0x1ce1638e, seq 8023->8025, clock -77 ms) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 29932.3 [29295.5, 30427.6] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 408 Request Timeout); agent reacts within 5000 ms (10/10) |
| refer | flips: pass 8, fail 2 | end of the request to REFER: 1836.3 [1494.8, 2188.7] ms (-17.0/+17.0) n=8<br>final NOTIFY to agent BYE: 1450.8 [530.5, 2892.6] ms (-0.4/+0.4) n=8 | agent transfers (REFER) (2/10) |
| refer-fail | fail 10/10 | end of the request to REFER: 1995.8 [1589.8, 6651.5] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 231.2 [6.6, 2192.2] ms (-25.2/+87.6) n=7 | agent keeps the call for 10 s (10/10: BYE 607 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1311.0 [1178.7, 4198.7] ms (-25.2/+87.6) n=10 | - |
| ssrc-change | flips: pass 9, fail 1 | end of the question to agent speech: 1297.9 [1065.7, 8096.3] ms (-25.2/+87.6) n=9 | agent replies within 10000 ms (1/10) |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 8.7 [1.9, 35.9] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1234.3 [1133.4, 3712.3] ms (-25.2/+87.6) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |

### lte-bad

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | flips: pass 6, fail 4 | 200 OK to agent speech: 1931.5 [1418.0, 3043.5] ms (-35.1/+96.9) n=9 | agent speaks within 2000 ms (3/10); agent speaks first (1/10) |
| bye | flips: pass 9, inconclusive 1 | BYE to its response: 2.8 [1.0, 109.0] ms (-0.4/+0.4) n=10<br>BYE to the agent's last RTP: 59.9 [-25.4, 110.4] ms (-0.4/+0.4) n=10 | agent was talking at the BYE (1/10) |
| cancel | inconclusive 10/10 | - | CANCEL sent while ringing (10/10: final response 46 ms after the first provisional, before a CANCEL) |
| hold | fail 10/10 | sendonly hold: re-INVITE to 2xx: 7.3 [2.6, 14.9] ms (-0.4/+0.4) n=10<br>resume from sendonly: re-INVITE to 2xx: 10.5 [4.0, 55.2] ms (-0.4/+0.4) n=10<br>resume from sendonly: 2xx to agent RTP: 40.7 [23.5, 97.4] ms (-0.4/+0.4) n=10<br>resume from sendonly: RTP clock drift: -6.7 [-52.0, 10.3] ms (-0.4/+0.4) n=10<br>inactive hold: re-INVITE to 2xx: 8.0 [2.2, 25.4] ms (-0.4/+0.4) n=10<br>resume from inactive: re-INVITE to 2xx: 12.1 [2.7, 67.4] ms (-0.4/+0.4) n=10<br>resume from inactive: 2xx to agent RTP: 53.8 [-2.6, 102.6] ms (-0.4/+0.4) n=10<br>resume from inactive: RTP clock drift: -0.2 [-12.1, 15.3] ms (-0.4/+0.4) n=10 | inactive hold: answer inactive (10/10: recvonly); resume from sendonly: same RTP stream (1/10: ssrc 0xdb6465->0xdb6465, seq 2967->2968, clock -52 ms) |
| dtmf-rfc4733 | fail 10/10 | - | telephone-event negotiated (10/10) |
| dtmf-info | fail 10/10 | INFO to its response: 29869.8 [29334.5, 30580.1] ms (-0.4/+0.4) n=10 | INFO answered 2xx (10/10: SIP/2.0 408 Request Timeout); agent reacts within 5000 ms (10/10) |
| refer | pass 10/10 | end of the request to REFER: 4306.0 [1714.4, 10610.9] ms (-17.0/+17.0) n=10<br>final NOTIFY to agent BYE: 1545.2 [11.1, 2789.4] ms (-0.4/+0.4) n=10 | - |
| refer-fail | fail 10/10 | end of the request to REFER: 2518.4 [1511.9, 7822.3] ms (-17.0/+17.0) n=10<br>failure NOTIFY to agent speech: 194.6 [19.4, 493.3] ms (-35.1/+96.9) n=8 | agent keeps the call for 10 s (10/10: BYE 2541 ms after it); agent speaks within 5000 ms (10/10) |
| timer | fail 10/10 | - | Session-Expires in the 2xx (10/10: timers not supported) |
| ptime-30 | pass 10/10 | end of the question to agent speech: 1263.9 [1155.7, 1892.3] ms (-35.1/+96.9) n=10 | - |
| ssrc-change | pass 10/10 | end of the question to agent speech: 1506.9 [1101.7, 2544.7] ms (-35.1/+96.9) n=10 | - |
| reinvite | pass 10/10 | refresh re-INVITE to 2xx: 18.9 [2.6, 41.1] ms (-0.4/+0.4) n=10<br>end of the question to agent speech: 1224.1 [1092.2, 3544.7] ms (-35.1/+96.9) n=10 | - |
| reinvite-nosdp | fail 10/10 | - | 2xx offers the call's codec (10/10: no SDP); refresh answered 2xx (10/10: SIP/2.0 487 Request Terminated) |


Error bars: true value = measured - error, error within

- [-96.9, +35.1] ms: webrtcvad onset, p5..p95, PCMA, lte-bad (calibrate --speech --profiles lte-bad)
- [-88.1, +24.3] ms: webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech)
- [-87.6, +25.2] ms: webrtcvad onset, p5..p95, PCMA, lte (calibrate --speech --profiles lte)
- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
