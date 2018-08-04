from dorpsgek_irc import watcher


@watcher.register("pong")
async def pong(event, ws, irc):
    # Currently no action needed
    pass
