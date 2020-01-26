import logging
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core.integration import aiohttp_error_middleware
from datetime import datetime
from config import DefaultConfig

config = DefaultConfig()

async def test_hello(req):
    return web.Response(text="Skynet is almost here - " + str(datetime.utcnow()))

app = web.Application(middlewares=[aiohttp_error_middleware])
logging.basicConfig(level=logging.DEBUG)
app.router.add_get("/test/hello", test_hello)

if __name__ == "__main__":
    try:
        web.run_app(app, host="localhost", port=config.PORT)
    except Exception as error:
        raise error