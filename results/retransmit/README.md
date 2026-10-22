# Lost SIP messages: the retransmission cases on the bundled targets

2026-10-21: the three [cases](../../docs/cases.md) for a lost SIP message on LiveKit, AI Voice
Connector CE at b95f5af and Asterisk + AVA, 10 repeats each, on the
[mock engine](../../docs/targets.md#mock-engine). The three cases are `invite-retransmit` (every
response to the INVITE lost for T1, so the INVITE goes again), `refer-lost` and `bye-lost` (the
agent's first REFER, or its BYE after the transfer, left unanswered).
- **Route:** direct only, because a carrier's own transaction would absorb and resend for the
  agent.
- **Profile:** clean only, because SIP is exempt from netem.
- **Code:** image `rtpbench:fe41c0856bb3`; the git tag `retransmit-wave` is the commit that ran it
  (687f998).
- **Files:** summaries, records and reports are in this folder, judged again by the code of the
  commit that added it. The raw run directories are [archived](#raw-runs).

```sh
uv run --extra vad rtpbench target livekit --mock --only invite-retransmit,refer-lost,bye-lost --runs 10
uv run --extra vad rtpbench target aivc --mock --only invite-retransmit,refer-lost,bye-lost --runs 10
uv run --extra vad rtpbench target ava --mock --only invite-retransmit,refer-lost,bye-lost --runs 10
uv run --extra vad rtpbench cases --only invite-retransmit,refer-lost,bye-lost --runs 1
```

Conditions:
- **Host:** the baseline's host, 16 CPUs, kernel 6.8.0-147-generic, CPU governor `performance`,
  Docker 29.9.1.
- **Mock engine:** waits 1000 ms of silence and answers 500 ms later.
- **AVA:** its default variant, AudioSocket with the egress pacer on.
- **Schedule and load:** the sets ran one after another, then the reference agent's proofs:
  21 min. Other work shared the host; the load average stayed between 3.1 and 5.1.
- **Clock and proofs:** 0 clock steps. The reference agent got the expected verdict in 7 of 7
  calls.

## What they did

| case | LiveKit | AIVC CE | AVA |
| --- | --- | --- | --- |
| `invite-retransmit` | pass 10/10 | pass 10/10 | pass 10/10 |
| `refer-lost` | pass 10/10 | pass 10/10 | pass 10/10 |
| `bye-lost` | pass 10/10 | pass 10/10 | pass 10/10 |

Milliseconds, median [min, max] over 10 calls, from the caller's capture:

| | LiveKit | AIVC CE | AVA |
| --- | --- | --- | --- |
| INVITE to its 200 OK | 343.1 [316.3, 357.5] | 2.1 [1.8, 2.3] | 4.9 [4.5, 9.0] |
| INVITE copy to the next response | 92.9 [66.0, 106.9] | 0.2 [0.2, 0.2] | 0.3 [0.3, 0.4] |
| first REFER to its copy | 501.0 [500.5, 501.1] | 501.9 [433.2, 557.8] | 500.2 [499.6, 500.8] |
| first BYE to its copy | 500.9 [500.4, 501.0] | 476.6 [436.6, 575.3] | 500.5 [499.5, 500.8] |

- **INVITE copy:** every target answered within T1 (500 ms), so in every call the copy crossed
  the 200 OK on its way. None was still setting the call up when the copy came, the case the
  check of a reply within 1 s is for. The reference agent's proofs cover that case.
- **AI Voice Connector CE and AVA:** they answered the copy itself with the same 200 OK and
  To-tag.
- **LiveKit:** it absorbed the copy (RFC 6026 7.1) and resent the 200 OK by itself, with the same
  To-tag, 250.5 [250.3, 251.2] ms after the first. RFC 3261 13.3.1.4 starts that interval at T1
  (500 ms). No target sent a provisional response or a second final response.
- **REFER and BYE copies:** every target resent its REFER and its BYE on timer E, at T1. AI
  Voice Connector CE's interval varies by about ±70 ms, the others' by under 1 ms. The transfer
  then went on and each target hung up, as in `refer`.

## Raw runs

Attached to the [release](https://github.com/jjaroztegi/rtpbench/releases/tag/retransmit-wave)
as `.tar.zst`; each unpacks to the directory `rtpbench` wrote and judges again from there:

```sh
sha256sum -c --ignore-missing SHA256SUMS && zstd -dc retransmit-aivc-direct-fe41c0856bb3.tar.zst | tar -x
uv run --extra vad rtpbench report aivc-direct
```

| archive | SHA-256 |
| --- | --- |
| `retransmit-livekit-direct-fe41c0856bb3.tar.zst` | `85c8506595b2bb261e01ea724cfc62ecfb91f0b5f0349701b6bd27d554eda159` |
| `retransmit-aivc-direct-fe41c0856bb3.tar.zst` | `c553650ee804831c679dd41fbadcada3a0f77b4a885f9b002fca2a15b752752e` |
| `retransmit-ava-direct-fe41c0856bb3.tar.zst` | `11a1383738332d5bd7704e294a5752b99c5aed13143685550144270062aabd5b` |
| `retransmit-reference-direct-fe41c0856bb3.tar.zst` | `6ae9e8f49d62ca27acfafc9ff173a82a6583b77accf97dc98c9f9d6a9e8af777` |
