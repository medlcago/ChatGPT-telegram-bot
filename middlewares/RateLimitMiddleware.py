from typing import Callable, Any, Awaitable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.fsm.storage.redis import Redis
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold


class RateLimitMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]) -> Any:
        rate_limit = get_flag(data, "rate_limit")
        if rate_limit is None:
            return await handler(event, data)

        redis: Redis = data.get("redis")
        rate = rate_limit.get("rate", 120)
        limit = rate_limit.get("limit", 1)
        key = rate_limit.get("key", "key")
        user = f"User_{event.from_user.id}_{key}"

        if await redis.get(name=user) is not None:
            if int(await redis.get(name=user)) < limit:
                await redis.incr(name=user)
                return await handler(event, data)

            self.seconds = await redis.ttl(name=user)
            await self.handle_restriction(event=event)
            return
        await redis.set(name=user, value=1, ex=rate, nx=True)
        return await handler(event, data)

    async def handle_restriction(self, event: Union[Message, CallbackQuery]) -> None:
        if isinstance(event, CallbackQuery):
            await event.answer(f"Повторите попытку через {self._get_seconds_suffix(self.seconds)}")
        else:
            await event.answer(
                f"⏳ Подождите еще {hbold(self._get_seconds_suffix(self.seconds))} перед тем, как отправить следующий запрос..")

    @staticmethod
    def _get_seconds_suffix(seconds: int) -> str:
        if seconds % 10 == 1 and seconds % 100 != 11:
            return f"{seconds} секунду"
        elif seconds % 100 not in (12, 13, 14) and seconds % 10 in (2, 3, 4):
            return f"{seconds} секунды"
        return f"{seconds} секунд"
