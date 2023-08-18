from aiogram import types
from aiogram.filters import Filter

from database.db import Database


class IsAdmin(Filter):
    async def __call__(self, event: types.Message | types.CallbackQuery, request: Database) -> bool:
        return await request.check_admin_permissions(user_id=event.from_user.id)
