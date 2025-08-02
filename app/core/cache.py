from redis.asyncio import Redis
from app.core.config import settings

redis: Optional[Redis] = None

async def get_redis() -> Redis:
    return redis

async def init_redis() -> None:
    global redis
    redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        decode_responses=True
    )
