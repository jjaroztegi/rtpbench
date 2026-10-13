# rtpbench

Calls voice agents over SIP/RTP and measures turn latency, barge-in timing and signalling
behaviour from captured packets, with and without network impairment (`tc netem`).

## Principles

- Timing comes from packets on the wire, never from agent logs or recordings.
- Every published number ships with the command and conditions that reproduce it.
- Smallest change that works. No speculative abstractions or "for later" code.
- Docs stay short. Code explains itself; comments say why, not what.

## Environment

Linux only (network namespaces, `tc netem`). On Windows, use WSL2.

```sh
uv sync
uv run ruff format && uv run ruff check --fix
uv run mypy
```

## Commits and pull requests

- Conventional commits in plain language: `feat(timing): measure turn latency from RTP`.
- One problem per PR. Body: the problem in a sentence or two, the change, and how it was verified.
