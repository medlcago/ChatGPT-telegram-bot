from typing import Union

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from database.db import Database


class IsSubscription(Filter):
    async def __call__(self, event: Union[Message, CallbackQuery], request: Database) -> bool:
        return await request.check_user_subscription(event.from_user.id)
