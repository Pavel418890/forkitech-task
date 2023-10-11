import asyncio
import logging
import os
from time import monotonic

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from redis.asyncio import ConnectionPool, Redis
from redis.asyncio.lock import Lock

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG) if os.getenv("DEBUG") else False

router = APIRouter()

app = FastAPI(description="FastAPI Server Port %s" % os.getenv("BACKEND_PORT"))
redis_url = "redis://{}:{}"
redis_pool = ConnectionPool.from_url(
    redis_url.format(
        os.getenv("REDIS_HOST") or "localhost",
        int(os.getenv("REDIS_PORT") or 6379),
    )
)


async def work() -> None:
    await asyncio.sleep(3)


class TestResponse(BaseModel):
    elapsed: float


@router.get("/test", response_model=TestResponse)
async def handler() -> TestResponse:
    logger.debug("%s\t::\thandle request" % app.description)
    ts1 = monotonic()
    redis_client = await Redis.from_pool(redis_pool)
    async with Lock(redis_client, name="worker") as lock:
        while True:
            if not await lock.owned():
                logger.debug("we are no longer lock owner, falling back")
                continue

            await work()
            ts2 = monotonic()

            await redis_client.aclose()

            logger.debug("%s\t::\tdone\t::\t%d" % (app.description, (ts2-ts1)))
            return TestResponse(elapsed=ts2 - ts1)


app.include_router(router)
