from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from data.config import SUBSCRIBERS_ONLY
from data.templates import SUBSCRIBERS_ONLY_MESSAGE
from database.db import Database
from keyboards.inline import btn_contact_admin


class SubscribersMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        request: Database = data["request"]
        if (not SUBSCRIBERS_ONLY or
                await request.check_user_subscription(user_id=user_id) or await request.check_admin_permissions(user_id=user_id)):
            return await handler(event, data)

        if isinstance(event, CallbackQuery):
            await event.answer(SUBSCRIBERS_ONLY_MESSAGE)
            await event.message.answer(SUBSCRIBERS_ONLY_MESSAGE, reply_markup=btn_contact_admin)
        else:
            await event.answer(SUBSCRIBERS_ONLY_MESSAGE, reply_markup=btn_contact_admin)
