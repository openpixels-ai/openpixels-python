import asyncio
import logging
import time
from typing import AsyncGenerator, Literal, TypedDict, Union

import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    connected_machine_id: str

    def __init__(self, api_key: str, base_url="https://worker.openpixels.ai"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Key {api_key}"},
            http2=True,
            timeout=5,
        )
        self.jobs = {}

    async def submit(self, input: dict) -> str:
        # Submit the payload and obtain a job id.
        start_time = time.time()
        submit_response = await self.client.post("/submit", json=input)
        self.connected_machine_id = submit_response.headers.get("machine-id")
        if not submit_response.is_success:
            raise ValueError(f"Failed to submit job: {submit_response.text}")
        submit_data = submit_response.json()
        job_id = submit_data.get("id")
        if not job_id:
            raise ValueError("No job id received from /submit")

        self.jobs[job_id] = {"start_time": start_time}
        return job_id

    async def subscribe(self, job_id: str) -> AsyncGenerator[dict, None]:
        # Poll the /poll endpoint until a non-empty response is received.
        while True:
            try:
                poll_response = await self.client.get(
                    f"/poll/{job_id}",
                    timeout=30,
                    headers={"fly-force-instance-id": self.connected_machine_id},
                )
            except httpx.TimeoutException:
                logger.info(f"Job {job_id} timed out; continuing to poll.")
                continue

            if not poll_response.is_success:
                yield {"type": "result", "error": poll_response.text, "meta": {}}
                break
            poll_data = poll_response.json()
            # If we get a non-empty response, assume processing is complete.
            if poll_data:
                logger.info(f"yielding poll data: {poll_data}")
                yield poll_data

                if poll_data["type"] == "result":
                    break

    async def run(self, payload: dict) -> dict:
        job_id = await self.submit(payload)
        print("machine id", self.connected_machine_id)
        async for result in self.subscribe(job_id):
            if result["type"] == "result":
                end_time = time.time()
                self.jobs[job_id]["end_time"] = end_time
                self.jobs[job_id]["duration"] = (
                    end_time - self.jobs[job_id]["start_time"]
                )
                # overhead = (
                #     self.jobs[job_id]["duration"] - result["meta"]["providerTime"]
                # )
                # logger.info(
                #     f"Job {job_id} completed in {self.jobs[job_id]['duration']} seconds (overhead: {overhead} seconds)"
                # )
                return {
                    "error": result.get("error"),
                    "data": result.get("data"),
                    # "meta": {**result.get("meta", {}), "overhead": overhead},
                }

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
