import asyncio
from typing import List

import pytest
from httpx import AsyncClient, Response


@pytest.mark.asyncio
async def test_work_handler(client: AsyncClient, client2: AsyncClient) -> None:
    history: List[Response] = await asyncio.gather(
        *[client.get("/test") for _ in range(2)],
        *[client2.get("/test") for _ in range(2)]
    )
    history.sort(key=lambda x: x.json()["elapsed"], reverse=True)
    for i in range(len(history) - 1):
        current_longest = history[i].json()["elapsed"]
        previous = history[i + 1].json()["elapsed"]
        assert current_longest - previous >= 3
