import asyncio

import httpx


class OpenPixelsClient:
    def __init__(self, api_key: str, base_url="https://worker.openpixels.ai"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=self.base_url, headers={"Authorization": f"Key {api_key}"}
        )

    async def submit(self, payload: dict) -> dict:
        # Submit the payload and obtain a job id.
        submit_response = await self.client.post("/submit", json=payload)
        submit_response.raise_for_status()
        submit_data = submit_response.json()
        job_id = submit_data.get("id")
        if not job_id:
            raise ValueError("No job id received from /submit")

        # Poll the /poll endpoint until a non-empty response is received.
        while True:
            poll_response = await self.client.get(f"/poll/{job_id}")
            poll_response.raise_for_status()
            poll_data = poll_response.json()
            # If we get a non-empty response, assume processing is complete.
            if poll_data:
                return poll_data
            await asyncio.sleep(1)

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
