# Conformance cases

```sh
uv run --extra vad rtpbench cases                      # prove every case against the reference agent
uv run --extra vad rtpbench cases --profiles clean,lte,lte-bad --runs 10
```

Each case ([`cases.py`](../src/rtpbench/cases.py)) is a scripted call with a verdict (pass, fail
or inconclusive) and timings, each timing with its [error bar](calibration.md#error-bars).
`rtpbench cases` runs every case against the reference agent once with a behaviour that should
pass it and once with each behaviour that should fail it (for `timer`, also once without the
extension, which is inconclusive), so the case itself is proven; the command fails on any
unexpected verdict. `rtpbench target` runs them against an agent
([targets](targets.md)).

With `--runs N`, repeat k uses seed + k − 1. Verdicts are counted ("pass 10/10"); a case whose
verdict changes between repeats reads "flips: pass 7, fail 3", and fails the reference run.
Timings read median [min, max]. `report.html` draws, per call, the SIP messages, speech and RTP
of both sides on one time axis; `rtpbench report DIR` judges a finished run again.

Against the reference agent the caller says a corpus utterance; against a target, `prompt.wav`
(a question) and `transfer.wav` (asking for a person) from [`corpus/lines`](../corpus/README.md).
Transfers go to the operator, a service on the agent's side of the router that rings for a
second and answers, or answers 486 for `refer-fail`. Bundled targets refer to
`sip:operator@operator`; against a URI the transferee calls the operator whatever the Refer-To
names.

| case | what passes |
| --- | --- |
| `greeting` | the agent speaks first, within 2 s of its 200 OK |
| `bye` | caller hangs up at least a second into the agent's speech: 2xx to BYE, agent RTP stops within 500 ms |
| `cancel` | caller cancels a ringing INVITE: 2xx to CANCEL, 487 to the INVITE, no RTP after |
| `hold` | hold (sendonly, then inactive) and resume by re-INVITE: answers honour the offer, no agent RTP while held, RTP back within 1 s as the same stream (SSRC, next seq, timestamps kept time) |
| `dtmf-rfc4733` | once the greeting is over the caller presses 5 (RFC 4733): telephone-event negotiated, the agent says something within 5 s |
| `dtmf-info` | the same by SIP INFO (`application/dtmf-relay`): 2xx, the agent says something within 5 s |
| `refer` | the caller asks for a person: REFER with a SIP or tel Refer-To, 202, NOTIFY sipfrag 100, a real call to the target, NOTIFY with its final response, both NOTIFYs answered 2xx, the agent hangs up within 10 s. If the target does not answer 2xx, inconclusive, with its status: the agent should then take the call back, as `refer-fail` checks |
| `refer-fail` | as `refer`, but the target is busy (`486 Busy Here`): the agent takes the call back (RFC 5589 6.3): no BYE for 10 s, and it speaks within 5 s of the failure NOTIFY |
| `codec-pcmu` | the caller offers PCMU alone: answered with PCMU alone (RFC 3264 6.1) and the agent's RTP is PCMU |
| `codec-pcma` | the same with PCMA |
| `timer` | session timers offered (90 s, caller refreshes), refreshed once at half time, then not again: the 2xx takes them (RFC 4028), the refresh gets 2xx with media undisturbed, the agent ends the session by BYE 45-90 s after the refresh. The offer says `Supported: timer`, not `Require`, so an agent without timers (a 2xx without Session-Expires) is inconclusive (RFC 4028 9: the extension is optional) |
| `ssrc-change` | after the greeting the caller's audio becomes a new RTP source (RFC 3550 8): the agent replies to a question within 10 s |
| `reinvite` | after the greeting, a session refresh by re-INVITE with the same SDP: 2xx `sendrecv`, media undisturbed, a reply within 10 s |
| `reinvite-nosdp` | a re-INVITE without SDP, as PBXs send to move or audit media (RFC 3261 14.1): the 2xx offers the call's codec, the caller answers in the ACK, media undisturbed, a reply within 10 s |
| `hold-zero` | hold the RFC 2543 way, `c=0.0.0.0` and no direction attribute, then resume (RFC 3264 8.4): 2xx, no agent RTP while held, RTP back within 1 s as the same stream |
| `codec-change` | a re-INVITE offers the other G.711 law alone and the caller switches on the 2xx: the answer has that law alone, the agent's RTP switches, a reply within 10 s |
| `large-invite` | an INVITE over 1300 bytes goes over TCP (RFC 3261 18.1.1 MUST): answered 2xx over TCP and a reply within 10 s; a refused connection is retried over UDP, for the record. Not over TLS |
| `refer-lost` | as `refer`, but the caller leaves the agent's first REFER unanswered, as if lost: a copy within 1 s (2*T1; over UDP timer E fires at T1, RFC 3261 17.1.2.2), then the transfer as in `refer`. Without a copy, the caller waits for the agent's timer F (32 s) and notes whether it spoke again. Not over TLS |
| `bye-lost` | as `refer`, but the caller leaves the agent's BYE after the transfer unanswered: a copy within 1 s. Inconclusive if the agent never hangs up. Not over TLS |
| `invite-retransmit` | the caller loses every response for T1 (500 ms), so it sends the INVITE again then, as timer A does: before a final response, the copy gets a provisional or final one within 1 s (RFC 3261 17.2.1); after a 2xx, the agent resends it until ACKed (13.3.1.4) and absorbs the copy or answers it with that 2xx (RFC 6026 7.1). Every final response is the same (status and To-tag). `INVITE to the 2xx` under T1 means the agent had already answered. Not over TLS |

An agent may send RTP only while it speaks (silence suppression, RFC 3551 4.1). When it sent
nothing for a second before a hold or a refresh, its silence afterwards is not the request's
doing: after a resume, nothing from it makes the check inconclusive. Around a refresh, when its
stream pauses elsewhere in the call (the same stream going on after a second or more, which a
loss burst cannot fake), its next RTP must go on with the same stream (SSRC, next sequence
number), or the check is inconclusive if none came. The summary's RTP section reports each pause
outside a hold: how many per call, and whether the RTP clock kept time across it (RFC 3550 5.1)
and marked the restart. Speech is detected with every pause heard as silence: joined by sequence
number alone, a reply would run on from the speech before the pause, and its onset go unheard.

## Through the carrier

With `--carrier`, four more cases are what real trunks send; the carrier rewrites the call and
the agent must answer and reply to a question within 10 s:

| case | what reaches the agent |
| --- | --- |
| `compact-headers` | `f:`, `t:`, `i:`, `c:` for From, To, Call-ID, Content-Type (RFC 3261 7.3.3: MUST accept both forms) |
| `sdp-ssrc` | an offer with `a=ssrc:<id>` and no attribute (invalid per RFC 5576 10; sent by some softphones) |
| `late-offer` | an INVITE without SDP: the agent offers in its 2xx and the ACK answers (RFC 3261 13.2.1; the default of Cisco CUCM trunks) |
| `ptime-30` | the caller's audio in 30 ms packets, offered `a=ptime:30` (RFC 3551 4.2: receivers SHOULD accept 0-200 ms) |

Some cases run without the carrier only, because its media relay (rtpengine) would answer for
the agent:
- `codec-pcmu`, `codec-pcma` and `codec-change`: when the agent answers with a law the caller did
  not offer, rtpengine gives the caller the offered law and transcodes.
- `hold-zero`: rtpengine passes a `c=0.0.0.0` offer on with `a=sendonly` added, which `hold`
  already covers.
- `large-invite`: the carrier takes SIP over UDP (and TLS, with `--tls`), not TCP.
- `refer-lost` and `bye-lost`: the carrier's own transaction resends the agent's request to the
  caller.
- `invite-retransmit`: the carrier's own transaction answers the caller's copy; the agent never
  sees it.
