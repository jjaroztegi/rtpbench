# Asterisk + AVA over SIP: AudioSocket, ExternalMedia and WebSocket

2026-11-03: Asterisk 22.8 (`chan_pjsip`) with AVA v7.6.4 (Asterisk AI Voice Agent), the
[`ava` target](../../docs/targets.md), on the [mock engine](../../docs/targets.md#mock-engine),
called direct and through the [carrier](../../docs/targets.md#carrier), under three network
profiles, 10 repeats each. AVA takes the call's audio from Asterisk over AudioSocket, as upstream
ships it, over ExternalMedia (RTP), or over Asterisk's WebSocket channel (`chan_websocket`); its
golden configuration turns on an egress pacer. All three transports ran with the pacer, and
AudioSocket and WebSocket without it. rtpbench v0.3.0 ran it (image `rtpbench:12ddda5e7bf9`; the
git tag `ava-transports-wave` is that commit). Summaries, records and reports are in this folder,
judged again by the code of the commit that added it; the raw run directories are
[archived](#raw-runs).

[tvbench](https://github.com/ictinnovations/telephony-voice-agent-benchmark) measures an agent by
standing in for Asterisk over a local AudioSocket: "Loopback is not a network. Add jitter and loss
yourself if that is what you want to know." Here Asterisk and the network stay in front of the
agent: the caller's SIP and RTP cross netem, and with `--carrier` OpenSIPS and rtpengine, before
the audio reaches AVA.

```sh
P="--profiles clean,lte,lte-bad --runs 10"
CARRIER=greeting,bye,cancel,hold,dtmf-rfc4733,dtmf-info,refer,refer-fail,timer,ptime-30,ssrc-change,reinvite,reinvite-nosdp,compact-headers,sdp-ssrc,late-offer
for t in audiosocket externalmedia websocket; do
  AVA_TRANSPORT=$t uv run --extra vad rtpbench target ava --mock $P
  AVA_TRANSPORT=$t uv run --extra vad rtpbench target ava --mock --carrier $P --only $CARRIER
done
for t in audiosocket websocket; do
  AVA_TRANSPORT=$t AVA_EGRESS_PACER=false uv run --extra vad rtpbench target ava --mock --only latency,barge-in $P
done
uv run --extra vad rtpbench cases --profiles clean,lte,lte-bad --runs 1
uv run --extra vad rtpbench cases --carrier --profiles clean,lte,lte-bad --runs 1
uv run rtpbench calibrate
uv run rtpbench calibrate --carrier
```

Conditions: the [baseline](../baseline)'s host, 16 CPUs, kernel 6.8.0-147-generic, CPU governor
`performance`, Docker 29.9.1; the mock engine waits 1000 ms of silence and answers 500 ms later;
the carrier is OpenSIPS 3.6.9 and rtpengine, as in the baseline. The sets ran four at a time, in
the order above, then the reference agent's proofs, then the calibrations alone: 10 h 7 min. The
load average stayed between 0.6 and 10.0; 0 clock steps. The reference agent got the expected
verdict in 153 of 153 calls direct and 117 of 117 through the carrier, and wire timing against
its truth stayed exact (max abs 0.00 ms) in every profile direct, and within 0.12 ms through the
carrier.

## Verdicts

| case | AudioSocket, direct | ExternalMedia, direct | WebSocket, direct | AudioSocket, carrier | ExternalMedia, carrier | WebSocket, carrier |
| --- | --- | --- | --- | --- | --- | --- |
| `greeting` | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 |
| `bye` | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 |
| `cancel` | inconclusive 30/30 | inconclusive 30/30 | inconclusive 30/30 | inconclusive 30/30 | inconclusive 30/30 | inconclusive 30/30 |
| `hold` | inconclusive 30/30 | inconclusive 30/30 | **fail** 30/30 | inconclusive 30/30 | inconclusive 30/30 | **fail** 30/30 |
| `hold-zero` | inconclusive 30/30 | inconclusive 30/30 | **fail** 30/30 | | | |
| `dtmf-rfc4733` | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 |
| `dtmf-info` | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 |
| `refer` | flips: pass 29, fail 1 | pass 30/30 | pass 30/30 | flips: pass 29, fail 1 | pass 30/30 | pass 30/30 |
| `refer-fail` | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 |
| `refer-lost` | flips: pass 29, fail 1 | pass 30/30 | pass 30/30 | | | |
| `codec-pcmu` | pass 30/30 | pass 30/30 | pass 30/30 | | | |
| `codec-pcma` | pass 30/30 | pass 30/30 | pass 30/30 | | | |
| `codec-change` | pass 30/30 | pass 30/30 | pass 30/30 | | | |
| `timer` | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 |
| `ssrc-change` | flips: pass 29, fail 1 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 |
| `large-invite` | pass 30/30 | pass 30/30 | pass 30/30 | | | |
| `reinvite` | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 |
| `reinvite-nosdp` | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 |
| `bye-lost` | flips: pass 29, inconclusive 1 | pass 30/30 | pass 30/30 | | | |
| `invite-retransmit` | pass 30/30 | pass 30/30 | pass 30/30 | | | |
| `compact-headers` | | | | pass 30/30 | pass 30/30 | pass 30/30 |
| `sdp-ssrc` | | | | pass 30/30 | pass 30/30 | pass 30/30 |
| `late-offer` | | | | flips: pass 29, fail 1 | pass 30/30 | pass 30/30 |
| `ptime-30` | | | | pass 30/30 | pass 30/30 | pass 30/30 |

- `cancel` is inconclusive: AVA answers 4-7 ms after its first provisional response, so no CANCEL
  can arrive while it rings.
- `hold` and `hold-zero` depend on the transport. Over AudioSocket and ExternalMedia, AVA sends
  RTP only while it speaks, and it said nothing in the second before the hold, so whether media
  resumes cannot be judged. Over WebSocket, Asterisk sends RTP for the whole call, silence
  between answers included, and goes on sending it to a held caller.
- A digit reaches the engine by neither method; Asterisk accepts the INFO with a 2xx.
- `refer`: the REFER goes out about 6 s after the request: the mock calls the transfer tool, AVA
  asks it for a reply, plays it, and hands the call to the dialplan's `Transfer()`. `refer-fail`:
  the dialplan ends the call after `Transfer()` whatever its outcome, so the failure never
  reaches the engine and the caller is hung up on.
- `timer`: AVA hangs up 13 s after the session refresh, about 59 s into a call where the caller
  stays silent (its no-input check), before the session could expire.
- Every flip is a call where the engine got silence instead of the caller,
  [below](#silence-instead-of-the-caller).

## Turn latency

Turn latency, ms, p50 [p5, p95], every turn of the latency calls, and AVA's share of it on the
way out (downlink, the mock's first audio to the agent's speech on the wire, p50; on the way in
it is 1 ms on a clean network, 37-42 ms under `lte` and `lte-bad`, the profiles' own delay):

| set | clean | lte | lte-bad | downlink: clean | lte | lte-bad |
| --- | --- | --- | --- | --- | --- | --- |
| AudioSocket | 1589 [1469, 1594] | 1662 [1547, 1678] | 1652 [1510, 1733] | 87 | 123 | 119 |
| ExternalMedia | 1588 [1469, 1593] | 1663 [1553, 1679] | 1662 [1522, 1737] | 88 | 123 | 115 |
| WebSocket | 1559 [1449, 1580] | 1642 [1525, 1661] | 1657 [1535, 1713] | 60 | 103 | 110 |
| AudioSocket, pacer off | 1570 [1445, 1582] | 1652 [1525, 1664] | 1634 [1504, 1704] | 72 | 112 | 95 |
| WebSocket, pacer off | 1561 [1449, 1599] | 1639 [1529, 1681] | 1650 [1532, 1715] | 60 | 100 | 109 |

The engine's share is the mock's fixed 1501 ms. On a clean network AVA adds 87-88 ms to a turn
over AudioSocket and ExternalMedia, 19 ms of it the pacer's, and 58-60 ms over WebSocket, with or
without the pacer; in the baseline, AI Voice Connector CE adds 11 ms and LiveKit 332 ms. These
are the median turn less the engine's 1501 ms; the [front page](../../README.md) adds the medians
of uplink and downlink instead. The greeting is heard 688-748 ms after the 200 OK over
AudioSocket and ExternalMedia, 787-824 ms over WebSocket, where AVA asks the engine for it 240 ms
after answering instead of 144-151.

## The pacer cuts every answer short

With the pacer on, AVA stops sending each answer before its end, over every transport. With the
pacer off an answer reaches the caller as 192-195 packets of sound; with it, as 162-166 over
AudioSocket and ExternalMedia, in all 130 answers of the clean latency calls of each set, the
greeting included. The last 0.6 s of speech is missing: the last packets carry speech (the
loudest of the last three: -24 to -33 dBFS), where without the pacer an answer ends in the
clip's quiet tail.

Over WebSocket the pacer also breaks up what it does send. Asterisk plays the channel out on its
own 20 ms clock and sends silence for any 20 ms in which it has no frame from AVA; the pacer
hands it one frame per 20 ms from a timer of its own, so a frame that comes a little late leaves
a gap: 7 to 10 short silences inside every answer (median 8, a packet or two each), and the
answer reaches the caller as 173-175 packets. With the pacer off there are 0 or 1. What
the caller hears of the engine's audio shows it: against what no linear filter explains, 3.3 dB
below the speech on a clean network with the pacer, 13.7 dB without it, 25.6 dB over AudioSocket;
the speech moved by up to 60 ms in all 199 completed answers, against 19 of 240 without the
pacer. The same holds on AVA's main branch at 99560e1, built from a checkout (2 latency calls per
setting, clean): 3.1 dB with the pacer and every answer moved, 13.7 dB and none without.

Over AudioSocket and ExternalMedia the pacer also makes the stream uneven: AVA's packets arrived
up to 440-453 ms behind their timestamps (p99, median of the 20 latency and barge-in calls on a
clean network), against 2.3 ms without the pacer. Over WebSocket Asterisk's own clock sends them
evenly (0.2 ms), whatever is inside.

```sh
uv run --extra vad python results/ava/answers.py ava-audiosocket-direct ava-externalmedia-direct \
  ava-websocket-direct ava-audiosocket-direct-nopacer ava-websocket-direct-nopacer
AVA_TRANSPORT=websocket uv run --extra vad rtpbench target ava --mock --source AVA --only latency --runs 2
AVA_TRANSPORT=websocket AVA_EGRESS_PACER=false uv run --extra vad rtpbench target ava --mock --source AVA --only latency --runs 2
```

The first prints these numbers and the next section's from the unpacked archives; the others
are the check on AVA's main branch (`AVA`, a checkout of it at 99560e1).

## Barge-in

AVA did not stop for interjections: of 1500 (100 per profile and set), an answer ended within 2 s
of one three times, all under `lte-bad` over AudioSocket, and each time with the mock's answer,
which the engine had sent in full: nothing stopped it. AVA holds back the caller's audio while
it plays (an echo gate, always on in its OpenAI Realtime provider), so the mock cancelled no
answer for the caller's voice, in any set. On a clean network the mock heard all 220 lines the caller said
outside AVA's answers (22 of the 32 in a latency and a barge-in call), and none of the 100 said
during one, over every transport. `answers.py` prints the times of each event and these counts.

## The RTP clock across AVA's pauses

Over AudioSocket and ExternalMedia AVA sends RTP only while it speaks. Over AudioSocket, Asterisk
keeps the RTP clock across each pause (1 ms behind, at the median) and sets the marker bit on the
packet after it (330 of 330 on a clean network), as RFC 3550 5.1 and RFC 3551 4.1 ask. Over
ExternalMedia it does neither: the timestamps go on as if no time had passed (7.9 s behind per
pause, at the median) and no packet is marked (0 of 330). A receiver that plays by timestamp then
runs the answers together. Over WebSocket there are no pauses: Asterisk sends RTP for the whole
call.

## Silence instead of the caller

In 6 calls, all over AudioSocket and all under `lte-bad`, the engine got silence in place of the
caller's audio: for the whole call in two (it never heard the question: the `ssrc-change` and
`late-offer` failures), and for part of the transfer request in four (the mock heard another
line and never asked for the transfer: the `refer` and `refer-lost` failures and the inconclusive
`bye-lost`). The cause is AVA's AudioSocket squelch: it takes its noise floor from the first
frame with sound in it, and when the network loses the quiet frames before a line, that floor is
the speech itself, so every frame of the line goes to the engine as zeros. AVA has fixed this
since the commit tested here. Over ExternalMedia and WebSocket every call in which the caller
spoke got its reply or its transfer.

Otherwise the caller's audio reached the engine as over the other transports, but noisier: what
no linear filter explains is 24.9 dB below the speech over AudioSocket, against 43.3 dB over
ExternalMedia and WebSocket (clean, median line). All three carry AVA's upsampling to 24 kHz,
with images above 4 kHz 25 dB below the speech, where LiveKit's are 61 dB below
([media path](../media-path)).

## Raw runs

Attached to the [release](https://github.com/jjaroztegi/rtpbench/releases/tag/ava-transports-wave)
as `.tar.zst`; each unpacks to the directory `rtpbench` wrote, with the mock's recordings in its
`realtime/`, and judges again from there:

```sh
sha256sum -c --ignore-missing SHA256SUMS && zstd -dc ava-websocket-direct-12ddda5e7bf9.tar.zst | tar -x
uv run --extra vad rtpbench report ava-websocket-direct
```

| archive | SHA-256 |
| --- | --- |
| `ava-audiosocket-direct-12ddda5e7bf9.tar.zst` | `ef44f04b4f08f2131e76c55144c4d1c420a8d76950e4146ce620d0dcda323757` |
| `ava-externalmedia-direct-12ddda5e7bf9.tar.zst` | `130b2cf950b56fcdda57916415e04d47ba0c96088c842bdb5569ce67c4b45e5a` |
| `ava-websocket-direct-12ddda5e7bf9.tar.zst` | `c66860bc4f875523b273d065f7df6b7cd3a2481759e512d9aa370e0548c3f5f8` |
| `ava-audiosocket-carrier-12ddda5e7bf9.tar.zst` | `29fa2c113e774a8b4fa9e2b18592cbbf495a0bcca20bd458a027d77729758d21` |
| `ava-externalmedia-carrier-12ddda5e7bf9.tar.zst` | `c03e36011a0a40ad9bade7beb33fabf2a1c37dacf8ece722ea2b7a14dec9bd83` |
| `ava-websocket-carrier-12ddda5e7bf9.tar.zst` | `9ae0e69476dc525d57d166c5e55244dbd26e17d955675b616306846453d28c06` |
| `ava-audiosocket-direct-nopacer-12ddda5e7bf9.tar.zst` | `1a448dcee57c8cb19c7c20c53be2fe6c4799612961762346b6343662ea62b060` |
| `ava-websocket-direct-nopacer-12ddda5e7bf9.tar.zst` | `c5041129c88dc3a88d39e9ffb68c95a74923a4e92743022c1c72f8ea6442758f` |
| `ava-reference-direct-12ddda5e7bf9.tar.zst` | `dafbcba74fed54031b1a8d99ccf9de3eb07df1188bdb7f03eb3a2937a154830f` |
| `ava-reference-carrier-12ddda5e7bf9.tar.zst` | `93d858dadb6612e6b87a6412abb50b436c85866319531ba02afa820b3e1729ae` |
| `ava-calibrate-12ddda5e7bf9.tar.zst` | `621ace3b0cd51165dfa5f7e917d16418da66061a83a61e95859cefa851fd1b1c` |
| `ava-calibrate-carrier-12ddda5e7bf9.tar.zst` | `dcea391c318dd388b85edfbc087e113efb39f28e6a995f65071fc160cfbda771` |
| `ava-main-99560e1-ae0e562f27ae.tar.zst` | `69f00cf45bb5969ba6f84c224428e7accaa5d109c9ab7a789b8b9bc1d50add70` |
