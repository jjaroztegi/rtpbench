# rtpbench

Calls voice agents over SIP/RTP and measures turn latency, barge-in timing and signalling
behaviour from captured packets, with and without network impairment (`tc netem`).

## Principles

- Timing comes from packets on the wire, never from agent logs or recordings.
- Every published number ships with the command and conditions that reproduce it, and its raw
  runs are archived: judging changes re-judge them; only wire changes need new runs.
- Smallest change that works. No speculative abstractions or "for later" code.
- Docs stay short. Code explains itself; comments say why, not what.

## Environment

Linux only (network namespaces, `tc netem`). On Windows, use WSL2.

Several checkouts may run at once. Give each run its own ports, namespace and container names,
and output directory.

```sh
uv sync
uv run ruff format && uv run ruff check --fix
uv run mypy
```

## Commits and pull requests

- Conventional commits in plain language: `feat(timing): measure turn latency from RTP`.
- One problem per PR. Body: the problem in a sentence or two, the change, and how it was verified.

## Documentation

- `README.md`: what rtpbench is, what it found, how to start. `docs/`: how to use it and what is
  unintuitive about it. `results/<name>/README.md`: one published run, with its commands,
  conditions and findings.
- Before adding a paragraph, ask what a reader would get wrong without it: a finding, a source,
  a constraint, a trap. Do not restate what the code or `--help` shows; link the source.
- Public files never name hosts, addresses, credentials or private notes.
- When something changes, rewrite the affected text instead of appending another account.
