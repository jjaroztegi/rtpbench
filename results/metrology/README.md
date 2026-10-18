# Metrology: how far common latency measurements are from the truth

Voice-agent latency is measured in several ways, and the documentation of most tools says little
about how far each is off. Here the same calls are measured each way against rtpbench's ground
truth: a reference agent that logs every reply, speech clips with labelled boundaries, captures
at both ends on one kernel clock. No new calls were placed: these are the held-out detector
calibrations of [the baseline](../baseline#detector-error-bars-held-out), seeds 6-10, under the
profiles clean, lte and lte-bad, PCMU and PCMA: 215 turns per profile and codec of real speech
(43 per call, the agent answering 1.5-2.5 s after the caller's last speech), and 230 barge-ins.
The bars in the code were fit on seeds 1-5, so rtpbench's own row is held out too.

```sh
sha256sum -c SHA256SUMS && zstd -dc baseline-detector-seeds6-10-965085c223d2.tar.zst | tar -x
uv run --extra vad rtpbench analyze --methods pub/speech-s*-{clean,lte,lte-bad}/*-pcm{u,a}  # methods/summary.md
uv run --extra vad rtpbench analyze pub/barge-s*-{clean,lte,lte-bad}-pcm{u,a}/*-pcm?      # barge-in/summary.md
```

Conditions of the calls: as the baseline's, image `rtpbench:965085c223d2`, 16 CPUs, 0 clock
steps. The analysis is the code of the commit that added this folder; it reads only the
archived captures and the caller's and agent's logs, so its numbers do not depend on the host.
The full outputs are [methods](methods/summary.md) and [barge-in](barge-in/summary.md).

## Methods

Truth: from the caller's last labelled speech sample to the agent's first, as they crossed the
caller's wire. Error: measured minus truth.

| method | what it does | who documents it |
| --- | --- | --- |
| rtpbench | packet capture times at the caller; the caller's end from its own labels; the agent's onset by webrtcvad, with a calibrated error bar | [calibration](../../docs/calibration.md) |
| agent side | the same labels on the agent's own capture: the best an agent-side log can do | Retell's `e2e` latency "does not account for the network trip time from Retell server to user frontend" ([get-call](https://docs.retellai.com/api-references/get-call)); LiveKit Agents' [`e2e_latency`](https://docs.livekit.io/deploy/observability/data/) and Pipecat's [latency observer](https://docs.pipecat.ai/server/utilities/observers/user-bot-latency-observer) are taken inside the agent |
| recording | a two-channel recording at the caller, the agent's channel placed by a jitter buffer; the caller's end and the agent's onset both detected | Coval's Latency ("speaking segments detected for the call (voice activity detection runs upstream)") and [Cekura's](https://docs.cekura.ai/documentation/key-concepts/metrics/pre-defined-metrics) ("applying VAD to the stereo recording", average and P25-P99); neither names its VAD |
| detector `rms` | speech wherever the 10 ms around each 1 ms step has a mean-removed RMS above 0.01 of full scale | Coval's TTS time-to-first-audio onset ([ttfa.py](https://github.com/coval-ai/benchmarks/blob/29c8feee73c4e87a76498c1b9b1b9a9aaa93264e/runner/src/coval_bench/metrics/ttfa.py)); Coval's call-level Time to First Audio uses "RMS energy (signal level) above a threshold" and gives no value |
| detectors `webrtcvad`, `silero`, `silero16` | the open VADs a reader would reach for, raw ([detect.py](../../src/rtpbench/detect.py)) | |
| mean of gaps | per call, the mean of the recording's gaps from the caller's end to the agent's onset, only gaps of at least 0.5 s | Coval's Latency: "the average silence gap in seconds", gaps "of at least 0.5 seconds", no percentiles ([statistical metrics](https://docs.coval.ai/concepts/metrics/types/statistical)) |
| appending payloads | the agent's channel written as packets arrive, a lost packet leaving no gap | a naive recorder |

Vendor documentation was read on 2026-10-18. Other testing vendors publish no method in their
documentation, so none is named here.

## Findings

- **Measured inside the agent, a turn misses the network.** On lte the agent's own capture reads
  80 ms short (73 to 88, p5 to p95); on lte-bad 88-92 ms short (29 to 157). On clean it is exact.
  An agent-side metric also places the caller's end with its own VAD, with the errors below.
- **An energy threshold on a recording reads turns long: by 87-110 ms at p50 and up to 274 at
  p95**, on every profile and codec. Coval's onset rule (RMS above 0.01 of full scale) finds the
  agent's onset only 6-13 ms late, but ends the caller's turn 65 ms early, and 240 ms early at
  p5: the soft tail of a sentence is under −40 dBFS.
- **webrtcvad and Silero at 16 kHz on a recording read turns short, and spread over 190-310
  ms.** They end the caller's turn late (webrtcvad +24 ms on PCMU, +42 on PCMA; Silero about
  +50) and find the agent less late, so at p50 webrtcvad reads −9 ms on PCMU and −53 on PCMA,
  Silero at 16 kHz about −20. Per turn (p5 to p95), webrtcvad runs from −80 to +158 ms on PCMU
  and −191 to +117 on PCMA; Silero at 16 kHz, the tightest, from −68 to +135 on clean and −94
  to +170 on lte-bad. Silero at 8 kHz reads long instead, up to 311 ms, and misses 8 of 215
  replies (9 on lte-bad PCMA).
- **A mean per call hides the spread, and still moves with outliers.** With webrtcvad on PCMU, on clean
  and lte, every call's mean of gaps is within 9 ms of its true mean while its turns are off by
  −64 to +158 ms. With Silero at 8 kHz a few late detections move a call's mean by up to 321 ms.
  The 0.5 s floor dropped no turn here, where the agent never answered in under 1.5 s; it drops
  every turn a faster agent answers in under 0.5 s, so for such an agent the mean reads high.
- **A recorder that appends payloads as they arrive is seconds off after a few lost packets**,
  and finds no reply at all for 16-23% of the turns on lte and lte-bad. A jitter buffer costs a
  few ms on lte and about 40 ms on lte-bad (synthetic voice, the baseline's
  [calibration](../baseline/calibrate/summary.md)).
- **rtpbench's wire method reads −2 to +9 ms at p50**, and its spread is what its error bars
  say: held out on these calls, 5-13% of turns fall outside a p5..p95 bar
  ([baseline](../baseline#detector-error-bars-held-out)). The early PCMA tail, to −172 ms, is the
  A-law lead-in its bar [describes](../../docs/calibration.md#error-bars).

## Turn latency

Measured − truth, ms: p50 [p5, p95] over the 215 turns of each profile and codec; in
parentheses, the turns a method found, where it missed some. Where each recording's error comes
from (the caller's end against the agent's onset) is in [methods](methods/summary.md).

| method | clean-pcmu | clean-pcma | lte-pcmu | lte-pcma | lte-bad-pcmu | lte-bad-pcma |
| --- | --- | --- | --- | --- | --- | --- |
| truth itself | +1877 [+1455, +2345] | +1885 [+1458, +2349] | +1958 [+1535, +2428] | +1965 [+1531, +2427] | +1957 [+1545, +2423] | +1961 [+1520, +2458] |
| rtpbench: wire, labelled end, webrtcvad onset | +9 [-2, +38] | +0 [-139, +13] | +7 [-4, +40] | -1 [-143, +15] | +1 [-16, +64] | -2 [-172, +31] |
| the agent's capture, labelled: an agent-side log | -0 [-0, -0] | -0 [-0, -0] | -80 [-87, -75] | -80 [-88, -73] | -88 [-156, -29] | -92 [-157, -40] |
| recording, rms at both edges | +88 [+34, +256] | +88 [+34, +257] | +87 [+33, +258] | +89 [+35, +261] | +110 [+24, +274] | +103 [+11, +267] |
| recording, webrtcvad at both edges | -9 [-63, +158] | -53 [-191, +117] | -11 [-64, +154] | -51 [-188, +113] | +6 [-80, +158] | -36 [-182, +104] |
| recording, silero at both edges | +20 [-65, +225] (207/215) | +30 [-54, +265] (207/215) | +19 [-64, +243] (207/215) | +37 [-53, +266] (207/215) | +34 [-58, +232] (207/215) | +37 [-92, +311] (206/215) |
| recording, silero16 at both edges | -20 [-66, +119] | -17 [-68, +135] | -19 [-70, +119] | -20 [-72, +142] | +2 [-79, +153] | -1 [-94, +170] |
| recording appending payloads as they arrive, webrtcvad | -9 [-63, +158] | -53 [-191, +117] | -991 [-2067, +7007] (176/215) | -968 [-2121, +6461] (165/215) | +1265 [-1805, +7018] (181/215) | +1350 [-1513, +6944] (181/215) |

The mean of gaps per call, Coval's Latency, against the mean of the call's true latencies, ms:
median [min, max] over the 5 calls; gaps counted / turns.

| detector | clean-pcmu | clean-pcma | lte-pcmu | lte-pcma | lte-bad-pcmu | lte-bad-pcma |
| --- | --- | --- | --- | --- | --- | --- |
| rms | +107 [+107, +107] (215/215) | +107 [+107, +108] (215/215) | +107 [+103, +110] (215/215) | +108 [+106, +109] (215/215) | +132 [+80, +146] (215/215) | +120 [+67, +143] (215/215) |
| webrtcvad | +5 [+0, +9] (215/215) | -53 [-55, -49] (215/215) | +7 [-3, +7] (215/215) | -52 [-56, -50] (215/215) | +29 [-28, +41] (215/215) | -40 [-93, -18] (215/215) |
| silero | +66 [+31, +274] (207/215) | +68 [+45, +290] (207/215) | +56 [+40, +280] (207/215) | +75 [+59, +293] (207/215) | +80 [+22, +306] (207/215) | +85 [+34, +321] (206/215) |
| silero16 | -3 [-7, +1] (215/215) | +2 [-4, +9] (215/215) | -4 [-11, +2] (215/215) | +1 [-2, +7] (215/215) | +31 [-24, +40] (215/215) | +27 [-36, +41] (215/215) |

## Barge-in

Stop time: from the caller's interjection onset, labelled, to the agent's last sample before it
fell silent, both as they crossed the caller's wire. The reference agent cuts hard, after a
known delay. Cekura documents a "Stop Time After User Interruption" with VAD on a stereo
recording; rtpbench uses the gate (|sample| ≥ 1000) on the wire, with its calibrated bar.

Measured − truth, ms: p50 [p5, p95] over the 230 stops of each profile and codec, from
[barge-in](barge-in/summary.md); a recording is the agent's channel through a jitter buffer.

| method | clean-pcmu | clean-pcma | lte-pcmu | lte-pcma | lte-bad-pcmu | lte-bad-pcma |
| --- | --- | --- | --- | --- | --- | --- |
| rtpbench: wire, gate | -4 [-86, +0] | -3 [-86, +0] | -2 [-104, +0] | -2 [-110, +0] | -2 [-104, +0] | -1 [-112, +0] |
| wire, rms | +1 [-79, +6] | +2 [-83, +6] | +2 [-92, +6] | +2 [-110, +6] | +0 [-94, +6] | +0 [-105, +6] |
| recording, webrtcvad | +71 [-21, +102] | +84 [-2, +102] | +82 [-18, +105] | +89 [-8, +104] | +63 [-28, +138] | +63 [-32, +130] |
| wire, silero16 | +32 [-3, +112] | +53 [-3, +118] | +28 [-2, +115] | +52 [-3, +118] | +29 [-7, +138] | +63 [-5, +142] |
| recording appending payloads as they arrive, webrtcvad | +71 [-21, +102] | +84 [-2, +102] | -879 [-1688, +103] (50/230) | -850 [-1611, +56] (51/230) | -290 [-1467, +1308] (49/230) | -533 [-1779, +1198] (47/230) |

- **Energy rules time a stop to the ms at the median and read early in the tail**: the gate and
  Coval's RMS rule −4 to +2 ms at p50, 79-112 ms early at p5, where the speech before the cut
  had already gone soft.
- **A VAD reads every stop long by its hangover**: webrtcvad on a recording +63 to +89 ms at
  p50 and up to +138; Silero at 16 kHz, on the wire, +28 to +63. A stop webrtcvad reads as 500 ms took about
  420.
- Appending payloads finds a fifth of the stops on lte and lte-bad, and those seconds off.
- Here the interjection's onset is the caller's own label; a recording detects it too, which
  adds the onset error of its detector.

## Raw runs

The calls are the baseline's `baseline-detector-seeds6-10-965085c223d2.tar.zst`, SHA-256
`b2ffa0585eb3c6d29eef4d0287cff53b12d57cc25fcf648c349efee872515640`, on its
[release](../../docs/README.md#published-results).
