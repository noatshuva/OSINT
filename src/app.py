import time
from fastapi import FastAPI, Path
from pydantic import BaseModel
import aiohttp
import aioredis
import asyncio
from hashlib import sha256
import json
import uvicorn

API_URLS = {
    "ip-api": "http://ip-api.com/json/",
}
SUCCESS_CODE = 200

app = FastAPI()

r = aioredis.from_url(f"redis://localhost:6379", decode_responses=True)


class IPResponse(BaseModel):
    raw_data: dict
    metrics: dict


async def fetch_data(session, ip, name, url):
    cache_key = sha256(f"{url}{ip}".encode('utf-8')).hexdigest()
    cached = await r.exists(cache_key)

    if cached:
        cached_response = await r.get(cache_key)
        return name, json.loads(cached_response), {'success': 'true', 'time': 0}
    else:
        start_time = time.time()
        async with session.get(url + ip) as response:
            if response.status == SUCCESS_CODE:
                response_data = await response.json()
                success = 'true'
                await r.setex(cache_key, 3600, json.dumps(response_data))
            else:
                response_data = {}
                success = 'false'
            elapsed_time = time.time() - start_time
    return name, response_data, {'success': success, 'time': elapsed_time}


@app.get("/{ip_addresses}", response_model=IPResponse)
async def post_request(ip_addresses: str = Path(..., title="The IP addresses, comma-separated")):
    ips = ip_addresses.split(',')
    async with aiohttp.ClientSession() as session:
        tasks = []
        for ip in ips:
            for name, url in API_URLS.items():
                task = asyncio.create_task(fetch_data(session, ip, name, url))
                tasks.append(task)
        results = await asyncio.gather(*tasks)
        raw_data = {}
        metrics = {}
        for result in results:
            name, data, metric = result
            if name not in raw_data:
                raw_data[name] = []
                metrics[name] = []
            raw_data[name].append(data)
            metrics[name].append(metric)
    return {
        "raw_data": raw_data,
        "metrics": metrics
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
