"""Redis client — sessions, rate limiting, webhook queue."""

from redis import Redis, ConnectionError

from app.core.config import settings

redis_client: Redis | None = None


def init_redis() -> Redis:
    global redis_client
    redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        redis_client.ping()
    except ConnectionError:
        redis_client = None
    return redis_client


def get_redis() -> Redis | None:
    return redis_client
