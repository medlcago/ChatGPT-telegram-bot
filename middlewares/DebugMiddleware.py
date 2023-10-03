from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message, CallbackQuery

from data.config import DEBUG
from database.db import Database
from keyboards.inline_main import contact_admin_button
from language.translator import LocalizedTranslator


class DebugMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        request: Database = data["request"]
        translator: LocalizedTranslator = data["translator"]
        skip = get_flag(data, "skip")

        if skip or await self.is_allowed(user_id, request):
            return await handler(event, data)
        await self.handle_restriction(event, translator)

    @staticmethod
    async def is_allowed(user_id: int, request: Database) -> bool:
        if not DEBUG:
            return True
        return await request.check_admin_permissions(user_id)

    @staticmethod
    async def handle_restriction(event: Union[Message, CallbackQuery], translator: LocalizedTranslator) -> None:
        if isinstance(event, CallbackQuery):
            await event.answer(translator.get("debug-message"))
            await event.message.answer(translator.get("debug-message"), reply_markup=contact_admin_button)
        else:
            await event.answer(translator.get("debug-message"), reply_markup=contact_admin_button)
