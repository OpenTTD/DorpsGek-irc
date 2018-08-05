from dorpsgek_irc import watcher


@watcher.register("notify.issue")
async def issue(event, ws, irc):
    # Our userdata are the channels we like to join, without '#'
    channels = event.data["userdata"]
    if not isinstance(channels, list):
        channels = [channels]
    channels = [f"#{c}" for c in channels]

    autojoins = irc.get_plugin("irc3.plugins.autojoins.AutoJoins")

    if event.data["action"] == "opened":
        message = f"{event.data['user']} opened issue #{event.data['issue_id']}: {event.data['title']}"
    elif event.data["action"] == "closed":
        message = f"{event.data['user']} closed issue #{event.data['issue_id']}: {event.data['title']}"
    elif event.data["action"] == "comment":
        message = f"{event.data['user']} commented on issue #{event.data['issue_id']}: {event.data['title']}"

    for channel in channels:
        # Try to join the channel before we send a message
        if channel not in autojoins.joined:
            autojoins.join(channel)

        irc.privmsg(channel, f"[{event.data['repository_name']}] {message} {event.data['url']}")
