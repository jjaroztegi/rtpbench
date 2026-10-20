# rtpbench docs

- [Calibration](calibration.md): how close each measurement is to the truth, error bars, clock
  steps, network profiles and their sources
- [Conformance cases](cases.md): what each case checks, and which run through the carrier
- [Targets, your own agent, the mock engine and the carrier](targets.md)
- [CI](ci.md): pass or fail a target run against a policy: the cases it may fail, latency and
  barge-in limits, regression from an earlier run

## Published results

Each comes from one version of the code, named by its image tag (`rtpbench:` and a hash of
`src`, the `Dockerfile` and the corpus, recorded as `image` in `conditions.json`), with its
commands and conditions, and its raw run directories (captures, logs, the reference agent's
truth) attached to a GitHub release as `.tar.zst`, named with their SHA-256 in the result's
README. A change to how runs are judged (checks, error bars,
summaries) re-judges those directories; a new wave is needed only when what goes on the wire
changes (caller, carrier, mock engine, target versions, network profiles).

```sh
sha256sum -c SHA256SUMS && zstd -dc NAME.tar.zst | tar -x
uv run --extra vad rtpbench report DIR       # a cases or target directory: judged again
uv run --extra vad rtpbench analyze DIR...   # calibrations; same-named directories pool
```

Published:

- [Baseline](../results/baseline): every case on the reference agent and both targets, on a
  mock engine, direct and through a carrier
- [Media path](../results/media-path): what each target does to the caller's audio on its way
  to the engine, and to the engine's on its way to the caller, on a mock engine that records
  what it receives
- [AI Voice Connector CE at b95f5af](../results/aivc-b95f5af): the baseline's sets again, with the
  connector at upstream main, which passes 4 more cases
- [Asterisk + AVA](../results/ava): Asterisk and AVA over AudioSocket and over ExternalMedia with
  AVA's egress pacer, and over AudioSocket without it, on a mock engine, direct and through a
  carrier
- [SIP over TLS and SRTP](../results/tls-srtp): this host's timing error with both, direct and
  through the carrier, the cases proven on the reference agent over them, and AI Voice Connector
  CE behind a carrier that takes them
- [Metrology](../results/metrology): how far common ways of measuring turn latency (an agent's
  own view, energy and VAD rules on a recording, a mean of gaps) are from the truth, on the
  baseline's calibration calls
