from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient

from main import app


@pytest_asyncio.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as c:
        yield c

@pytest_asyncio.fixture
async def client2() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://localhost:8001") as c2:
        yield c2
