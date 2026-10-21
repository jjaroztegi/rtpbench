"""rtpbench's LiveKit target: a LiveKit Agents worker on the OpenAI Realtime model through Azure
OpenAI (`RealtimeModel.with_azure`, as LiveKit's Azure docs set it), on the structure of LiveKit's
starter agent, set up as targets/aivc sets AI Voice Connector CE: the same instructions, welcome
message, voice and tool descriptions, transfers to TRANSFER_TO (LiveKit's documented cold
transfer, a SIP REFER). Before the worker starts, an inbound trunk for the number rtpbench
dials (from any address, no auth: LiveKit wants a number, addresses or auth) and a dispatch rule
that puts each call in its own room, as LiveKit's SIP docs create them.

Env: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT, TRANSFER_TO,
LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET.
"""

import asyncio
import os
import sys
from pathlib import Path

from livekit import api, rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    RunContext,
    cli,
    function_tool,
    get_job_context,
)
from livekit.agents.beta import EndCallTool
from livekit.plugins import openai

NUMBER = "agent"  # the Request-URI user rtpbench calls (bench.TARGETS)
# the compose healthcheck's: the server can dispatch to this worker. Its own health check answers
# once its HTTP server is up, seconds before it registers; a call in between gets a room no
# worker ever joins, and rings unanswered
REGISTERED = Path("/tmp/registered")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful assistant.", tools=[EndCallTool()])

    async def on_enter(self) -> None:
        self.session.generate_reply(
            instructions="Please greet the user with the following: Hello! How can I help you?"
        )

    @function_tool()
    async def transfer_call(self, context: RunContext) -> str:
        """call the function if a request was received to transfer a call with an operator, a
        person"""
        job = get_job_context()
        caller = next(
            p
            for p in job.room.remote_participants.values()
            if p.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
        )
        request = api.TransferSIPParticipantRequest(
            room_name=job.room.name,
            participant_identity=caller.identity,
            transfer_to=os.environ["TRANSFER_TO"],
        )
        try:
            await job.api.sip.transfer_sip_participant(request)
        except Exception as e:
            return f"transfer failed: {e}"
        return "transferred"


server = AgentServer()


@server.on("worker_registered")
def registered(worker_id: str, info: object) -> None:
    REGISTERED.touch()


@server.rtc_session()
async def entrypoint(ctx: JobContext) -> None:
    session: AgentSession = AgentSession(
        llm=openai.realtime.RealtimeModel.with_azure(
            azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"], voice="alloy"
        )
    )
    await session.start(room=ctx.room, agent=Assistant())


async def setup() -> None:
    async with api.LiveKitAPI() as lk:
        for _ in range(60):  # the server may still be starting
            try:
                await lk.sip.list_inbound_trunk(api.ListSIPInboundTrunkRequest())
                break
            except Exception:
                await asyncio.sleep(1)
        await lk.sip.create_inbound_trunk(
            api.CreateSIPInboundTrunkRequest(
                trunk=api.SIPInboundTrunkInfo(name="rtpbench", numbers=[NUMBER])
            )
        )
        rule = api.SIPDispatchRule(
            dispatch_rule_individual=api.SIPDispatchRuleIndividual(room_prefix="call-")
        )
        await lk.sip.create_dispatch_rule(api.CreateSIPDispatchRuleRequest(rule=rule))


if __name__ == "__main__":
    if sys.argv[1:] == ["setup"]:
        asyncio.run(setup())
    else:
        cli.run_app(server)
