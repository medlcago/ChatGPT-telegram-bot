from aiogram import types
from aiogram.filters import Filter

from loader import db


class IsSubscription(Filter):
    async def __call__(self, event: types.Message | types.CallbackQuery) -> bool:
        return await db.check_user_subscription(event.from_user.id)
