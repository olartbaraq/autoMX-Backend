import aiohttp
import asyncio
from decouple import config


async def get_unsplash_image(query: str) -> dict:
    client_id = config("ACCESS_KEY")

    url = f"https://api.unsplash.com/search/photos/?client_id={client_id}?query={query}"
    async with aiohttp.ClientSession() as session:
        res = await session.get(url=url)
        return res.json()
