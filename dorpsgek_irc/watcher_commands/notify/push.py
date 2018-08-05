from dorpsgek_irc import watcher


@watcher.register("notify.push")
async def push(event, ws, irc):
    # Our userdata are the channels we like to join, without '#'
    channels = event.data["userdata"]
    if not isinstance(channels, list):
        channels = [channels]
    channels = [f"#{c}" for c in channels]

    autojoins = irc.get_plugin("irc3.plugins.autojoins.AutoJoins")

    commit_count = len(event.data["commits"])

    for channel in channels:
        # Try to join the channel before we send a message
        if channel not in autojoins.joined:
            autojoins.join(channel)

        irc.privmsg(channel,
                    f"[{event.data['repository_name']}] "
                    f"{event.data['user']} pushed {commit_count} commits to {event.data['branch']}:"
        )
        for commit in event.data["commits"]:
            irc.privmsg(channel, f"  - {commit['message']} (by {commit['author']})")
        irc.privmsg(channel, event.data["url"])
