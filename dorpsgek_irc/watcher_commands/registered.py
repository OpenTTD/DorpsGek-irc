from dorpsgek_irc import watcher


@watcher.register("registered")
async def registered(event, ws, irc):
    # Currently no action needed
    pass
