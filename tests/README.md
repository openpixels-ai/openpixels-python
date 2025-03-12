# OpenPixels SDK Tests

This directory contains tests for the OpenPixels Python SDK.

## Running the Tests

### Setting up Environment Variables

You can set environment variables in two ways:

1. Using a `.env` file:
   - Copy the `.env.example` file in the project root to `.env`
   - Edit the `.env` file and set your API key and other configuration options
   - The tests will automatically load variables from this file

2. Setting environment variables directly:
   ```bash
   # Required for API tests
   export OPENPIXELS_API_KEY="your-api-key"

   # Optional configuration
   export OPENPIXELS_BASE_URL="https://worker.openpixels.ai"  # Default API URL
   ```

### Running the Test Suite

To install development dependencies:

```bash
uv pip install -e ".[dev]"
```

Then run the tests with pytest:

```bash
# From the py-sdk directory
pytest

# Run with verbose output
pytest -v

# Run a specific test
pytest tests/test_client.py::test_image_generation
```

## Running as a Script

You can also run the test file directly as a script:

```bash
# Make sure you've set up the environment variables or .env file
python -m tests.test_client
```

This will execute a single test that generates an image using the API. 