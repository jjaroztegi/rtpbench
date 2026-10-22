# Asterisk + AVA over SIP: AudioSocket and ExternalMedia

2026-10-20: Asterisk 22.8 (`chan_pjsip`) with AVA v7.6.4 (Asterisk AI Voice Agent), the
[`ava` target](../../docs/targets.md), on the [mock engine](../../docs/targets.md#mock-engine),
called direct and through the [carrier](../../docs/targets.md#carrier), under three network
profiles, 10 repeats each. AVA takes the call's audio from Asterisk over AudioSocket, as upstream
ships it, or over ExternalMedia (RTP); its golden configuration turns on an egress pacer. Both
transports ran with the pacer, and AudioSocket without it. Image `rtpbench:0397e3c41635`; the git
tag `ava-wave` is the commit that ran it. Summaries, records and reports are in this folder,
judged again by the code of the commit that added it; the raw run directories are
[archived](#raw-runs).

[tvbench](https://github.com/ictinnovations/telephony-voice-agent-benchmark) measures an agent by
standing in for Asterisk over a local AudioSocket: "Loopback is not a network. Add jitter and loss
yourself if that is what you want to know." Here Asterisk and the network stay in front of the
agent: the caller's SIP and RTP cross netem, and with `--carrier` OpenSIPS and rtpengine, before
the audio reaches the socket.

```sh
uv run --extra vad rtpbench target ava --mock --profiles clean,lte,lte-bad --runs 10
AVA_TRANSPORT=externalmedia uv run --extra vad rtpbench target ava --mock --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench target ava --mock --carrier --profiles clean,lte,lte-bad --runs 10 \
  --only greeting,bye,cancel,hold,dtmf-rfc4733,dtmf-info,refer,refer-fail,timer,ptime-30,ssrc-change,reinvite,reinvite-nosdp,compact-headers,sdp-ssrc,late-offer
AVA_TRANSPORT=externalmedia uv run --extra vad rtpbench target ava --mock --carrier --profiles clean,lte,lte-bad --runs 10 \
  --only greeting,bye,cancel,hold,dtmf-rfc4733,dtmf-info,refer,refer-fail,timer,ptime-30,ssrc-change,reinvite,reinvite-nosdp,compact-headers,sdp-ssrc,late-offer
AVA_EGRESS_PACER=false uv run --extra vad rtpbench target ava --mock --only latency,barge-in --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench cases --profiles clean,lte,lte-bad --runs 1
uv run --extra vad rtpbench cases --carrier --profiles clean,lte,lte-bad --runs 1
uv run rtpbench calibrate
uv run rtpbench calibrate --carrier
```

Conditions: the [baseline](../baseline)'s host, 16 CPUs, kernel 6.8.0-147-generic, CPU governor
`performance`, Docker 29.9.1; the mock engine waits 1000 ms of silence and answers 500 ms later;
the carrier is OpenSIPS 3.6.9 and rtpengine, as in the baseline. The four transport sets ran at
once, then the pacer-off set and the reference agent's proofs, then the calibrations alone: 6 h
8 min. The load average went from 0.8 to 10.1 (3.9 at the start, from the host's other services);
0 clock steps. The reference agent got the expected verdict in 117 of 117 calls direct and 111 of
111 through the carrier, and wire timing against its truth stayed exact (max abs 0.00 ms) in
every profile, but for one `lte` turn direct (0.50 ms) whose first packet of speech was lost.

## Verdicts

| case | AudioSocket, direct | ExternalMedia, direct | AudioSocket, carrier | ExternalMedia, carrier |
| --- | --- | --- | --- | --- |
| `greeting` | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 |
| `bye` | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 |
| `cancel` | inconclusive 30/30 | inconclusive 30/30 | inconclusive 30/30 | inconclusive 30/30 |
| `hold` | inconclusive 30/30 | inconclusive 30/30 | inconclusive 30/30 | inconclusive 30/30 |
| `hold-zero` | inconclusive 30/30 | inconclusive 30/30 | | |
| `dtmf-rfc4733` | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 |
| `dtmf-info` | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 |
| `refer` | pass 30/30 | pass 30/30 | flips: pass 27, fail 3 | pass 30/30 |
| `refer-fail` | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 |
| `codec-pcmu` | pass 30/30 | pass 30/30 | | |
| `codec-pcma` | pass 30/30 | pass 30/30 | | |
| `codec-change` | pass 30/30 | pass 30/30 | | |
| `timer` | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 | **fail** 30/30 |
| `ssrc-change` | pass 30/30 | pass 30/30 | flips: pass 29, fail 1 | pass 30/30 |
| `large-invite` | pass 30/30 | pass 30/30 | | |
| `reinvite` | flips: pass 29, fail 1 | pass 30/30 | flips: pass 29, fail 1 | pass 30/30 |
| `reinvite-nosdp` | pass 30/30 | pass 30/30 | pass 30/30 | pass 30/30 |
| `compact-headers` | | | pass 30/30 | pass 30/30 |
| `sdp-ssrc` | | | flips: pass 29, fail 1 | pass 30/30 |
| `late-offer` | | | pass 30/30 | pass 30/30 |
| `ptime-30` | | | flips: pass 29, fail 1 | pass 30/30 |

- `cancel` is inconclusive: AVA answers 4-5 ms after its first provisional response, so no CANCEL
  can arrive while it rings. `hold` and `hold-zero` too: AVA sends RTP only while it speaks, and it
  said nothing in the second before the hold, so whether media resumes cannot be judged.
- A digit reaches the engine by neither method.
- `refer`: the REFER goes out 5.9 s after the request: the mock calls the transfer tool, AVA asks
  it for a reply, plays it, and hands the call to the dialplan's `Transfer()`. `refer-fail`: the
  dialplan ends the call after `Transfer()` whatever its outcome, so the failure never reaches
  the engine and the caller is hung up on.
- `timer`: AVA hangs up 13 s after the session refresh, about 59 s into a call where the caller
  stays silent (its no-input check), before the session could expire.
- Every other failure is a call where the engine got silence instead of the caller,
  [below](#silence-instead-of-the-caller).

## Turn latency

Turn latency, ms, p50 [p5, p95], every turn of the latency calls, and AVA's share of it on the
way out (the mock's first audio to the agent's speech on the wire; on the way in it is 1 ms on a
clean network, 40-41 ms under `lte` and `lte-bad`, the profiles' own delay):

| profile | AudioSocket | downlink | ExternalMedia | downlink | AudioSocket, pacer off | downlink |
| --- | --- | --- | --- | --- | --- | --- |
| clean | 1588 [1469, 1594] | 87 | 1588 [1469, 1596] | 88 | 1572 [1444, 1582] | 71 |
| lte | 1663 [1546, 1679] | 122 | 1662 [1551, 1675] | 121 | 1650 [1525, 1666] | 109 |
| lte-bad | 1650 [1501, 1713] | 106 | 1656 [1533, 1727] | 112 | 1643 [1498, 1726] | 103 |

The engine's share is the mock's fixed 1501 ms. On a clean network AVA adds 87 ms to a turn
with either transport, 16 ms of it the pacer's; in the baseline, AI Voice Connector CE adds 11 ms
and LiveKit 332 ms. These are the median turn less the engine's 1501 ms; the
[front page](../../README.md) adds the medians of uplink and downlink instead (88 ms for AVA,
335 ms for LiveKit). The greeting is heard 690-736 ms after the 200 OK; AVA asks the engine for it
140-155 ms after answering.

## The pacer cuts every answer short

With the pacer on, AVA stops sending each answer about 0.8 s before its end: 162-166 packets of
the 204-205 it sends with the pacer off, in all 130 answers of the clean latency calls of each
transport, the greeting included. The last packets it sends carry speech (the loudest of the last
three: -24 to -33 dBFS), where without the pacer an answer ends in silence. The pacer also makes
the stream uneven: over AudioSocket on a clean network, AVA's packets arrived up to 442 ms behind
their timestamps (p99, median of the 20 latency and barge-in calls), against 2.7 ms without it
in the same 20 calls of that set. The set's summary gives 200 ms: over all 176 clean calls of
every case.

```sh
uv run --extra vad python results/ava/answers.py ava-audiosocket-direct ava-externalmedia-direct \
  ava-audiosocket-direct-nopacer   # these numbers and the next section's, on the unpacked archives
```

## Barge-in

AVA did not stop for interjections: of 900 (100 per profile and set, both transports, pacer on
or off), an answer ended within 2 s of one only once: ExternalMedia, clean, run 10, 1.3 s into a
1.9 s interjection that began 16.571 s after the call's INVITE. The answer's RTP ended at
17.882 s, as the mock's answer did (17.885 s). AVA holds back the caller's audio while it plays
(an echo gate, always on in its OpenAI Realtime provider), so the mock cancelled no answer for
the caller's voice, in any set. In that call the first voiced audio of the interjection reached
the mock at 17.892 s, 7 ms after its answer ended; it heard a turn ending at 18.528 s. On a
clean network the mock heard all 220 lines the caller said outside AVA's answers (22 of the 32 in
a latency and a barge-in call), and of the 100 said during one, only that interjection's tail.
`answers.py` prints the times of the event and these counts.

## The RTP clock across AVA's pauses

AVA sends RTP only while it speaks. Over AudioSocket, Asterisk keeps the RTP clock across each
pause (0 ms behind, at the median) and sets the marker bit on the packet after it (310 of 310
on a clean network), as RFC 3550 5.1 and RFC 3551 4.1 ask. Over ExternalMedia it does neither:
the timestamps go on as if no time had passed (8.0 s behind per pause, at the median) and no packet
is marked (0 of 311). A receiver that plays by timestamp then runs the answers together.

## Silence instead of the caller

In 8 calls, all over AudioSocket and all under `lte` or `lte-bad`, the engine got silence in
place of the caller's audio: for the whole call in five (it never heard the question: the
`reinvite`, `ssrc-change`, `sdp-ssrc` and `ptime-30` failures), and for part of the transfer
request in three (the mock heard another line and never asked for the transfer: the `refer`
failures through the carrier). Over ExternalMedia every call in which the caller spoke got its
reply or its transfer. Where on the way through Asterisk and AVA the audio was lost was not
found.

Otherwise the caller's audio reached the engine as over ExternalMedia, but noisier: what no
linear filter explains is 24.9 dB below the speech over AudioSocket, against 43.3 dB over
ExternalMedia (clean, median line). Both carry AVA's upsampling to 24 kHz, with images above
4 kHz 25 dB below the speech, where LiveKit's are 61 dB below ([media path](../media-path)).

## Raw runs

Attached to the [release](https://github.com/jjaroztegi/rtpbench/releases/tag/ava-wave) as
`.tar.zst`; each unpacks to the directory `rtpbench` wrote, with the mock's recordings in its
`realtime/`, and judges again from there:

```sh
sha256sum -c SHA256SUMS && zstd -dc ava-audiosocket-direct-0397e3c41635.tar.zst | tar -x
uv run --extra vad rtpbench report ava-audiosocket-direct
```

| archive | SHA-256 |
| --- | --- |
| `ava-audiosocket-direct-0397e3c41635.tar.zst` | `6f5095434b0a62e1a9cd71b0d65299808f7653f8ee3cb15e9c36c3d9a6cab52a` |
| `ava-externalmedia-direct-0397e3c41635.tar.zst` | `ce90e8d9d0bb0771da4c2cd528bb576a0b5751de627bde2b7c4645cf725250d6` |
| `ava-audiosocket-direct-nopacer-0397e3c41635.tar.zst` | `b55f528cda6011be854a9d60364341742c33439f8d3220a47a2f3d6ab59026fd` |
| `ava-audiosocket-carrier-0397e3c41635.tar.zst` | `14fdc0f01d1871015ce1d0ea5a0a716a4e8f967d666a18575c57aaeff69ef90d` |
| `ava-externalmedia-carrier-0397e3c41635.tar.zst` | `a416f24c304d26d6cd335eb527c46281a39c4994edb9cf2191504426e17a4295` |
| `ava-reference-direct-0397e3c41635.tar.zst` | `c45020223be57f700f252daeb6c1cb49190be4045944418d17496fe90552ac03` |
| `ava-reference-carrier-0397e3c41635.tar.zst` | `5d3663f67628a90cb5cd84c09deb66f34279a7cfb752b297614de0e054a3fd73` |
| `ava-calibrate-0397e3c41635.tar.zst` | `cdc179f9d892d3aa1e637c70fa1b9a98502437219c07bc98cd6289a25de61215` |
| `ava-calibrate-carrier-0397e3c41635.tar.zst` | `7d4a2e8f86e9e8212d9239f83fc23aacfa4a3e5d24f1bbf929cf6fb36373c1c9` |
