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
clips: the labeller finds where speech ends from it, and refuses a file without. `--proxy HOST`
is where a transfer's INVITE goes (by default the Refer-To host, as the caller resolves it: give
`--proxy` when it is a name on the agent's Docker network). An agent that demands digest
authentication gets it from `RTPBENCH_SIP_USER` and `RTPBENCH_SIP_PASSWORD`
([below](#digest-authentication)).

The URI's host is looked up as an address record (no SRV or NAPTR, so give its port), and not on
loopback: from Docker, this host is its own address. `conditions.json`, the summary and the
captures name the URI and the addresses on the path. SIP over TLS (`sips:`) and SRTP are not
supported: TLS hides SIP from the capture, so judging would need its session keys (a key log)
to read it; SRTP needs AES counter mode and HMAC-SHA1 (a new dependency) and its keys kept with
the captures to judge the audio.

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
