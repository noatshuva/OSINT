import aiohttp
import asyncio


async def fetch(session, url, request_number):
    async with session.get(url) as response:
        response_text = await response.text()
        print(f"Response {request_number}: {response_text}")


async def main():
    url = "http://127.0.0.1:8000/8.8.8.8,24.48.0.1,8.8.4.4"
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, i + 1) for i in
                 range(30)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
