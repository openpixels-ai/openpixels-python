import logging
from typing import AsyncGenerator, Generator

import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://worker.openpixels.ai"


class AsyncOpenPixels:
    connected_machine_id: str

    def __init__(self, api_key: str, base_url=BASE_URL):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Key {api_key}"},
            http2=True,
            timeout=5,
        )
        # self.jobs = {}

    async def submit(self, input: dict) -> str:
        submit_response = await self.client.post("/submit", json=input)
        if not submit_response.is_success:
            raise ValueError(f"Failed to submit job: {submit_response.text}")

        self.connected_machine_id = submit_response.headers.get("machine-id")
        submit_data = submit_response.json()
        job_id = submit_data.get("id")
        if not job_id:
            raise ValueError("No job id received from /submit")

        return job_id

    async def subscribe(self, job_id: str) -> AsyncGenerator[dict, None]:
        while True:
            try:
                poll_response = await self.client.get(
                    f"/poll/{job_id}",
                    timeout=30,
                    headers={"fly-force-instance-id": self.connected_machine_id},
                )
            except httpx.TimeoutException:
                continue

            if not poll_response.is_success:
                # this is wrong...? you don't return an {error: ... if there was a connection error, because it might be fine.}
                # yield {"type": "result", "error": poll_response.text, "meta": {}}
                # perhaps should throw here.
                break

            poll_data = poll_response.json()
            yield poll_data
            # here we're exposing exactly what we receive from the worker, so the worker's responses are a final API.
            # honestly, that seems right; the client should be a thin wrapper around the worker, and avoid modifying the responses much.

            if poll_data["type"] == "result":
                break

    async def run(self, payload: dict) -> dict:
        job_id = await self.submit(payload)
        async for result in self.subscribe(job_id):
            if result["type"] == "result":
                return {
                    **({"error": result.get("error")} if result.get("error") else {}),
                    **({"data": result.get("data")} if result.get("data") else {}),
                    "status": result.get("status"),
                }

    async def close(self):
        await self.client.aclose()


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


class OpenPixels:
    connected_machine_id: str

    def __init__(self, api_key: str, base_url=BASE_URL):
        self.base_url = base_url
        self.client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Key {api_key}"},
            http2=True,
            timeout=5,
        )
        # self.jobs = {}

    def submit(self, input: dict) -> str:
        submit_response = self.client.post("/submit", json=input)
        if not submit_response.is_success:
            raise ValueError(f"Failed to submit job: {submit_response.text}")

        self.connected_machine_id = submit_response.headers.get("machine-id")
        submit_data = submit_response.json()
        job_id = submit_data.get("id")
        if not job_id:
            raise ValueError("No job id received from /submit")

        return job_id

    def subscribe(self, job_id: str) -> Generator[dict, None, None]:
        while True:
            try:
                poll_response = self.client.get(
                    f"/poll/{job_id}",
                    timeout=30,
                    headers={"fly-force-instance-id": self.connected_machine_id},
                )
            except httpx.TimeoutException:
                continue

            if not poll_response.is_success:
                # this is wrong...? you don't return an {error: ... if there was a connection error, because it might be fine.}
                # yield {"type": "result", "error": poll_response.text, "meta": {}}
                # perhaps should throw here.
                break

            poll_data = poll_response.json()
            yield poll_data
            # here we're exposing exactly what we receive from the worker, so the worker's responses are a final API.
            # honestly, that seems right; the client should be a thin wrapper around the worker, and avoid modifying the responses much.

            if poll_data["type"] == "result":
                break

    def run(self, payload: dict) -> dict:
        job_id = self.submit(payload)
        for result in self.subscribe(job_id):
            if result["type"] == "result":
                return {
                    **({"error": result.get("error")} if result.get("error") else {}),
                    **({"data": result.get("data")} if result.get("data") else {}),
                    "status": result.get("status"),
                }

    def close(self):
        self.client.close()


__all__ = ["OpenPixels", "AsyncOpenPixels"]
