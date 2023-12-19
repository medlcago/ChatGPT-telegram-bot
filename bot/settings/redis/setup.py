from aiogram.fsm.storage.redis import Redis


async def create_redis_session(url: str):
    redis_session = Redis.from_url(url=url)
    return redis_session
