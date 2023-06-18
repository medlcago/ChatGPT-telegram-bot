from aiogram import types
from aiogram.filters import Filter

from loader import db


class IsAdmin(Filter):
    async def __call__(self, message: types.Message | types.CallbackQuery) -> bool:
        return message.from_user.id in (item.user_id for item in await db.get_admins())
