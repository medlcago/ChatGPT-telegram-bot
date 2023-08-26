from typing import Callable, Any, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.fsm.storage.redis import Redis
from aiogram.types import Message
from aiogram.utils.markdown import hbold


class RateLimitMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]) -> Any:
        rate_limit = get_flag(data, "rate_limit")
        if rate_limit is None:
            return await handler(event, data)

        redis: Redis = data.get("redis")
        limit = rate_limit.get("limit", 120)
        key = rate_limit.get("key", "key")
        user = f"User_{event.from_user.id}_{key}"

        if await redis.get(name=user):
            seconds = await redis.ttl(name=user)
            await event.answer(
                f"⏳ Подождите еще {hbold(self._get_seconds_suffix(seconds))} перед тем, как отправить следующий запрос..")
            return
        await redis.set(name=user, value=1, ex=limit, nx=True)
        return await handler(event, data)

    @staticmethod
    def _get_seconds_suffix(seconds: int) -> str:
        if seconds % 10 == 1 and seconds % 100 != 11:
            return f"{seconds} секунду"
        elif seconds % 100 not in (12, 13, 14) and seconds % 10 in (2, 3, 4):
            return f"{seconds} секунды"
        return f"{seconds} секунд"
