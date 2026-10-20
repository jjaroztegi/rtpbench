# AI Voice Connector CE at b95f5af: the baseline's sets again

2026-10-20: AI Voice Connector CE at upstream main b95f5af (2026-10-20), run as the
[baseline](../baseline) ran it at 09e14d0 (2026-10-12): direct and through the
[carrier](../../docs/targets.md#carrier), under three network profiles, 10 repeats each, on the
[mock engine](../../docs/targets.md#mock-engine), on OpenSIPS 3.6.9. Only the connector differs,
and its example configuration, which now also listens on TCP. Image `rtpbench:f026db2ef9a8`; the
git tag `aivc-b95f5af-wave` is the commit that ran it. Summaries, records and reports are in this
folder, judged again by the code of the commit that added it; the raw run directories are
[archived](#raw-runs).

```sh
uv run --extra vad rtpbench target aivc --mock --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench target aivc --mock --carrier --profiles clean,lte,lte-bad --runs 10 \
  --only greeting,bye,cancel,hold,dtmf-rfc4733,dtmf-info,refer,refer-fail,timer,ptime-30,ssrc-change,reinvite,reinvite-nosdp,compact-headers,sdp-ssrc,late-offer
uv run --extra vad rtpbench cases --profiles clean,lte,lte-bad --runs 1
uv run --extra vad rtpbench cases --carrier --profiles clean,lte,lte-bad --runs 1
```

Conditions: the baseline's host, 16 CPUs, kernel 6.8.0-147-generic, CPU governor `performance`,
Docker 29.9.1; the mock engine waits 1000 ms of silence and answers 500 ms later. The two sets ran
at once, then the reference agent's proofs: 5 h 56 min. The load average stayed between 0.6 and
7.0; 0 clock steps. The reference agent got the expected verdict in 117 of 117 calls direct and
111 of 111 through the carrier; the same day's [calibrations](../ava) measured this host's wire
timing within 0.5 ms.

## What changed

| case | direct, 09e14d0 | direct, b95f5af | carrier, 09e14d0 | carrier, b95f5af |
| --- | --- | --- | --- | --- |
| `refer-fail` | **fail** 30/30 | pass 30/30 | **fail** 30/30 | pass 30/30 |
| `large-invite` | **fail** 30/30 | pass 30/30 | | |
| `compact-headers` | | | **fail** 30/30 | pass 30/30 |
| `sdp-ssrc` | | | **fail** 30/30 | pass 30/30 |
| `refer` | pass 30/30 | pass 30/30 | pass 30/30 | flips: pass 29, fail 1 |

- A failed transfer no longer hangs up on the caller: the connector keeps the call and the engine
  speaks again.
- An INVITE over 1300 bytes, sent over TCP, is taken: the example configuration listens on TCP.
- Compact header names and an `a=ssrc` line without an attribute, as a carrier sends them, are
  understood.
- The one `refer` failure is new, [below](#an-rtp-port-already-in-use).

Every other verdict is the baseline's. Still failing: `hold` (an `inactive` offer answered
`recvonly`), `hold-zero` (about 120 packets sent during a `c=0.0.0.0` hold), `codec-change` (the
old codec in the answer), `reinvite-nosdp`, `late-offer` (500), `timer`, and both DTMF cases (an
INFO now gets 501, where it got no answer at all); `cancel` stays inconclusive.

Timing and audio did not move. Turn latency p50 1511, 1593 and 1604 ms (`clean`, `lte`,
`lte-bad`) against 1512, 1592 and 1605; the connector's own share 9 ms on a clean network. It
stopped for all 100 interjections per profile, 23 ms after an interruption at the median against
24. A receiver needs a 1.1 ms jitter buffer for its RTP on a clean network, against 1.2, and the
engine's speech still reaches the caller sample for sample.

## An RTP port already in use

One `refer` call through the carrier (`lte-bad`, repeat 7) was refused: the connector's OpenSIPS
answered its INVITE `500 Server Internal Error` 3 ms after it arrived, and the connector logged
`Address already in use`. It draws each call's RTP port at random from 35000-65000 and binds it
without a retry. That range overlaps the kernel's ephemeral ports (32768-60999 here), which its
own outbound connections also use, such as the one to the engine. The code is the same at
09e14d0. A deployment avoids the collision by setting `min_port` and `max_port` outside the
ephemeral range.

## Raw runs

Attached to the [release](https://github.com/jjaroztegi/rtpbench/releases/tag/aivc-b95f5af-wave)
as `.tar.zst`; each unpacks to the directory `rtpbench` wrote and judges again from there:

```sh
sha256sum -c SHA256SUMS && zstd -dc aivc-b95f5af-aivc-direct-f026db2ef9a8.tar.zst | tar -x
uv run --extra vad rtpbench report aivc-direct
```

| archive | SHA-256 |
| --- | --- |
| `aivc-b95f5af-aivc-direct-f026db2ef9a8.tar.zst` | `47c344e83fd4ac249cd020e7c13100c4ded39a5077a71e53a6bd231e02113b4d` |
| `aivc-b95f5af-aivc-carrier-f026db2ef9a8.tar.zst` | `99cab08875239a48f7158dccc191c9ba59f3faab93e51126feed63abc485e4c4` |
| `aivc-b95f5af-reference-direct-f026db2ef9a8.tar.zst` | `7c51f345a360f58e68433764debef05af7d35c43fa0636bfc10f0e4351094fe0` |
| `aivc-b95f5af-reference-carrier-f026db2ef9a8.tar.zst` | `87536f86466e8ca73920f2c5ebb7fbe64ff208bcd17e25f67ff15cda0a4f7f5c` |
