import logging
from typing import AsyncGenerator, Generator

import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://worker.openpixels.ai"


class AsyncOpenPixels:
    def __init__(self, api_key: str, base_url=BASE_URL):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Key {api_key}"},
            http2=True,
            timeout=5,
        )

    async def _submit(self, input: dict) -> str:
        submit_response = await self.client.post("/v2/submit", json=input)
        if not submit_response.is_success:
            raise ValueError(f"Failed to submit job: {submit_response.text}")

        return submit_response.json()

    async def _subscribe(self, job_id: str) -> AsyncGenerator[dict, None]:
        while True:
            try:
                poll_response = await self.client.get(
                    f"/v2/poll/{job_id}",
                    timeout=30,
                )
            except httpx.TimeoutException:
                continue

            if not poll_response.is_success:
                # this is wrong...? you don't return an {error: ... if there was a connection error, because it might be fine.}
                # yield {"type": "result", "error": poll_response.text, "meta": {}}
                # perhaps should throw here.
                raise ValueError(f"Failed to poll job: {poll_response.text}")

            poll_data = poll_response.json()
            yield poll_data
            # here we're exposing exactly what we receive from the worker, so the worker's responses are a final API.
            # honestly, that seems right; the client should be a thin wrapper around the worker, and avoid modifying the responses much.

            if poll_data["type"] == "result":
                break

    async def run(self, payload: dict) -> dict:
        result = await self._submit(payload)
        if result["type"] == "result":
            return _clean_result(result)

        async for result in self._subscribe(result["id"]):
            if result["type"] == "result":
                return _clean_result(result)

    async def close(self):
        await self.client.aclose()


class OpenPixels:
    def __init__(self, api_key: str, base_url=BASE_URL):
        self.base_url = base_url
        self.client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Key {api_key}"},
            http2=True,
            timeout=5,
        )

    def _submit(self, input: dict) -> str:
        submit_response = self.client.post("/v2/submit", json=input)
        if not submit_response.is_success:
            raise ValueError(f"Failed to submit job: {submit_response.text}")

        return submit_response.json()

    def _subscribe(self, job_id: str) -> Generator[dict, None, None]:
        while True:
            try:
                poll_response = self.client.get(
                    f"/v2/poll/{job_id}",
                    timeout=30,
                )
            except httpx.TimeoutException:
                continue

            if not poll_response.is_success:
                # this is wrong...? you don't return an {error: ... if there was a connection error, because it might be fine.}
                # yield {"type": "result", "error": poll_response.text, "meta": {}}
                # perhaps should throw here.
                raise ValueError(f"Failed to poll job: {poll_response.text}")

            poll_data = poll_response.json()
            yield poll_data
            # here we're exposing exactly what we receive from the worker, so the worker's responses are a final API.
            # honestly, that seems right; the client should be a thin wrapper around the worker, and avoid modifying the responses much.

            if poll_data["type"] == "result":
                break

    def run(self, payload: dict) -> dict:
        result = self._submit(payload)
        if result["type"] == "result":
            return _clean_result(result)

        for result in self._subscribe(result["id"]):
            if result["type"] == "result":
                return _clean_result(result)

    def close(self):
        self.client.close()


__all__ = ["OpenPixels", "AsyncOpenPixels"]


def _clean_result(result: dict) -> dict:
    if result["type"] == "result":
        return {
            **({"id": result.get("id")} if result.get("id") else {}),
            **({"error": result.get("error")} if result.get("error") else {}),
            **({"data": result.get("data")} if result.get("data") else {}),
            "status": result.get("status"),
        }
