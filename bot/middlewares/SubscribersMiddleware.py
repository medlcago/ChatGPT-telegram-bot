from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message, CallbackQuery

from config import SUBSCRIBERS_ONLY
from bot.database.db import Database
from bot.keyboards.inline_utils import create_inline_keyboard
from bot.language.translator import LocalizedTranslator


class SubscribersMiddleware(BaseMiddleware):
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
        if not SUBSCRIBERS_ONLY:
            return True
        return await request.check_user_subscription_status(user_id) or await request.check_admin_permissions(user_id)

    @staticmethod
    async def handle_restriction(event: Union[Message, CallbackQuery], translator: LocalizedTranslator) -> None:
        keyboard = create_inline_keyboard(
            width=1,
            activate_promocode="✅ Активировать промокод",
            close="❌ Закрыть"
        )

        if isinstance(event, CallbackQuery):
            await event.answer("Access limited due to lack of subscription.")
            await event.message.answer(translator.get("subscribers-only-message"), reply_markup=keyboard)
        else:
            await event.answer(translator.get("subscribers-only-message"), reply_markup=keyboard)
