from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from data.templates import BLOCKED_MESSAGE
from database.db import Database
from keyboards.inline import btn_contact_admin


class BlockMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        request: Database = data["request"]
        if not await request.check_user_blocked(user_id=user_id):
            return await handler(event, data)

        if isinstance(event, CallbackQuery):
            await event.answer("Access is denied.")
            await event.message.answer(hbold(BLOCKED_MESSAGE), reply_markup=btn_contact_admin)
        else:
            await event.answer(hbold(BLOCKED_MESSAGE), reply_markup=btn_contact_admin)
