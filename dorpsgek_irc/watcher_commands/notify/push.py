from dorpsgek_irc import watcher


@watcher.register("notify.push")
async def push(event, ws, irc):
    # Our userdata are the channels we like to join, without '#'
    channels = event.data["userdata"]
    if not isinstance(channels, list):
        channels = [channels]
    channels = ["#%s" % c for c in channels]

    autojoins = irc.get_plugin("irc3.plugins.autojoins.AutoJoins")

    for channel in channels:
        # Try to join the channel before we send a message
        if channel not in autojoins.joined:
            autojoins.join(channel)

        irc.privmsg(channel, "[%s] Push to %s by %s:" % (
            event.data["repository_name"],
            event.data["branch"],
            event.data["pusher"],
        ))
        for commit in event.data["commits"]:
            irc.privmsg(channel, "  - %s (by %s)" % (commit["message"], commit["author"]))
        irc.privmsg(channel, event.data["url"])
