# Targets, your own agent, the mock engine and the carrier

## Targets

```sh
uv run --extra vad rtpbench target livekit --mock   # no AI account needed
uv run --extra vad rtpbench target aivc --mock
uv run --extra vad rtpbench target ava --mock
export OPENAI_API_KEY=...                           # see targets/aivc/compose.yaml
uv run --extra vad rtpbench target aivc             # on the real engine
```

A target is a voice agent that runs in Docker next to the reference stack, so the caller reaches
it through the same netem router. `rtpbench target NAME` runs every case, a 12-turn latency call
and a 10-turn barge-in call against it (`--only` picks among them), with `--profiles` and
`--runs` as for the cases. `summary.md` holds the verdicts, then turn latency and barge-in over
every turn of every repeat, how evenly the target's RTP reached the caller and, on the mock
engine, what of its answers' audio reached the caller as sent and of the caller's reached the
engine; `target.log`, the target's own logs.

| target | what |
| --- | --- |
| [`aivc`](../targets/aivc) | [OpenSIPS AI Voice Connector CE](https://github.com/OpenSIPS/opensips-ai-voice-connector-ce) at a pinned commit on OpenSIPS 3.6, openai flavor as upstream's example sets it, transferring to the operator. Without `--mock`, needs `OPENAI_API_KEY`; `OPENAI_URL` points it at another Realtime endpoint (such as Azure OpenAI `wss://<resource>.openai.azure.com/openai/v1/realtime?model=<deployment>`). Set `OPENAI_REASONING_EFFORT=` (empty) for a model without reasoning, such as gpt-realtime-1.5: with the default, the session setup is rejected and the caller hears noise |
| [`ava`](../targets/ava) | Asterisk 22 (certified 22.8, an [andrius/asterisk](https://github.com/andrius/asterisk) image with Asterisk's AudioSocket modules added) and [AVA](https://github.com/hkjarral/AVA-AI-Voice-Agent-for-Asterisk) (Asterisk AI Voice Agent), an ARI app, at a pinned commit, on its OpenAI Realtime provider with AVA's golden configuration for it, transferring to the operator. Without `--mock`, needs `OPENAI_API_KEY`; `OPENAI_BASE_URL` points it at another Realtime endpoint, `OPENAI_MODEL` names the model (default `gpt-realtime-2.1`). `AVA_EGRESS_PACER=false` turns off the egress pacer that configuration turns on; `AVA_TRANSPORT=externalmedia` hands AVA the call audio over RTP instead of AudioSocket |
| [`livekit`](../targets/livekit) | [LiveKit](https://github.com/livekit/livekit) server and [SIP bridge](https://github.com/livekit/sip) as livekit/sip's compose runs them, and a [LiveKit Agents](https://github.com/livekit/agents) worker on the OpenAI Realtime model through Azure OpenAI (`with_azure`), given AI Voice Connector CE's instructions, greeting, voice and tools, and a cold transfer. Without `--mock`, needs `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY`; `AZURE_OPENAI_DEPLOYMENT` names the deployment (default `gpt-realtime-2.1`) |

Images are pinned by digest. Upstream ships no SIP + Realtime compose for LiveKit, so its agent
is rtpbench's own, on LiveKit's documented settings. LiveKit converts the call audio for the
engine; AI Voice Connector CE passes G.711 through. AVA converts it too, behind Asterisk, which
answers the call and bridges it to AVA over AudioSocket (TCP, 16-bit linear, as AVA's golden
configuration ships) or, with `AVA_TRANSPORT=externalmedia`, over RTP (G.711). The variable
also selects the profile AVA sends with: `slin` for AudioSocket, `ulaw` for ExternalMedia.

What `targets/ava` changes from AVA's golden configuration, and why:
- The andrius image leaves Asterisk's AudioSocket modules out, so `compose.yaml` builds those three
  from the same release tarball and build options and adds them. For ExternalMedia, the profile
  has to send `ulaw`: left at `slin`, AVA sends 16-bit samples in PCMU packets, the caller hears
  noise, and nothing reports an error.
- It enables AVA's transfer tool, to one destination. AVA does not refer the call itself: it
  hands it to an Asterisk dialplan extension and ends its session there. `Transfer()` in
  [`extensions.conf`](../targets/ava/extensions.conf) sends the REFER, so its outcome never
  reaches the engine, and the call ends after it either way.
- The rest is as shipped, including the hang-up of a caller silent for about 50 s (AVA's
  `no_input`).

## Your own agent

```sh
uv run --extra vad rtpbench target sip:agent@203.0.113.7:5080 --profiles clean,lte
uv run --extra vad rtpbench target sip:agent@agent --network myagent_default   # in Docker here
```

`rtpbench target URI` places the same calls from the same caller container, through the netem
router, and judges them the same way. Only the router's setup differs: it masquerades the
caller, so replies come back through it and netem holds both ways. The profile adds to the real
path beyond the router, which the error bars do not cover. `rtpbench check` passes or fails
the run against a policy, for CI ([CI](ci.md)).

Our offer carries the caller's address inside Docker. An agent that sends its audio back to
where ours comes from (symmetric RTP, as AI Voice Connector CE does) needs nothing more; one
that sends it to the offered address (LiveKit) needs an address that reaches the caller:
- `--network NAME`: the agent runs in Docker on this host, on that network (Docker drops traffic
  between its networks otherwise). The router joins it, and the caller advertises the router's
  address there.
- `--advertise HOST:PORT`: an address of this host the agent can reach. The host publishes PORT
  and the next 7 (UDP and TCP), the caller's SIP and RTP ports; forward them to it if a NAT is in
  between.

When the agent's audio never arrives, a latency or barge-in call ends after its first turn's
reply time and the summary says so, and a failed case gets the check `agent RTP arrived`, both
with the address our offer gave.

`--lines DIR` replaces the caller's lines ([`corpus/lines/en`](../corpus/README.md)) with ones in
your agent's language, under the same file names: `turn-NN.wav` for the latency call,
`prompt-NN.wav` and `interrupt-NN.wav` for barge-in, `prompt.wav` and `transfer.wav` for the
cases. Each is 8 kHz mono 16-bit with silence around the speech, as the corpus processes its
clips: the labeller finds where speech ends from it, and refuses a file without.

A transfer's INVITE goes to the stack's operator over UDP, whatever host, number or scheme the
agent's Refer-To names, so a test run never calls a real person, and `refer` and `refer-fail`
judge the agent alone. To reach a real transferee, `--proxy HOST` sends the INVITE there
instead, over UDP, or over TLS as `--proxy sips:HOST`, trusting `--ca` as a `sips:` URI does
(a name on the agent's Docker network works with `--network`). An agent that demands digest
authentication gets it from `RTPBENCH_SIP_USER` and `RTPBENCH_SIP_PASSWORD`
([below](#digest-authentication)).

The URI's host is looked up as an address record (no SRV or NAPTR, so give its port), and not on
loopback: from Docker, this host is its own address. `conditions.json`, the summary and the
captures name the URI and the addresses on the path. A `sips:` URI, or one with
`;transport=tls`, puts SIP on TLS, and `--srtp` the media on SRTP ([below](#tls-and-srtp)).

The summary's RTP pacing is what reached the caller: the agent's own pacing plus the real path's
jitter. To split the two, capture whole packets at the agent for the length of the run
(`tcpdump -i any -w agent.pcap udp`: a classic pcap, not pcapng) and judge again with
`rtpbench report DIR --agent-pcap agent.pcap`. Packets pair by SSRC, sequence number and
timestamp, and by payload unless the call is SRTP, so a call through a media relay that rewrites
them (one that repacketizes to another ptime, say) is reported as not matched. The two hosts'
clocks need no sync: the path's figure is taken against a line that follows their offset and
rate difference. The capture is copied into DIR as `agent-side.pcap`, so it ships with the run
and any archive of it, with the addresses it saw and, without SRTP, the call audio.

## TLS and SRTP

```sh
uv run --extra vad rtpbench target 'sip:agent@agent.example.com;transport=tls' --srtp
uv run --extra vad rtpbench target sips:agent@agent --network myagent_default --ca agent-ca.pem
uv run --extra vad rtpbench cases --tls --srtp
```

On port 5061 unless the URI gives one: TLS 1.3, or 1.2 with an AES-GCM or ChaCha20 suite (the
only ones the caller offers there). The caller checks the agent's certificate for the URI's host
against the system's trusted certificates, or those in `--ca` (PEM). Its connection leaves from
the port its Contact gives (and its Via, with RFC 5923 `alias`), so an agent that sends its own
requests (a BYE, a REFER) to the Contact finds that connection and uses it. One that opens a new
connection reaches the caller only if the way back is open (`--advertise`), and must not check
the caller's certificate, a test one.

TLS hides SIP from the capture, so the caller writes each call's session keys to `keys.log`
next to its capture, and judging decrypts the messages from the capture with them: each message
is timed by the packet that brought the start of its TLS record. The same file opens the
capture in Wireshark (TLS protocol preferences, (Pre)-Master-Secret log filename). Anyone with
the results reads that call's signalling, and only that call's: TLS protects nothing beyond test
calls here. With [digest authentication](#digest-authentication) the captures then hold the
digest, as over UDP.

`cases --tls` and `calibrate --tls` reach the reference agent over TLS, with a certificate from a
CA the stack makes for the run (both kept in the results' `tls/`); with `--carrier`, the carrier
takes both on the caller's leg ([below](#carrier)). `large-invite`, `invite-retransmit`,
`refer-lost` and `bye-lost` do not run over TLS: they are about UDP. `conditions.json` records `tls` and what the
caller trusted (`tls_trust`); each call's `caller.json`, the TLS version and cipher suite, which
the summary counts.

`--srtp` offers SRTP keyed in the SDP (SDES, RFC 4568: `RTP/SAVP` with an `a=crypto` line per
suite): AES_CM_128_HMAC_SHA1_80, AES_CM_128_HMAC_SHA1_32 and AEAD_AES_128_GCM (RFC 7714), in that
order; `--srtp SUITE,...` offers those instead. That is what trunks and hosted agents use, OpenAI's
among them; DTLS-SRTP (WebRTC's keying) is not supported. An answer without SRTP, or with an MKI
or session parameters, ends the call. The keys travel in the SDP, so judging reads them from the
captured SIP and opens each side's packets with that side's key, its rollover counter guessed
per SSRC (RFC 3711 3.3.1); packets that none authenticates are left out, and the summary counts
them. Over plain SIP the keys are in the capture in the clear, and with TLS anyone with
`keys.log` reads them: they protect only that test call. `conditions.json` records the suites
offered (`srtp`); each call's `caller.json`, the one taken.

## Mock engine

`--mock` puts a deterministic stand-in for the OpenAI Realtime API (GA protocol) where the
target expects its engine ([`realtime.py`](../src/rtpbench/realtime.py)). The target's code is
unchanged, and the target has no route out, so no paid engine can be reached.

The mock ends a turn after 1 s of silence and answers 500 ms later: with a fixed clip, a longer
one to the long question, or a call to the transfer tool to the transfer line (named
`transfer_call`, or `blind_transfer` as AVA names it, with `operator` in every required text
argument; a tool with any other required argument is not called). Speech while it answers
cancels the answer. It logs when it heard each turn end and when it sent its first
audio, on the captures' clock, so the summary splits turn latency and greeting time into the
target's uplink, the engine's fixed share and the target's downlink. It records what it
receives as it arrives (`realtime/` in the run directory), so the summary also compares the
caller's lines with what reached the engine.

It recognises the caller's own lines, not speech in general: it names the nearest line by the
shape of its energy envelope, whatever the level and through lost packets. A target's audio path
can change the audio a lot: LiveKit's raises the caller's level by anything from 0 to 12 dB,
line to line ([media path](../results/media-path)). A new set of caller lines needs lengths
that stay apart from the transfer line's.

What the mock cannot stand in for is the model: what it understands, and when it decides to
transfer or to stop for a backchannel. Against a mock, `greeting` times the stack, `refer` the
transfer mechanics, `refer-fail` whether the failure reaches the engine, and the DTMF cases
whether a digit reaches it at all.

### An agent of your own on the mock

`--mock` wires the mock into the bundled targets only. Your own agent can use it if its engine
URL can lead there: `uv run rtpbench realtime --out DIR` serves it as plain `ws` on port 8000.
The agent then relays audio and the mock recognises rtpbench's own lines, so leave out
`--lines`. What the agent has to meet:

- The session shape of the OpenAI Realtime GA API. The mock reads the audio format from
  `session.audio.input.format.type` (`audio/pcmu`, `audio/pcma`, else 24 kHz PCM16) only; an
  agent that sends the preview shape (`input_audio_format`) is heard as 24 kHz PCM16.
- An endpoint it accepts. The mock ignores the path, the query and any auth header. Over plain
  `ws` that header crosses the network in clear: give the agent a dummy key, not a live token.
  An agent that takes only `wss` URLs under its provider's host names and verifies TLS needs
  both overridden on its side: that host name resolving to the mock (a hosts entry or DNS),
  and a TLS proxy in front of the mock with a certificate for that name from a CA the agent
  trusts. The token it fetches then travels inside TLS.
- For `refer`, a transfer tool named as above.

The split of turn latency into uplink, engine and downlink needs the mock's log on the
captures' clock: run the mock on the host that runs `rtpbench target`, and write its log into
the run's directory (DIR is the run's `--out`, or copy `realtime.jsonl` and `realtime/` there
and run `rtpbench report`). End-to-end turn latency comes from the caller's capture alone and
does not depend on where the mock runs.

## Carrier

```sh
uv run rtpbench calibrate --carrier --profiles clean --turns 20
uv run --extra vad rtpbench cases --carrier
uv run --extra vad rtpbench target aivc --carrier
```

`--carrier` puts a carrier between the router and the agent, as a trunk puts an SBC in front of
a PBX ([`carrier/`](../carrier)): OpenSIPS 3.6 as a stateful proxy that hides the topology (the
agent sees the carrier's Via, Contact and Call-ID), and rtpengine anchoring the media of both
legs. The caller's leg crosses the netem router; the carrier-agent leg does not. Both carrier
legs are captured (`carrier.pcap`), and the calibration adds the carrier's own transit time per
packet: 0.1 ms or less at the median. Which cases change through it is in
[cases](cases.md#through-the-carrier).

```sh
uv run --extra vad rtpbench cases --carrier --tls --srtp
uv run --extra vad rtpbench target aivc --mock --carrier --tls --srtp
```

With `--tls` and `--srtp` the caller's leg is SIP over TLS on 5061 and SRTP, as trunks offer
them ([`tls.cfg`](../carrier/tls.cfg)): OpenSIPS ends TLS with the stack's test certificate,
rtpengine ends SRTP, and the agent's leg stays plain SIP over UDP and RTP, as an SBC in front of
a PBX would leave it. A bundled target that takes neither (AI Voice Connector CE's media is plain
RTP) is judged this way behind a secure trunk. The caller's `keys.log` reads that leg in
`carrier.pcap` too, and the carrier's transit time then includes rtpengine's encryption.

## Digest authentication

```sh
export RTPBENCH_SIP_USER=... RTPBENCH_SIP_PASSWORD=...
uv run --extra vad rtpbench cases --carrier
```

With both variables set, the caller answers a 401 or 407 to any request it sends with digest
credentials (RFC 7616: MD5 or SHA-256, qop auth or none) and sends it again, once; the carrier
demands them, MD5 on the INVITE and SHA-256 inside the dialog. A challenged request, its
challenge and their ACK are left out when a case is judged, so verdicts and timings read as
without credentials. `conditions.json` records `sip_auth`, never the values; the captures hold
the user name and, per request, a digest of the password that a dictionary attack can test, so
publish captures only from a throwaway password.
