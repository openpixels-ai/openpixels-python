import asyncio

from openpixels.client import AsyncOpenPixels

client = AsyncOpenPixels(
    # api_key="sk-op-43477e1622dd9ea82b364e1339cfba1da2c59c099f2cbdf4409b3cec59d353ee",
    # base_url="https://worker.openpixels.ai",
    api_key="sk-op-00bb01f7633d1db1ce2f76b2a4a369b5d73f7f949e69dcd889c2fc29b566352e",
    base_url="http://localhost:1729",
)


async def test():
    print(
        await client.run(
            {
                "model": "blackforestlabs/flux-dev",
                "prompt": "a cat",
                "count": 1,
                "width": 512,
                "height": 512,
            }
        )
    )
    return
    print(
        await client.run(
            {
                "model": "blackforestlabs/flux-dev",
                "prompt": "a dog",
                "count": 1,
                "width": 512,
                "height": 512,
            }
        )
    )
    print(
        await client.run(
            {
                "model": "blackforestlabs/flux-dev",
                "prompt": "a frog",
                "count": 1,
                "width": 512,
                "height": 512,
            }
        )
    )


asyncio.run(test())
