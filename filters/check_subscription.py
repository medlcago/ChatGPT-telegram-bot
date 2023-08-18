from aiogram import types
from aiogram.filters import Filter

from database.db import Database


class IsSubscription(Filter):
    async def __call__(self, event: types.Message | types.CallbackQuery, request: Database) -> bool:
        return await request.check_user_subscription(event.from_user.id)
