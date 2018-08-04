import logging
import time

from dorpsgek_irc import watcher

log = logging.getLogger(__name__)


@watcher.register("welcome")
async def welcome(event, ws, irc):
    await ws.send_event("register", {"protocol": "irc"})
    await ws.send_event("ping", {"time": time.time()})
    log.info("Watcher registered")
