from dorpsgek_irc import (
    watcher,
    url,
)


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
    elif event.data["action"] == "dismissed":
        message = f"{event.data['user']} dismissed a review for pull request #{event.data['pull_id']}:" \
                  f" {event.data['title']}"
    elif event.data["action"] == "approved":
        message = f"{event.data['user']} approved pull request #{event.data['pull_id']}: {event.data['title']}"
    elif event.data["action"] == "changes_requested":
        message = f"{event.data['user']} requested changes for pull request #{event.data['pull_id']}:" \
                  f" {event.data['title']}"
    elif event.data["action"] == "commented":
        message = f"{event.data['user']} commented on pull request #{event.data['pull_id']}: {event.data['title']}"
    else:
        return

    for channel in channels:
        # Try to join the channel before we send a message
        if channel not in autojoins.joined:
            autojoins.join(channel)

        shortened_url = await url.shorten(event.data["url"])
        irc.privmsg(channel, f"[{event.data['repository_name']}] {message} {shortened_url}")
