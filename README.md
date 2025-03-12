# OpenPixels Python SDK

A Python SDK for accessing the OpenPixels API.

## Installation

```bash
pip install openpixels
# or with uv
uv pip install openpixels
```

## Usage

```python
from openpixels import OpenPixels

client = OpenPixels(
    api_key="sk-op-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
)

# Generate an image
def generate_image():
    result = client.run(
        model="flux-dev",
        prompt="a cat"
    )
    
    print(result)

generate_image()
```

The SDK provides both synchronous and asynchronous clients. The asynchronous client is preferable for most applications, especially those handling multiple requests or running in async environments like FastAPI.

### Async Client Usage

```python
from openpixels import AsyncOpenPixels
import asyncio

client = AsyncOpenPixels(
	api_key="sk-op-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
)

async def generate_image_async():
    result = await client.run(
        model="flux-dev",
        prompt="a cat"
    )
    
    print(result)

# Run the async function
asyncio.run(generate_image_async())
```

## API Reference

### `OpenPixels`

The synchronous client for making calls to the OpenPixels API.

```python
client = OpenPixels(
    api_key="YOUR_API_KEY",
    base_url="https://worker.openpixels.ai"  # Optional, defaults to production API
)
```

### `AsyncOpenPixels`

The asynchronous client for making calls to the OpenPixels API. This is generally preferred for better performance and responsiveness.

```python
client = AsyncOpenPixels(
    api_key="YOUR_API_KEY",
    base_url="https://worker.openpixels.ai"  # Optional, defaults to production API
)
```

#### Methods

Both clients provide the following methods:

- `run(payload)`: Submits a job and waits for the result.

<!-- - `submit(payload)`: Submits a job and returns the job ID.
- `subscribe(job_id)`: Subscribes to updates for a job. -->

## Development

### Building the Package

This project uses [uv](https://github.com/astral-sh/uv) for package management and building:

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Build the package
uv build
```

### Deploying a New Version

1. Update the version in `pyproject.toml`
2. Remove the dists folder: `rm -rf dist`
3. Build the distribution packages:
   ```bash
   uv build
   ```
4. Upload to PyPI using twine:
   ```bash
   python3 -m twine upload dist/*
   ```
5. `git tag vX.Y.Z`
6. `git push origin vX.Y.Z`

## License

MIT
