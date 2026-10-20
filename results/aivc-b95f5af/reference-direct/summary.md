### clean

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 830.1 ms (-63.6/-1.0) | - | +29.5 |
| greeting | late | fail | fail | 200 OK to agent speech: 3030.2 ms (-63.6/-1.0) | agent speaks within 2000 ms | +29.5 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 19.4 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2219.4 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 0.3 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3938.1 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 36.6 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: 0.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 34.1 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -0.0 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (125 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (125 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 35.9 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -3000.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 32.8 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3000.0 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0xa0b6225f->0xa0b6225f, seq 4316->4317, clock -3000 ms); resume from inactive: same RTP stream (ssrc 0xa0b6225f->0xa0b6225f, seq 4466->4467, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 829.5 ms (-63.6/-1.0) | - | +29.4 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.2 ms (-0.4/+0.4)<br>digit to agent speech: 828.5 ms (-63.6/-1.0) | - | +28.1 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.2 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| refer | good | pass | pass | end of the request to REFER: 1311.6 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 0.2 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1314.1 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1310.3 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1025.9 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1313.2 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 821.5 ms (-63.6/-1.0) | - | +21.4 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1310.1 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 0 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1309.8 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| codec-pcmu | good | pass | pass | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail | - | answer has PCMU alone (8); agent RTP is PCMU (payload types 8) | - |
| codec-pcma | good | pass | pass | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail | - | answer has PCMA alone (0); agent RTP is PCMA (payload types 0) | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60016.2 ms (-0.4/+0.4) | - | - |
| timer | unsupported | fail | fail | - | Session-Expires in the 2xx (timers not supported) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1095.9 ms (-44.6/+3.2) | - | +17.5 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| large-invite | good | pass | pass | end of the question to agent speech: 1095.9 ms (-44.6/+3.2) | - | +17.5 |
| large-invite | udp-only | fail | fail | end of the question to agent speech: 1106.0 ms (-44.6/+3.2) | INVITE over TCP answered 2xx (ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) | +27.5 |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1105.8 ms (-44.6/+3.2) | - | +27.5 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 4 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1096.0 ms (-44.6/+3.2) | - | +17.5 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>end of the question to agent speech: 1105.9 ms (-44.6/+3.2) | 2xx offers the call's codec (no SDP) | +27.5 |
| hold-zero | good | pass | pass | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: 2xx to agent RTP: 37.7 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: RTP clock drift: -0.0 ms (-0.4/+0.4) | - | - |
| hold-zero | ignores-address | fail | fail | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | c=0.0.0.0 hold: no agent RTP (125 packets) | - |
| codec-change | good | pass | pass | end of the question to agent speech: 1126.0 ms (-64.9/-1.1) | - | +27.5 |
| codec-change | stale | fail | fail | - | answer has PCMA alone (0); agent RTP is PCMA after it (payload types 0); agent replies within 10000 ms | - |

### lte

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 868.9 ms (-67.6/+0.8) | - | +27.0 |
| greeting | late | fail | fail | 200 OK to agent speech: 3099.6 ms (-67.6/+0.8) | agent speaks within 2000 ms | +0.0 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 55.1 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2218.7 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 0.3 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3936.0 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 80.4 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: 1.7 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 73.8 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: 0.0 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (124 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (124 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 78.6 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -3004.8 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 79.1 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -2999.8 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x2ed66851->0x2ed66851, seq 45366->45367, clock -3005 ms); resume from inactive: same RTP stream (ssrc 0x2ed66851->0x2ed66851, seq 45516->45517, clock -3000 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 899.8 ms (-67.6/+0.8) | - | +22.8 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.2 ms (-0.4/+0.4)<br>digit to agent speech: 864.6 ms (-67.6/+0.8) | - | +23.8 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.2 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| refer | good | pass | pass | end of the request to REFER: 1351.0 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 0.2 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1354.2 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1351.3 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1024.9 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1350.8 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 859.8 ms (-67.6/+0.8) | - | +20.0 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1353.3 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 0 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1348.9 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| codec-pcmu | good | pass | pass | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail | - | answer has PCMU alone (8); agent RTP is PCMU (payload types 8) | - |
| codec-pcma | good | pass | pass | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail | - | answer has PCMA alone (0); agent RTP is PCMA (payload types 0) | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60003.3 ms (-0.4/+0.4) | - | - |
| timer | unsupported | fail | fail | - | Session-Expires in the 2xx (timers not supported) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1189.2 ms (-43.3/+3.6) | - | +26.2 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| large-invite | good | pass | pass | end of the question to agent speech: 1181.7 ms (-43.3/+3.6) | - | +23.1 |
| large-invite | udp-only | fail | fail | end of the question to agent speech: 1179.6 ms (-43.3/+3.6) | INVITE over TCP answered 2xx (ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) | +19.6 |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1154.9 ms (-43.3/+3.6) | - | +12.5 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 54 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1166.6 ms (-43.3/+3.6) | - | +22.3 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1193.6 ms (-43.3/+3.6) | 2xx offers the call's codec (no SDP) | +17.8 |
| hold-zero | good | pass | pass | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: 2xx to agent RTP: 72.7 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: RTP clock drift: -3.8 ms (-0.4/+0.4) | - | - |
| hold-zero | ignores-address | fail | fail | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | c=0.0.0.0 hold: no agent RTP (124 packets) | - |
| codec-change | good | pass | pass | end of the question to agent speech: 1202.4 ms (-67.7/+2.5) | - | +21.2 |
| codec-change | stale | fail | fail | - | answer has PCMA alone (0); agent RTP is PCMA after it (payload types 0); agent replies within 10000 ms | - |

### lte-bad

| case | agent | expected | result | timings, ms (error bar) | failed checks | measured - truth, ms |
| --- | --- | --- | --- | --- | --- | --- |
| greeting | good | pass | pass | 200 OK to agent speech: 846.8 ms (-109.8/+11.4) | - | +16.6 |
| greeting | late | fail | fail | 200 OK to agent speech: 3057.1 ms (-109.8/+11.4) | agent speaks within 2000 ms | +20.2 |
| greeting | silent | fail | fail | - | agent speaks first | - |
| bye | good | pass | pass | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 74.9 ms (-0.4/+0.4) | - | - |
| bye | linger | fail | fail | BYE to its response: 0.2 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 2170.8 ms (-0.4/+0.4) | agent RTP stops within 500 ms | - |
| cancel | good | pass | pass | CANCEL to the INVITE's final response: 0.3 ms (-0.4/+0.4) | - | - |
| cancel | answers | fail | fail | CANCEL to the INVITE's final response: 3952.0 ms (-0.4/+0.4) | INVITE ended 487 (SIP/2.0 200 OK); no agent RTP after the CANCEL (1 packets) | - |
| hold | good | pass | pass | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 110.1 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -24.2 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 85.6 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -15.1 ms (-0.4/+0.4) | - | - |
| hold | ignore | fail | fail | sendonly hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | sendonly hold: answer recvonly or inactive (sendrecv); sendonly hold: no agent RTP (116 packets); inactive hold: answer inactive (sendrecv); inactive hold: no agent RTP (121 packets) | - |
| hold | clock | fail | fail | sendonly hold: re-INVITE to 2xx: 0.4 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: 62.5 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -3000.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 45.5 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: -3004.0 ms (-0.4/+0.4) | resume from sendonly: same RTP stream (ssrc 0x1408a168->0x1408a168, seq 17906->17907, clock -3000 ms); resume from inactive: same RTP stream (ssrc 0x1408a168->0x1408a168, seq 18056->18057, clock -3004 ms) | - |
| dtmf-rfc4733 | good | pass | pass | digit to agent speech: 941.9 ms (-109.8/+11.4) | - | +32.4 |
| dtmf-rfc4733 | deaf | fail | fail | - | agent reacts within 5000 ms | - |
| dtmf-info | good | pass | pass | INFO to its response: 0.2 ms (-0.4/+0.4)<br>digit to agent speech: 888.2 ms (-109.8/+11.4) | - | +66.9 |
| dtmf-info | deaf | fail | fail | INFO to its response: 0.2 ms (-0.4/+0.4) | agent reacts within 5000 ms | - |
| refer | good | pass | pass | end of the request to REFER: 1348.6 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 0.3 ms (-0.4/+0.4) | - | - |
| refer | stays | fail | fail | end of the request to REFER: 1350.7 ms (-17.0/+17.0) | agent hangs up within 10 s | - |
| refer | early | fail | fail | end of the request to REFER: 1353.6 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: -1025.3 ms (-0.4/+0.4) | NOTIFY (SIP/2.0 100 Trying) answered 2xx (SIP/2.0 481 Subscription Does Not Exist); NOTIFY (SIP/2.0 200 OK) answered 2xx (SIP/2.0 481 Subscription Does Not Exist) | - |
| refer-fail | good | pass | pass | end of the request to REFER: 1371.7 ms (-17.0/+17.0)<br>failure NOTIFY to agent speech: 837.8 ms (-109.8/+11.4) | - | +19.1 |
| refer-fail | hangs-up | fail | fail | end of the request to REFER: 1348.3 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 0 ms after it); agent speaks within 5000 ms | - |
| refer-fail | silent | fail | fail | end of the request to REFER: 1349.9 ms (-17.0/+17.0) | agent speaks within 5000 ms | - |
| codec-pcmu | good | pass | pass | - | - | - |
| codec-pcmu | pcma-anyway | fail | fail | - | answer has PCMU alone (8); agent RTP is PCMU (payload types 8) | - |
| codec-pcma | good | pass | pass | - | - | - |
| codec-pcma | pcmu-anyway | fail | fail | - | answer has PCMA alone (0); agent RTP is PCMA (payload types 0) | - |
| timer | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>refresh 2xx to agent BYE: 60013.9 ms (-0.4/+0.4) | - | - |
| timer | unsupported | fail | fail | - | Session-Expires in the 2xx (timers not supported) | - |
| timer | no-expiry | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | agent ends the session in (45, 90] s | - |
| ssrc-change | good | pass | pass | end of the question to agent speech: 1201.9 ms (-60.9/+15.5) | - | -3.7 |
| ssrc-change | first-ssrc | fail | fail | - | agent replies within 10000 ms | - |
| large-invite | good | pass | pass | end of the question to agent speech: 1182.8 ms (-60.9/+15.5) | - | -2.5 |
| large-invite | udp-only | fail | fail | end of the question to agent speech: 1225.8 ms (-60.9/+15.5) | INVITE over TCP answered 2xx (ConnectionRefusedError: [Errno 111] Connection refused; over UDP then: SIP/2.0 200 OK) | +4.4 |
| reinvite | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1154.0 ms (-60.9/+15.5) | - | +46.7 |
| reinvite | one-way | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | media undisturbed by the refresh (agent RTP stops 98 ms after the 2xx); agent replies within 10000 ms | - |
| reinvite-nosdp | good | pass | pass | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1267.7 ms (-60.9/+15.5) | - | -12.5 |
| reinvite-nosdp | no-offer | fail | fail | refresh re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>end of the question to agent speech: 1196.8 ms (-60.9/+15.5) | 2xx offers the call's codec (no SDP) | +57.4 |
| hold-zero | good | pass | pass | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: 2xx to agent RTP: 97.0 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: RTP clock drift: 7.9 ms (-0.4/+0.4) | - | - |
| hold-zero | ignores-address | fail | fail | c=0.0.0.0 hold: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4)<br>resume from c=0.0.0.0: re-INVITE to 2xx: 0.3 ms (-0.4/+0.4) | c=0.0.0.0 hold: no agent RTP (116 packets) | - |
| codec-change | good | pass | pass | end of the question to agent speech: 1193.1 ms (-102.9/+13.1) | - | +4.1 |
| codec-change | stale | fail | fail | - | answer has PCMA alone (0); agent RTP is PCMA after it (payload types 0); agent replies within 10000 ms | - |

Every case proven over 1 repeat(s): good passes, bad fails.

Error bars: true value = measured - error, error within

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

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 16 | 0.1 [0.1, 5.8] | 0.02 [0.01, 0.02] |
| lte | 16 | 17.0 [11.7, 19.2] | 3.23 [2.49, 3.79] |
| lte-bad | 16 | 105.9 [72.9, 115.3] | 20.16 [16.03, 20.78] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.
