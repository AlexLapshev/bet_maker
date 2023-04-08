import asyncio
import decimal
import random

import httpx


async def async_range(count):
    for i in range(count):
        yield i
        await asyncio.sleep(0.0)


async def main():
    async with httpx.AsyncClient() as client:
        async for i in async_range(10000):
            await client.put(
                url="http://0.0.0.0:8000/event",
                json={
                    "event_id": random.randint(1, 3),
                    "status": random.randint(1, 3),
                    "coefficient": float(
                        decimal.Decimal(
                            f"{random.randint(1, 6)}.{random.randint(11, 99)}"
                        )
                    ),
                    "deadline": 0,
                },
                headers={"accept": "*/*", "Content-Type": "application/json"},
            )


l = asyncio.get_event_loop()
l.run_until_complete(main())
