from typing import Callable, Any, Awaitable, Dict
from typing import Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


class RedisMiddleware(BaseMiddleware):
    def __init__(self, redis_session):
        self.redis_session = redis_session

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]) -> Any:
        data['redis'] = self.redis_session
        return await handler(event, data)
