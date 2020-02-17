import logging
import sys
import traceback
from datetime import datetime
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
)
from botbuilder.schema import Activity, ActivityTypes

from bots import EchoBot
from config import DefaultConfig


config = DefaultConfig()

settings = BotFrameworkAdapterSettings(config.APP_ID, config.APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)

# Catch-all for errors
async def on_error(context, error):
    # TODO: switch to logging to Azure application insights
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    await context.send_activity("The bot encountered and error or bug")
    # send a trace activity if Bot Framework Emulator
    if context.asctivity.channel_id == 'emulator':
        trace_activity = Activity(
            label = "TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error"
        )
        await context.send_activity(trace_activity)

adapter.on_turn_error = on_error

bot = EchoBot()

async def messages(req):
    # Main bot message handler
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=415)
    activity = Activity().deserialize(body)
    auth_header = (
        req.headers["Authorization"] if "Authorization" in req.headers else ""
    )

    try:
        await adapter.process_activity(activity, auth_header, bot.on_turn)
        return Response(status=201)
    except Exception as exception:
        raise exception

async def test_hello(req):
    return web.Response(text="Skynet is almost here - " + str(datetime.utcnow()))

app = web.Application(middlewares=[aiohttp_error_middleware])

logging.basicConfig(level=logging.DEBUG)
app.router.add_get("/test/hello", test_hello)
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(app, host="localhost", port=config.PORT)
    except Exception as error:
        raise error