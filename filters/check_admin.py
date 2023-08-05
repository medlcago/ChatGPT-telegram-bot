from aiogram import types
from aiogram.filters import Filter

from loader import db


class IsAdmin(Filter):
    async def __call__(self, event: types.Message | types.CallbackQuery) -> bool | None:
        return await db.check_admin_permissions(user_id=event.from_user.id)
