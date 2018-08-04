import aiohttp
import asyncio
import importlib
import logging

import irc3
from aiohttp import WSMsgType

from dorpsgek_irc import (
    config,
    watcher,
)
from dorpsgek_irc.load_config import load_config
from dorpsgek_irc.watcher import WatcherEventDoesntExist

log = logging.getLogger(__name__)
# These watcher_commands should always be loaded to have a functional watcher.
# They do not contain any code that can be executed.
WATCHER_COMMANDS_ALWAYS_LOAD = ["pong", "registered", "welcome"]


class WSEvent:
    """Event that comes from a websocket."""
    def __init__(self, type, data=None):
        self.type = type
        self.data = data


async def ws_send_event(self, event, data=None):
    """Easy helper function to send an event over the wire."""
    payload = {
        "type": event,
    }
    if data:
        payload["data"] = data

    await self.send_json(payload)
aiohttp.client_ws.ClientWebSocketResponse.send_event = ws_send_event


async def run(irc, session, address):
    log.info("Connecting to '%s' ...", address)
    try:
        ws = await session.ws_connect(address)
    except aiohttp.client_exceptions.ClientConnectorError:
        log.error("Failed to connect to '%s'", address)
        return

    log.info("Connection established; waiting for welcome message")

    async for msg in ws:
        if msg.type == WSMsgType.CLOSED:
            break
        elif msg.type == WSMsgType.TEXT:
            raw = msg.json()
            if raw["type"] == "request":
                wants_response = True
                event = WSEvent(raw["data"]["type"], raw["data"].get("data"))
            else:
                wants_response = False
                event = WSEvent(raw["type"], raw.get("data"))

            try:
                await watcher.process_request(event, ws, irc, wants_response)
            except WatcherEventDoesntExist as err:
                await ws.send_event("error", {"command_does_not_exist": err.args[0]})
        else:
            log.error(f"Unexpected message type {msg.type}")
            break


async def run_forever(irc, address):
    while True:
        session = aiohttp.ClientSession()
        try:
            await run(irc, session, address)
            log.info("Lost connection to server")
        except Exception:
            log.exception("Unexpected error")
        finally:
            await session.close()

        # Make sure we don't hammer the server on errors
        log.info("Waiting 5 seconds before retrying to connect ...")
        await asyncio.sleep(5)


def main():
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO)
    load_config()

    for command in config.WATCHER_COMMANDS.split() + WATCHER_COMMANDS_ALWAYS_LOAD:
        importlib.import_module(f"dorpsgek_irc.watcher_commands.{command}")

    cfg = irc3.utils.parse_config("bot", "dorpsgek.ini")
    irc = irc3.IrcBot.from_config(cfg)

    irc.run(forever=False)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_forever(irc, config.DORPSGEK_ADDRESS))


if __name__ == "__main__":
    main()
