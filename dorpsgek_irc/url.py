import aiohttp


async def shorten(url):
    """
    Generate a git.io shortened url from a github.com url.
    If the request errors, it just returns the original.
    """
    data = aiohttp.FormData()
    data.add_field("url", url)
    async with aiohttp.ClientSession() as session:
        async with session.post("https://git.io", data=data) as resp:
            if resp.status != 201 or "Location" not in resp.headers:
                return url
            return resp.headers["Location"]
