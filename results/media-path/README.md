# Media path: what each connector does to the audio

2026-10-19: LiveKit and AI Voice Connector CE, direct, on the
[mock engine](../../docs/targets.md#mock-engine), in latency and barge-in calls only, under three
network profiles, 10 repeats each. This mock records what reaches it, so both directions are
compared with audio known sample for sample: the caller's lines (its own capture, before the
network) against what reached the engine, and the engine's answers against what reached the
caller. Image `rtpbench:72e41c264960`; the git tag `media-path-wave` is the commit that ran it
(`git checkout media-path-wave` to run it again). Summaries, records and reports are in this
folder, judged again by the code of the commit that added it; the raw run directories (captures,
logs, the mock's recordings) are [archived](#raw-runs).

```sh
uv run --extra vad rtpbench target livekit --mock --only latency,barge-in --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench target aivc --mock --only latency,barge-in --profiles clean,lte,lte-bad --runs 10
```

Conditions: as the [baseline](../baseline)'s, on the same host: 16 CPUs, kernel 6.8.0-147-generic,
CPU governor `performance`, Docker 29.9.1. The two sets ran at once, each its own
stack, for 3 h 31 min; the load average stayed between 2.03 and 2.75; 0 clock
steps. 60 and 60 calls, none failed. The targets at the baseline's versions.

## The recording mock against the baseline's

Recording costs the mock two small writes per append. Turn latency split where the mock heard
the end of the caller's speech and sent its first audio, p50, ms, this set / the baseline:

| target | profile | engine | wire latency | uplink | downlink |
| --- | --- | --- | --- | --- | --- |
| LiveKit | clean | 1501 / 1501 | 1833 / 1833 | 190 / 186 | 143 / 149 |
| LiveKit | lte | 1501 / 1501 | 1984 / 1997 | 294 / 302 | 187 / 189 |
| LiveKit | lte-bad | 1501 / 1501 | 2135 / 2134 | 439 / 426 | 193 / 201 |
| AIVC CE | clean | 1501 / 1501 | 1512 / 1512 | 0 / 1 | 9 / 10 |
| AIVC CE | lte | 1501 / 1501 | 1594 / 1592 | 40 / 40 | 52 / 51 |
| AIVC CE | lte-bad | 1501 / 1501 | 1605 / 1605 | 47 / 45 | 61 / 61 |

The engine's share is the same, and every other part is within 13 ms of the baseline's:
recording does not change what the mock measures.

## The caller's audio, as the engine got it

Each line the caller said in these calls (turns, barge-in prompts, interruptions, backchannels),
aligned piece by piece with what reached the engine, median over lines (min and max in the
[summaries](livekit-direct/summary.md)). Unchanged: lines whose aligned speech came through
sample for sample. Distortion: the speech against what no linear filter of ±4 ms explains (G.711
alone leaves about 37 dB). Moved: lines where a piece came out 5 ms or more later or earlier
than the one before. Missing 20 ms: the caller's voiced 20 ms with nothing like them nearby, and
what came in their place. Appends: the audio per message to the engine. Packets the network lost
on the way count against the target here: it is what the target did about them.

| target | profile | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB | above 4 kHz, dB | missing 20 ms | appends, ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LiveKit | clean | 0 of 320 | 28.3 | 0 | +1.9 | -16.6 | -60.7 | 0.4%: 63 other | 100 |
| LiveKit | lte | 0 of 309 | 19.1 | 132, up to 60 ms | +1.6 | -16.6 | -60.7 | 0.9%: 9 silence, 4 repeat, 131 other | 100 |
| LiveKit | lte-bad | 0 of 236 | 3.9 | 174, up to 60 ms | -0.3 | -16.7 | -60.8 | 3.8%: 64 silence, 1 repeat, 333 other | 100 |
| AIVC CE | clean | 320 of 320 | exact | 0 | +0.0 | +0.0 |  | 0.0% | 20 |
| AIVC CE | lte | 233 of 317 | exact | 88, up to 60 ms | +0.0 | +0.0 |  | 0.6%: 5 silence, 91 other | 20 |
| AIVC CE | lte-bad | 71 of 255 | 12.0 | 154, up to 60 ms | -0.5 | +0.0 |  | 3.0%: 52 silence, 302 other | 20 |

AI Voice Connector CE passes the caller's G.711 to the engine as it gets it, one RTP packet per
message: every aligned sample of all 320 lines on a clean network. It does nothing about a lost
packet: the next one takes its place, so the engine hears the line shorter by the loss (moved,
up to 60 ms).

LiveKit converts the call to 24 kHz and sends the engine 100 ms at a time. Its level is not
fixed: +1.9 dB at the median on a clean network, from -0.4 to +11.7 dB line to line. It takes
3.4-4 kHz down by 16.6 dB and sends nothing above 4 kHz (-60.7 dB): the engine gets
telephone-band audio, as from AI Voice Connector CE. What no filter explains is 28.3 dB below the
speech on a clean network; under loss, what it puts in place of lost packets brings that to
3.9 dB under `lte-bad`, against 12.0 dB through AI Voice Connector CE.

## The engine's audio, as the caller got it

As in the [baseline](../baseline#the-connectors-audio), now with this mock, median over the
answers it completed:

| target | profile | unchanged | distortion, dB | moved | gain, dB | 3.4-4 kHz, dB |
| --- | --- | --- | --- | --- | --- | --- |
| LiveKit | clean | 0 of 240 | 27.4 | 24, up to 40 ms | -0.2 | -8.3 |
| LiveKit | lte | 0 of 240 | 27.3 | 23, up to 60 ms | -0.2 | -8.3 |
| LiveKit | lte-bad | 0 of 236 | 27.1 | 18, up to 40 ms | -0.2 | -10.0 |
| AIVC CE | clean | 227 of 227 | exact | 0 | +0.0 | +0.0 |
| AIVC CE | lte | 220 of 220 | exact | 0 | +0.0 | +0.0 |
| AIVC CE | lte-bad | 220 of 220 | exact | 0 | +0.0 | +0.0 |

The mock sends LiveKit 24 kHz audio interpolated from 8 kHz clips. The comparison is against
that audio through an ideal 8 kHz converter, so the interpolation's own loss near 4 kHz is not
counted against LiveKit; what its images above 4 kHz alias back into the band would be. In the
other direction the mock records before its own conversion, so the caller's audio carries none
of it.

## Raw runs

Attached to the [release](https://github.com/jjaroztegi/rtpbench/releases/tag/media-path-wave) as
`.tar.zst`; each unpacks to the directory `rtpbench` wrote, with the mock's recordings in its
`realtime/`, and judges again from there:

```sh
sha256sum -c --ignore-missing SHA256SUMS && zstd -dc media-path-livekit-direct-72e41c264960.tar.zst | tar -x
uv run --extra vad rtpbench report livekit-direct
```

| archive | SHA-256 |
| --- | --- |
| `media-path-aivc-direct-72e41c264960.tar.zst` | `53fca760568b5ba55688f9aeeca42c3ae8fadb8e75b940bfca71fe0233fa9a94` |
| `media-path-livekit-direct-72e41c264960.tar.zst` | `865334b5c1e6ab33035ccf26e4f69e398d119577456e67edb088e436d2cc7261` |

