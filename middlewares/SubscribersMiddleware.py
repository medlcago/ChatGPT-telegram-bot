from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message, CallbackQuery

from data.config import SUBSCRIBERS_ONLY
from data.templates import SUBSCRIBERS_ONLY_MESSAGE
from database.db import Database
from keyboards.inline import get_activate_subscription_button


class SubscribersMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        request: Database = data["request"]
        skip = get_flag(data, "skip")

        if skip or await self.is_allowed(user_id, request):
            return await handler(event, data)
        await self.handle_restriction(event)

    @staticmethod
    async def is_allowed(user_id: int, request: Database) -> bool:
        if not SUBSCRIBERS_ONLY:
            return True
        return await request.check_user_subscription(user_id) or await request.check_admin_permissions(user_id)

    @staticmethod
    async def handle_restriction(event: Union[Message, CallbackQuery]) -> None:
        markup = get_activate_subscription_button().as_markup()
        if isinstance(event, CallbackQuery):
            await event.answer(SUBSCRIBERS_ONLY_MESSAGE)
            await event.message.answer(SUBSCRIBERS_ONLY_MESSAGE, reply_markup=markup)
        else:
            await event.answer(SUBSCRIBERS_ONLY_MESSAGE, reply_markup=markup)
