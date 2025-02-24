import asyncio
from typing import AsyncGenerator, Literal, TypedDict, Union

import httpx


class FluxDev(TypedDict):
    model: Literal["flux-dev"]
    count: int | None
    prompt: str
    negative_prompt: str | None
    seed: int | None


class FluxSchnell(TypedDict):
    model: Literal["flux-schnell"]
    count: int | None
    prompt: str
    negative_prompt: str | None
    seed: int | None


Params = Union[FluxDev, FluxSchnell]


class AsyncOpenPixels:
    def __init__(self, api_key: str, base_url="https://worker.openpixels.ai"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Key {api_key}"},
            http2=True,
        )

    async def submit(self, input: dict) -> str:
        # Submit the payload and obtain a job id.
        submit_response = await self.client.post("/submit", json=input)
        submit_response.raise_for_status()
        submit_data = submit_response.json()
        job_id = submit_data.get("id")
        if not job_id:
            raise ValueError("No job id received from /submit")
        return job_id

    async def subscribe(self, job_id: str) -> AsyncGenerator[dict, None]:
        # Poll the /poll endpoint until a non-empty response is received.
        while True:
            poll_response = await self.client.get(f"/poll/{job_id}")
            poll_response.raise_for_status()
            poll_data = poll_response.json()
            # If we get a non-empty response, assume processing is complete.
            if poll_data:
                yield poll_data

                if poll_data["type"] == "result":
                    break

    async def run(self, payload: dict) -> dict:
        job_id = await self.submit(payload)
        async for result in self.subscribe(job_id):
            if result["type"] == "result":
                return result["data"]

    async def close(self):
        await self.client.aclose()


class OpenPixels:
    pass


# Example usage:
# async def main():
#     client = OpenPixelsClient()
#     try:
#         result = await client.submit({"some": "data"})
#         print("Result:", result)
#     finally:
#         await client.close()
#
# asyncio.run(main())
