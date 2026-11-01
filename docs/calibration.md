# Calibration

A calibration measures how far each of rtpbench's measurements is from the truth, on your host,
under each network profile. The cases take their error bars from it.

```sh
uv run rtpbench calibrate                               # 7 profiles x 20 turns, about 10 minutes
uv run rtpbench calibrate --profiles clean --turns 5
uv run --extra vad rtpbench calibrate --speech          # real speech, PCMU and PCMA, ~40 minutes
uv run --extra vad rtpbench calibrate --barge-in        # interruptions, ~35 minutes
```

## How the truth is known

The caller and a reference agent ([`agent.py`](../src/rtpbench/agent.py)) run in containers on
either side of a `tc netem` router. The agent answers each turn after a random delay it chooses
and logs to the sample. Both ends capture with `tcpdump`, and every container shares one kernel
clock. Wire timing is therefore exact against the agent's log, and the calibration's real job
is the other error: how far speech detection moves an onset or a stop. The exception is a host
that holds packets between containers: a virtual machine that loses its CPU now and then (steal
time) delays the turns it held by that long, and `calibrate` warns when wire timing misses its
±0.41 ms bar.

For the speech calibration, the clips in [`corpus/`](../corpus/README.md) carry speech boundaries
labelled on the clean audio. For barge-in, the caller and agent share a script of who cuts in
and whether the agent stops ([`bargein.py`](../src/rtpbench/bargein.py)).

## Error bars

A bar of (−3.2/+44.6) means the true value lies between 3.2 ms below and 44.6 ms above the
measured one: the p5..p95 range of the detector's error for that profile and codec. Each bar
pools five seeds of `calibrate --speech` or `--barge-in`, 215 onsets or 221 stops per profile
and codec ([`cases.py`](../src/rtpbench/cases.py)); five more seeds leave 5-13% outside the
bars, where about 10% would be expected ([held out](../results/baseline#detector-error-bars-held-out)).
The bars come from one host and serve every host: with one seed per bar, a run on a second host
moved the edges no more than a second run on the same host did.

Against a target, the gate's stop bar also decides which barge-in turns count: a stop time below
its low side means the agent's speech, as the gate heard it, ended before the caller cut in, and
the turn is left out of the stop rate and stop times ("speech ended before (gate)"). The bar is
p5..p95, so about 5% of real stops read below it and are left out with them.

The agent's first speech in a call, usually its greeting, has its own onset bar: a detector that
has heard nothing yet fires later, and without the early A-law tail below.

The PCMA onset bar's early edge (p5 −131 to −142 ms, against −3 to −16 on PCMU) is webrtcvad,
not the codec alone. On A-law, a detector that has heard earlier speech fires on the low-level
lead-in before a labelled onset: room tone and TTS noise floor, below the label's −35 dB
threshold. A fresh detector per clip does not do it, and nor does a lead-in replaced by digital
silence. A-law has no zero level (silence decodes to ±8), mu-law has one. An A-law agent's
onsets after its first can read more than 130 ms early.

## Clock steps and rate

Captures stamp the wall clock, which time sync can step. Senders schedule on the monotonic clock
([`clock.py`](../src/rtpbench/clock.py)), so a step leaves no gap in the audio. Each run logs the
steps it saw (`clock_steps` in `conditions.json`), and summaries mark any interval timed across
one, because it reads off by the step. A step under a tenth of the width of that timing's error
bar is not counted: it moves the timing less than the spread the bar already allows (a 1.5 ms
step across a webrtcvad onset bar of -133/+11 ms).

A clock stepped back again and again runs fast in between, and nothing marks that drift: late,
transit against the earliest packet, grows with it until the next step. Each run records the
wall clock's rate between steps (`clock_rate_ppm`, from the steps' net size), and summaries
warn above 100 ppm. Virtual machines are prone to both. One WSL2 guest's clock stepped back
25-80 ms about every 30 s, so it ran 800-2,700 ppm fast and late read up to 25-80 ms high just
before each step; Hyper-V's clocksource brought its steps down to about 4 ms. Another lost 6% of
real time and was stepped forward about 1.6 s every 31 s on either clocksource, so no timing
taken on it holds. On WSL2, a `calibrate` run before and after switching from the default `tsc`
clocksource to Hyper-V's shows whether that helps:

```sh
echo hyperv_clocksource_tsc_page | sudo tee /sys/devices/system/clocksource/clocksource0/current_clocksource
```

## Running stacks in parallel

Each run brings up its own containers and network, so several can run at once. On an 8-core,
16-thread host, 12 reference stacks at once kept wire timing exact, no packet more than 10 ms
late and no capture drop ([table](../results/baseline#timing-on-this-host)). Target stacks
weigh more: calibrate at the concurrency you intend to publish at, and watch the load.

## Network profiles

netem settings per direction, on the router, applied to RTP only: SIP, over UDP, TCP or TLS, is never
impaired. `delay`, `jitter`, `loss` and `mobile` are synthetic stimuli for the calibrations
([`bench.py`](../src/rtpbench/bench.py)). `lte` and `lte-bad` stand for a mobile caller's path,
and every number in them has a source:

| profile | netem | source |
| --- | --- | --- |
| `lte` | `delay 40ms 3ms distribution normal loss gemodel 0.505% 50% rate 100mbit` | 1% loss, the VoLTE (QCI 1) target per radio link ([3GPP TR 26.989](https://www.3gpp.org/ftp/Specs/archive/26_series/26.989/) 5.1.1.6.1), in bursts of 2 packets (3GPP VoLTE delay/error profiles 7-10, [EVS-7c S4-141392](https://www.3gpp.org/ftp/tsg_sa/WG4_CODEC/EVS_Permanent_Documents/) Annex D); jitter sd 3 ms (commercial LTE in mobility, [Elnashar et al.](https://arxiv.org/abs/1810.02968), fig. 6); 40 ms one way (LTE uplink p99, [Nielsen et al.](https://arxiv.org/abs/1909.03875), fig. 4) |
| `lte-bad` | `delay 36ms 30ms distribution normal loss gemodel 3.2% 48% rate 100mbit` | 3GPP delay/error profile 8, VoLTE logs in challenging radio conditions (EVS-7c Annex D): 6.2% loss in runs of 2.1 packets; delay above the floor mean 45 ms, sd 26, p95 90. netem delivers mean 48, sd 23, p95 88 (5000 packets) |

`rate` is there to keep packets in order, as a radio bearer delivers them. Independent netem
jitter of sd 26 ms reorders 30% of packets; the profile 8 trace reorders 3%. netem cannot
reproduce the trace's packet-to-packet delay correlation: 0.95 in the trace, 0.43 here.
