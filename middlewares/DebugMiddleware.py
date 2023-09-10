from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from data.config import DEBUG
from data.templates import DEBUG_MESSAGE
from database.db import Database
from keyboards.inline import contact_admin_button


class DebugMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        request: Database = data["request"]

        if await self.is_allowed(user_id, request):
            return await handler(event, data)
        await self.handle_restriction(event)

    @staticmethod
    async def is_allowed(user_id: int, request: Database) -> bool:
        if not DEBUG:
            return True
        return await request.check_admin_permissions(user_id)

    @staticmethod
    async def handle_restriction(event: Union[Message, CallbackQuery]) -> None:
        if isinstance(event, CallbackQuery):
            await event.answer(DEBUG_MESSAGE)
            await event.message.answer(DEBUG_MESSAGE, reply_markup=contact_admin_button)
        else:
            await event.answer(DEBUG_MESSAGE, reply_markup=contact_admin_button)
