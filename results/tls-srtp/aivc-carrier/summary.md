### clean

| case | result | timings, ms (error bar) | failed checks |
| --- | --- | --- | --- |
| greeting | pass | 200 OK to agent speech: 544.0 ms (-64.9/-1.1) | - |
| bye | pass | BYE to its response: 1.6 ms (-0.4/+0.4)<br>BYE to the agent's last RTP: 1.4 ms (-0.4/+0.4) | - |
| cancel | inconclusive | - | CANCEL sent while ringing (final response 3 ms after the first provisional, before a CANCEL) |
| hold | fail | sendonly hold: re-INVITE to 2xx: 3.1 ms (-0.4/+0.4)<br>resume from sendonly: re-INVITE to 2xx: 2.8 ms (-0.4/+0.4)<br>resume from sendonly: 2xx to agent RTP: -0.3 ms (-0.4/+0.4)<br>resume from sendonly: RTP clock drift: -0.0 ms (-0.4/+0.4)<br>inactive hold: re-INVITE to 2xx: 2.6 ms (-0.4/+0.4)<br>resume from inactive: re-INVITE to 2xx: 2.8 ms (-0.4/+0.4)<br>resume from inactive: 2xx to agent RTP: 14.0 ms (-0.4/+0.4)<br>resume from inactive: RTP clock drift: 0.0 ms (-0.4/+0.4) | inactive hold: answer inactive (recvonly) |
| dtmf-rfc4733 | fail | - | telephone-event negotiated |
| dtmf-info | fail | INFO to its response: 30700.8 ms (-0.4/+0.4) | INFO answered 2xx (SIP/2.0 408 Request Timeout); agent reacts within 5000 ms |
| refer | pass | end of the request to REFER: 1503.8 ms (-17.0/+17.0)<br>final NOTIFY to agent BYE: 17.4 ms (-0.4/+0.4) | - |
| refer-fail | fail | end of the request to REFER: 1503.3 ms (-17.0/+17.0) | agent keeps the call for 10 s (BYE 19 ms after it); agent speaks within 5000 ms |
| timer | inconclusive | - | Session-Expires in the 2xx (timers not supported (RFC 4028 9, optional; the caller may refresh alone)) |
| compact-headers | fail | - | call completed (SIP/2.0 500 Server Internal Error) |
| sdp-ssrc | fail | - | call completed (INVITE timed out) |
| late-offer | fail | - | call completed (SIP/2.0 500 Server Internal Error) |
| ptime-30 | pass | end of the question to agent speech: 1531.1 ms (-11.0/+133.0) | - |
| ssrc-change | pass | end of the question to agent speech: 1508.5 ms (-11.0/+133.0) | - |
| reinvite | pass | refresh re-INVITE to 2xx: 2.1 ms (-0.4/+0.4)<br>end of the question to agent speech: 1508.9 ms (-11.0/+133.0) | - |
| reinvite-nosdp | fail | - | 2xx offers the call's codec (no SDP); refresh answered 2xx (SIP/2.0 487 Request Terminated) |


Error bars: true value = measured - error, error within

- [-133.0, +11.0] ms: webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech, seeds 1-5)
- [-17.0, +17.0] ms: caller's labelled end; ±5 dB of label threshold, median (calibrate --speech)
- [-0.4, +0.4] ms: capture times; wire timing max abs error, clean (calibrate)
- [+1.1, +64.9] ms: webrtcvad first onset, p5..p95, PCMA, clean (calibrate --speech, seeds 1-5)

Wall-clock steps during the run: none.

SIP over TLS: TLSv1.3 TLS_AES_256_GCM_SHA384 (18 calls)

SRTP: AES_CM_128_HMAC_SHA1_80 (15 calls), none (3 calls)
SRTP packets that did not authenticate: 0

## Turn latency

Turn latency, ms: caller's labelled end to the agent's first speech (webrtcvad), every turn of every run. True value = measured - error, error within the onset bar; where the caller's speech ends is defined to ±17 ms (label threshold ±5 dB).

| profile | runs | answered | p5 | p50 | p95 | run medians | across a clock step | onset error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 1 | 12/12 | 1504 | 1511 | 1518 | 1511 .. 1511 | 0 | [-133.0, +11.0] webrtcvad onset, p5..p95, PCMA, clean (calibrate --speech, seeds 1-5) |

Each turn: a line of PROFILE/REPEAT/latency/turns.jsonl (results.json holds the cases only; rtpbench check gathers the turns into check.json).

## Barge-in

Barge-in: whether the agent stopped within 2 s of the interjection's onset, and its stop time (ms, gate, wire) when it did, every turn of every run. True value = measured - error, error within the bar (calibrated on hard cuts). Speech ended before (gate): turns left out, the gate having heard the agent's speech end before the onset by more than the bar.

| profile | interjection | runs | stopped | run rates | p5 | p50 | p95 | across a clock step | speech ended before (gate) | stop error bar |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | interrupt | 1 | 2/2 | 100% .. 100% | 108 | 108 | 176 | 0 | 1 | [-84.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in, seeds 1-5) |
| clean | backchannel | 1 | 3/3 | 100% .. 100% | 13 | 23 | 44 | 0 | 1 | [-84.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in, seeds 1-5) |
| clean | cough | 1 | 3/3 | 100% .. 100% | -40 | -9 | 21 | 0 | 0 | [-84.9, +0.0] gate stop time, p5..p95, PCMA, clean (calibrate --barge-in, seeds 1-5) |

Per clip: stopped / turns, over the same turns, and those left out as ended before; interruptions are the caller's lines (--lines), backchannels and coughs the corpus's.

| interjection | clip | words | clean |
| --- | --- | --- | --- |
| interrupt | interrupt-00 |  | 1/1 |
| interrupt | interrupt-01 |  | 0/0, 1 ended before |
| interrupt | interrupt-02 |  | 1/1 |
| backchannel | tts-cori-bc | Yeah | 0/0, 1 ended before |
| backchannel | tts-libritts0-bc | Okay | 1/1 |
| backchannel | tts-ljspeech-bc | Uh-huh | 1/1 |
| backchannel | tts-sharvardf-bc | Vale | 1/1 |
| cough | cough-man-1 |  | 1/1 |
| cough | cough-short-0 |  | 1/1 |
| cough | cough-short-1 |  | 1/1 |

Each turn: a line of PROFILE/REPEAT/barge-in/turns.jsonl (results.json holds the cases only; rtpbench check gathers the turns into check.json).

## Turn latency by part

Turn latency on the mock engine, split where it heard the end of the caller's speech and sent its first audio (one clock with the captures), ms, p50 [p5, p95]: uplink and downlink are the target's; the engine waits 1000 ms of silence and answers 500 ms later by design. Uplink carries the caller's label error (±17 ms), downlink the onset error bar of the profile and codec.

| profile | turns | wire latency | uplink | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 12 | 1511 [1504, 1518] | 0 [-2, 4] | 1501 [1500, 1502] | 8 [3, 17] |

Greeting on the mock engine, ms, p50 [p5, p95]: from the 200 OK on the wire to the target's request for a greeting (negative: asked before answering), the engine's 500 ms, and from its first audio to the agent's speech on the wire (webrtcvad onset bar).

| profile | calls | 200 OK to speech | to the request | engine | downlink |
| --- | --- | --- | --- | --- | --- |
| clean | 1 | 544 [544, 544] | 3 [3, 3] | 501 [501, 501] | 40 [40, 40] |

## RTP pacing

The agent's RTP as the caller received it, ms, median [min, max] over calls: late, p99 of how much later than their timestamps say the packets arrived, against the earliest before them: the jitter buffer a receiver needs to play 99% of them in time; jitter, the RFC 3550 interarrival jitter estimate, its median over each call. On a clean network both are the agent's own pacing (and a carrier's); a profile adds its own.

| profile | calls | late, p99 | jitter |
| --- | --- | --- | --- |
| clean | 14 | 1.1 [1.1, 2.8] | 0.28 [0.03, 0.36] |

Pauses: none; outside a hold, the agent's RTP never went on after stopping for a second or more.

## Engine audio as the caller received it

The mock engine's answers as the caller received them (completed answers in the latency and barge-in calls), median [min, max] over answers. Each piece of speech is aligned with what the mock sent; for 24 kHz audio, that is its interpolation through an ideal 8 kHz converter, so the mock's own resampling is not counted. Samples in packets the network lost are left out. unchanged: answers whose aligned speech came through sample for sample (pauses are not compared). distortion: the audio against what no linear filter of ±4 ms explains; a resampler or band filter would leave G.711's own, about 37 dB. moved: answers where a piece came out 5 ms or more later or earlier than the one before (a pause lengthened or shortened, audio inserted or dropped), and the largest move. gain: least squares. 3.4-4 kHz: that band against 300-3400 Hz, relative to what was sent.

| profile | answers | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB |
| --- | --- | --- | --- | --- | --- | --- |
| clean | 23 | 23 | exact [exact, exact] | 0 | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |

## Caller audio as the engine received it

The caller's lines in the latency and barge-in calls as the mock engine received them, aligned piece by piece with what the caller sent (its own capture, before the network), median [min, max] over lines; the columns as for the engine's audio above. Lost packets are the target's to fill: what it filled them with counts as distortion, and what it left out as moved. above 4 kHz: energy above 4 kHz against 300-3400 Hz in 24 kHz audio (the caller sends none). full scale: lines with samples at full scale. missing 20 ms: the caller's voiced 20 ms with nothing like them within 25 ms in what the engine got, and what came in their place: silence, the 20 ms before again (repeat), or other (also the next audio, where a packet was left out: see moved). appends: the audio each append carried, the median of each call's.

| profile | lines | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB | above 4 kHz, dB | full scale | missing 20 ms | appends, ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 32 | 32 | exact [exact, exact] | 0 | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] |  | 0 | 0.0% | 20 [20, 20] |
