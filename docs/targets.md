# Targets, the mock engine and the carrier

## Targets

```sh
uv run --extra vad rtpbench target livekit --mock   # no AI account needed
uv run --extra vad rtpbench target aivc --mock
export OPENAI_API_KEY=...                           # see targets/aivc/compose.yaml
uv run --extra vad rtpbench target aivc             # on the real engine
```

A target is a voice agent that runs in Docker next to the reference stack, so the caller reaches
it through the same netem router. `rtpbench target NAME` runs every case, a 12-turn latency call
and a 10-turn barge-in call against it (`--only` picks among them), with `--profiles` and
`--runs` as for the cases. `summary.md` holds the verdicts, then turn latency and barge-in over
every turn of every repeat; `target.log`, the target's own logs.

| target | what |
| --- | --- |
| [`aivc`](../targets/aivc) | [OpenSIPS AI Voice Connector CE](https://github.com/OpenSIPS/opensips-ai-voice-connector-ce) at a pinned commit on OpenSIPS 3.6, openai flavor as upstream's example sets it, transferring to the operator. Without `--mock`, needs `OPENAI_API_KEY`; `OPENAI_URL` points it at another Realtime endpoint (such as Azure OpenAI `wss://<resource>.openai.azure.com/openai/v1/realtime?model=<deployment>`). Set `OPENAI_REASONING_EFFORT=` (empty) for a model without reasoning, such as gpt-realtime-1.5: with the default, the session setup is rejected and the caller hears noise |
| [`livekit`](../targets/livekit) | [LiveKit](https://github.com/livekit/livekit) server and [SIP bridge](https://github.com/livekit/sip) as livekit/sip's compose runs them, and a [LiveKit Agents](https://github.com/livekit/agents) worker on the OpenAI Realtime model through Azure OpenAI (`with_azure`), given AI Voice Connector CE's instructions, greeting, voice and tools, and a cold transfer. Without `--mock`, needs `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY`; `AZURE_OPENAI_DEPLOYMENT` names the deployment (default `gpt-realtime-2.1`) |

Images are pinned by digest. Upstream ships no SIP + Realtime compose for LiveKit, so its agent
is rtpbench's own, on LiveKit's documented settings. LiveKit converts the call audio for the
engine; AI Voice Connector CE passes G.711 through.

## Mock engine

`--mock` puts a deterministic stand-in for the OpenAI Realtime API (GA protocol) where the
target expects its engine ([`realtime.py`](../src/rtpbench/realtime.py)). The target's code is
unchanged, and the target has no route out, so no paid engine can be reached.

The mock ends a turn after 1 s of silence and answers 500 ms later: with a fixed clip, a longer
one to the long question, or a call to the transfer tool to the transfer line. Speech while it
answers cancels the answer. It logs when it heard each turn end and when it sent its first
audio, on the captures' clock, so the summary splits turn latency and greeting time into the
target's uplink, the engine's fixed share and the target's downlink.

It recognises the caller's own lines, not speech in general: it names the nearest line by the
shape of its energy envelope, whatever the level and through lost packets. A target's audio path
can change the audio a lot; LiveKit's makes the caller about 10 dB louder and compresses it. A
new set of caller lines needs lengths that stay apart from the transfer line's.

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
