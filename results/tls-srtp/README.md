# SIP over TLS and SRTP

2026-10-20: this host's timing error with SIP over TLS and SRTP media on the caller's leg, direct
and through the [carrier](../../docs/targets.md#carrier); every case proven on the reference
agent over TLS and SRTP; and AI Voice Connector CE on the
[mock engine](../../docs/targets.md#mock-engine) behind the carrier, with TLS and SRTP between the
caller and the carrier. How the caller and judging handle both: [TLS and
SRTP](../../docs/targets.md#tls-and-srtp). Image `rtpbench:f026db2ef9a8`; the git tag
`tls-srtp-wave` is the commit that ran it. Summaries, records and reports are in this folder;
the raw run directories are [archived](#raw-runs).

```sh
uv run rtpbench calibrate --tls --srtp
uv run rtpbench calibrate --tls --srtp --carrier
uv run --extra vad rtpbench cases --tls --srtp
uv run --extra vad rtpbench cases --tls --srtp --carrier
uv run --extra vad rtpbench target aivc --mock --carrier --tls --srtp
```

Conditions: as the [baseline](../baseline)'s, on the same host. The five sets ran one after
another, in 59 minutes; the load average stayed between 0.3 and 3.1; 0 clock steps. The
calibrations measured every profile, 20 turns each; the cases and the target ran on a clean
network, one repeat. AI Voice Connector CE at the baseline's version, OpenSIPS 3.6.9.

## Timing on this host

Wire timing against the reference agent's truth (max abs error, ms, 20 turns per profile), with
TLS and SRTP and, from the baseline, without; and the time the carrier adds per packet (p50 /
p95 / max, ms, both directions):

| profile | direct | direct, plain | carrier | carrier, plain | transit, up | transit, down | transit, plain |
| --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 0.00 | 0.00 | 0.00 | 0.00 | 0.06 / 0.10 / 2.0 | 0.07 / 0.10 / 1.6 | 0.05 / 0.08 / 2.3 |
| delay | 0.00 | 0.00 | 0.00 | 0.00 | 0.05 / 0.10 / 2.3 | 0.08 / 0.13 / 3.0 | 0.05 / 0.08 / 2.7 |
| jitter | 0.00 | 0.00 | 0.00 | 0.00 | 0.05 / 0.10 / 0.9 | 0.06 / 0.09 / 1.4 | 0.04 / 0.07 / 2.9 |
| loss | 0.00 | 0.00 | 0.00 | 0.12 | 0.05 / 0.10 / 2.2 | 0.07 / 0.09 / 2.5 | 0.05 / 0.07 / 0.9 |
| mobile | 0.00 | 0.00 | 0.00 | 0.00 | 0.05 / 0.10 / 1.7 | 0.07 / 0.10 / 1.1 | 0.04 / 0.07 / 3.2 |
| lte | 0.00 | 0.00 | 0.00 | 0.00 | 0.05 / 0.10 / 1.7 | 0.07 / 0.10 / 2.9 | 0.04 / 0.07 / 2.2 |
| lte-bad | 0.00 | 0.00 | 4.12 | 0.00 | 0.07 / 0.14 / 0.3 | 0.06 / 0.10 / 0.8 | 0.05 / 0.09 / 0.9 |

TLS and SRTP leave the wire timing as exact as without them. The one exception, `lte-bad`
through the carrier, is one turn whose first packet of speech the network lost: the wire saw the
onset in the next packet, 4.1 ms later. The other four turns there that lost it read 0.00 to
0.25 ms. rtpengine, protecting and opening SRTP on the caller's leg, adds about
0.02 ms per packet at the median. The reference agent's own scheduling error stays within
0.11 ms, as without TLS.

## The cases over TLS and SRTP

| set | calls with the expected verdict | TLS | SRTP |
| --- | --- | --- | --- |
| reference, direct | 37 of 37 | TLSv1.3 TLS_AES_256_GCM_SHA384, 37 calls | AES_CM_128_HMAC_SHA1_80, 36 calls |
| reference, carrier | 37 of 37 | TLSv1.3 TLS_AES_256_GCM_SHA384, 37 calls | AES_CM_128_HMAC_SHA1_80, 33 calls |
| AI Voice Connector CE, carrier | as the baseline's, 16 of 16 | TLSv1.3 TLS_AES_256_GCM_SHA384, 18 calls | AES_CM_128_HMAC_SHA1_80, 15 calls |

The calls without SRTP are the ones whose INVITE gets no answer with SDP (a cancelled call, and
offers the carrier or the target refuses). No SRTP packet failed to authenticate. Behind the
carrier, AI Voice Connector CE gives every case the verdict it got in the baseline's 10 plain
clean repeats, and its turn latency is 1511 ms at p50, against 1512 ms in the baseline: the
caller's TLS and SRTP stop at the carrier, which talks plain SIP and RTP to the target, as a
secure trunk in front of a plain one does.

## Raw runs

Attached to the [release](https://github.com/jjaroztegi/rtpbench/releases/tag/tls-srtp-wave) as
`.tar.zst`; each unpacks to the directory `rtpbench` wrote and judges again from there:

```sh
sha256sum -c --ignore-missing SHA256SUMS && zstd -dc tls-srtp-reference-direct-f026db2ef9a8.tar.zst | tar -x
uv run --extra vad rtpbench report reference-direct
```

Each call's `keys.log` holds its TLS session keys, and its captured SDP the SRTP keys: they are
published on purpose, to open the captures, and protect only these test calls. The certificates
in `tls/` come from a CA made for the run; its private key is not archived.

| archive | SHA-256 |
| --- | --- |
| `tls-srtp-calibrate-f026db2ef9a8.tar.zst` | `768ee7a84ad6aec1c06469c83b6fefe76eaf3faff2b7a1efad130cb75e70d8e7` |
| `tls-srtp-calibrate-carrier-f026db2ef9a8.tar.zst` | `62eb257d7f98b453d38ad860720de551c6cb147752f41796e2987adb7ce6a710` |
| `tls-srtp-reference-direct-f026db2ef9a8.tar.zst` | `b2ba2d8e2ee42ffc4d4dad0a56675d39e67ca4cfc8c4d181c24f65831d8c2c07` |
| `tls-srtp-reference-carrier-f026db2ef9a8.tar.zst` | `5783a07a726dd39005ea926e222323a9a3488398ec047c6af6c7f09d79d75634` |
| `tls-srtp-aivc-carrier-f026db2ef9a8.tar.zst` | `55756ccb259b1efc87a167f313b6a544fa9339d8bb3a6373eddcabcc4072b874` |
