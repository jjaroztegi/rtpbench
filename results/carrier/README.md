# The reference agent and AI Voice Connector CE through a carrier

2026-10-14: the reference agent and AI Voice Connector CE behind the [carrier](../../docs/targets.md#carrier), every
call repeated 10 times under each network profile. The exception is the three signalling
mutations against AI Voice Connector CE, on clean only: SIP is never impaired, so the other
profiles cannot change what reaches the agent. Summaries, per-call records and reports are in
this folder; the captures are not published.

```sh
uv run --extra vad rtpbench cases --carrier --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench cases --only ssrc-change,reinvite --profiles clean,lte,lte-bad --runs 10
uv run --extra vad rtpbench target aivc --carrier --profiles clean,lte,lte-bad --runs 10 \
  --only greeting,bye,cancel,hold,dtmf-rfc4733,dtmf-info,refer,refer-fail,timer,ptime-30,ssrc-change,reinvite
uv run --extra vad rtpbench target aivc --carrier --profiles clean --runs 10 \
  --only compact-headers,sdp-ssrc,late-offer
uv run rtpbench calibrate --carrier --profiles clean,lte,lte-bad --turns 50
```

Conditions are those of the [first results](../first), plus OpenSIPS 3.6.9 and rtpengine 12.5.1.31 in the
carrier. Calls were placed at commit 9677e36, except the reference agent through the carrier,
placed at ba5f743: the same code with a larger capture buffer. A run at 9677e36 was voided when
the carrier's capture dropped a packet. Each profile ran as its own process.

The carrier does not change how exactly rtpbench times the wire. Through it, wire timing stays
exact against truth on all three profiles (0.00 ms), so the ±0.4 ms bar stands. Its own transit
per packet is 0.07-0.11 ms at the median and 0.13-0.22 ms at p95, with single packets up to
14 ms.

## What a carrier sends

The reference agent column covers both behaviours of each case, under clean, `lte` and `lte-bad`.
For AI Voice Connector CE, a passing cell gives the time from the end of the caller's question to
the agent's reply, as median [min, max] in ms with its error bar.

| case | what reaches the agent | reference agent | AIVC CE, clean | AIVC CE, lte | AIVC CE, lte-bad | why AIVC CE fails |
| --- | --- | --- | --- | --- | --- | --- |
| `compact-headers` | `f:` `t:` `i:` `c:` for From, To, Call-ID, Content-Type | proven 60/60 | **fail** 10/10 | | | 500 Server Internal Error |
| `sdp-ssrc` | an offer with `a=ssrc:<id>` and no attribute | proven 60/60 | **fail** 10/10 | | | no response at all: the caller gives up after 32 s |
| `late-offer` | an INVITE without SDP | proven 60/60 | **fail** 10/10 | | | 500 Server Internal Error |
| `ptime-30` | the caller's audio in 30 ms packets | proven 60/60 | pass 10/10; 1047 [978, 1138] (−24/+88) | pass 10/10; 1139 [1028, 4458] (−25/+88) | pass 10/10; 1159 [1020, 6025] (−35/+97) | |
| `ssrc-change` | the caller's audio from a new RTP source mid-call | proven 60/60, and 60/60 direct | pass 10/10; 1004 [958, 1150] (−24/+88) | pass 10/10; 1080 [970, 2263] (−25/+88) | pass 10/10; 1120 [1015, 1447] (−35/+97) | |
| `reinvite` | a session refresh (re-INVITE, same SDP) | proven 60/60, and 60/60 direct | pass 10/10; 1049 [948, 4609] (−24/+88) | pass 10/10; 1155 [1002, 3191] (−25/+88) | pass 10/10; 1156 [1009, 1256] (−35/+97) | |

## Everything else through the carrier

The carrier changes none of the reference agent's verdicts in the other cases. Every behaviour
is proven under every profile (690/690 calls); the codec cases run without the carrier
([why](../../docs/cases.md#through-the-carrier)). AI Voice Connector CE gets the verdicts of the [first results](../first), with two single
flips, both from the model rather than the carrier:
- `refer` on clean: once, no REFER and no reply in 20 s, although the engine's transcript shows
  it heard the request.
- `bye` on `lte-bad`: once inconclusive, the agent silent at the BYE.

Its unanswered SIP INFO now ends in the carrier's own 408 after about 30 s.

So AI Voice Connector CE takes in its stride what a carrier does to the media: 30 ms packets, a
new RTP source mid-call, a session refresh. It fails every signalling variation at the first
message. Compact header names and a bare `a=ssrc` each have one public report behind them. An
INVITE without SDP is what Cisco Unified CM trunks send by default.

These runs predate a carrier fix; see
[a correction](../bare-metal-mock#a-correction-to-the-earlier-carrier-results).
