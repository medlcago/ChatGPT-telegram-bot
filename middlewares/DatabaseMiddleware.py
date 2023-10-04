from typing import Callable, Any, Awaitable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated

from database.db import Database


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool):
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery, ChatMemberUpdated],
            data: Dict[str, Any]) -> Any:
        async with self.session_pool() as session:
            data['session'] = session
            data['request'] = Database(session=session)
            result = await handler(event, data)
        return result
