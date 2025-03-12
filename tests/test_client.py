import asyncio
import os
from pathlib import Path
from unittest import mock

from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path)

import pytest
from openpixels.client import AsyncOpenPixels


@pytest.fixture
def api_key():
    # Get API key from environment variable or use a mock for testing
    return os.environ.get("OPENPIXELS_API_KEY", "mock-api-key")


@pytest.fixture
def client(api_key):
    return AsyncOpenPixels(
        api_key=api_key,
        base_url=os.environ.get("OPENPIXELS_BASE_URL", "https://worker.openpixels.ai"),
    )


@pytest.mark.asyncio
async def test_image_generation(client):
    """Test generating an image with the default model."""

    result = await client.run(
        {
            "model": "flux-dev",
            "prompt": "a cat",
            "width": 512,
            "height": 512,
        }
    )

    assert result is not None
    if not isinstance(result, dict):
        result = result.dict()
    assert "url" in result


# Simple script-like usage example that mimics the original test.py
if __name__ == "__main__":

    async def main():
        # Get API key from environment variable
        api_key = os.environ.get("OPENPIXELS_API_KEY")
        if not api_key:
            print("Error: OPENPIXELS_API_KEY environment variable is not set")
            return

        client = AsyncOpenPixels(
            api_key=api_key,
            base_url=os.environ.get(
                "OPENPIXELS_BASE_URL", "https://worker.openpixels.ai"
            ),
        )

        model = os.environ.get("OPENPIXELS_MODEL", "flux-dev")

        print("Running test with model:", model)
        result = await client.run(
            {
                "model": model,
                "prompt": "a cat",
                "width": 512,
                "height": 512,
            }
        )
        print(result)

    asyncio.run(main())
