import os
import pytest
from openpixels import OpenPixels, AsyncOpenPixels

BASE_URL = os.environ.get("OPENPIXELS_BASE_URL", "http://localhost:1729")
API_KEY = os.environ.get("OPENPIXELS_API_KEY", "sk-test-has-credits")


@pytest.fixture
def client():
    c = OpenPixels(api_key=API_KEY, base_url=BASE_URL)
    yield c
    c.close()


@pytest.fixture
async def async_client():
    c = AsyncOpenPixels(api_key=API_KEY, base_url=BASE_URL)
    yield c
    await c.close()


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def api_key():
    return API_KEY
