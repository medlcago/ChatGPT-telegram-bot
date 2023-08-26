from typing import Callable, Any, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import Redis
from aiogram.types import Message


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 60):
        self.limit = limit

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]) -> Any:
        redis: Redis = data.get("redis")
        user = f"User{event.from_user.id}"

        if await redis.get(name=user):
            seconds = await redis.ttl(name=user)
            await event.answer(f"Повторите попытку через {self._get_seconds_suffix(seconds)}")
            return
        await redis.set(name=user, value=1, ex=self.limit, nx=True)
        return await handler(event, data)

    @staticmethod
    def _get_seconds_suffix(seconds: int) -> str:
        if seconds % 10 == 1 and seconds % 100 != 11:
            return f"{seconds} секунду"
        elif seconds % 100 not in (12, 13, 14) and seconds % 10 in (2, 3, 4):
            return f"{seconds} секунды"
        return f"{seconds} секунд"
