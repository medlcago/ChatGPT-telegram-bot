from typing import Union

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from database.db import Database


class IsAdmin(Filter):
    async def __call__(self, event: Union[Message, CallbackQuery], request: Database) -> bool:
        return await request.check_admin_permissions(user_id=event.from_user.id)
