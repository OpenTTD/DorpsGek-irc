from dorpsgek_irc import watcher


@watcher.register("notify.pull_request")
async def pull_request(event, ws, irc):
    # Our userdata are the channels we like to join, without '#'
    channels = event.data["userdata"]
    if not isinstance(channels, list):
        channels = [channels]
    channels = [f"#{c}" for c in channels]

    autojoins = irc.get_plugin("irc3.plugins.autojoins.AutoJoins")

    if event.data["action"] == "opened":
        message = f"{event.data['user']} opened pull request #{event.data['pull_id']}: {event.data['title']}"
    elif event.data["action"] == "closed":
        message = f"{event.data['user']} closed pull request #{event.data['pull_id']}: {event.data['title']}"
    elif event.data["action"] == "merged":
        message = f"{event.data['user']} merged pull request #{event.data['pull_id']}: {event.data['title']}"
    elif event.data["action"] == "synchronize":
        message = f"{event.data['user']} updated pull request #{event.data['pull_id']}: {event.data['title']}"
    elif event.data["action"] == "reopened":
        message = f"{event.data['user']} reopened pull request #{event.data['pull_id']}: {event.data['title']}"
    elif event.data["action"] == "comment":
        message = f"{event.data['user']} commented on pull request #{event.data['pull_id']}: {event.data['title']}"

    for channel in channels:
        # Try to join the channel before we send a message
        if channel not in autojoins.joined:
            autojoins.join(channel)

        irc.privmsg(channel, f"[{event.data['repository_name']}] {message} {event.data['url']}")
