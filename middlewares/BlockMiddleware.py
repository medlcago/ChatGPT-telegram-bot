from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from keyboards.inline import btn_contact_admin
from loader import db


class BlockMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        if not await db.check_user_blocked(user_id=user_id):
            return await handler(event, data)

        message = "<b>Access is denied.\nMost likely, you have been banned for violating the rules of the bot.</b>"
        if isinstance(event, CallbackQuery):
            await event.answer("Access is denied.")
            await event.message.answer(message, reply_markup=btn_contact_admin)
        else:
            await event.answer(message, reply_markup=btn_contact_admin)
