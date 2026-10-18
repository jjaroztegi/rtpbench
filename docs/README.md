# rtpbench docs

- [Calibration](calibration.md): how close each measurement is to the truth, error bars, clock
  steps, network profiles and their sources
- [Conformance cases](cases.md): what each case checks, and which run through the carrier
- [Targets, the mock engine and the carrier](targets.md)

## Published results

Each comes from one commit, with its commands and conditions, and its raw run directories
(captures, logs, the reference agent's truth) attached to a GitHub release as `.tar.zst`, named
with their SHA-256 in the result's README. A change to how runs are judged (checks, error bars,
summaries) re-judges those directories; a new wave is needed only when what goes on the wire
changes (caller, carrier, mock engine, target versions, network profiles).

```sh
sha256sum -c SHA256SUMS && zstd -dc NAME.tar.zst | tar -x
uv run --extra vad rtpbench report DIR       # a cases or target directory: judged again
uv run --extra vad rtpbench analyze DIR...   # calibrations; same-named directories pool
```

Published:

- [Both targets on a mock engine](../results/bare-metal-mock): where each stack's time goes
- [LiveKit and AI Voice Connector CE on a real engine](../results/two-targets)
- [Through a carrier](../results/carrier)
- [First results](../results/first): the reference agent and AI Voice Connector CE
