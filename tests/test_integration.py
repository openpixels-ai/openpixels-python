import os
import pytest
import httpx
from openpixels import OpenPixels, AsyncOpenPixels

BASE_URL = os.environ.get("OPENPIXELS_BASE_URL", "http://localhost:1729")
API_KEY = os.environ.get("OPENPIXELS_API_KEY", "sk-test-has-credits")


class TestSyncClient:
    def test_health_check(self, base_url):
        """Worker is reachable."""
        response = httpx.get(f"{base_url}/status")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "ok"

    def test_image_generation(self, client):
        """Generate an image with flux-schnell sync client."""
        result = client.run({
            "model": "flux-schnell",
            "prompt": "a red circle on white background",
            "width": 512,
            "height": 512,
        })
        assert result is not None
        assert "error" not in result or result.get("error") is None

    def test_auth_error_missing_key(self, base_url):
        """Missing API key returns error."""
        response = httpx.post(
            f"{base_url}/v2/submit",
            json={
                "model": "flux-schnell",
                "prompt": "test",
                "width": 512,
                "height": 512,
            },
        )
        assert response.status_code == 401

    def test_auth_error_invalid_key(self, base_url):
        """Invalid API key returns error."""
        bad_client = OpenPixels(api_key="sk-test-invalid-key", base_url=base_url)
        with pytest.raises(ValueError, match="Failed to submit"):
            bad_client.run({
                "model": "flux-schnell",
                "prompt": "test",
                "width": 512,
                "height": 512,
            })
        bad_client.close()


class TestAsyncClient:
    @pytest.mark.asyncio
    async def test_image_generation(self, async_client):
        """Generate an image with flux-schnell async client."""
        result = await async_client.run({
            "model": "flux-schnell",
            "prompt": "a blue square on white background",
            "width": 512,
            "height": 512,
        })
        assert result is not None
        assert "error" not in result or result.get("error") is None
