from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from data.config import DEBUG
from data.templates import DEBUG_MESSAGE
from loader import db


class DebugMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        if not DEBUG or await db.check_admin_permissions(user_id=user_id):
            return await handler(event, data)

        if isinstance(event, CallbackQuery):
            await event.answer(DEBUG_MESSAGE)
            await event.message.answer(DEBUG_MESSAGE)
        else:
            await event.answer(DEBUG_MESSAGE)
