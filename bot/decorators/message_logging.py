import logging
from functools import wraps
from typing import Union

from aiogram.types import Message, CallbackQuery


class MessageLogging:
    def __init__(self, func):
        self.func = func
        wraps(func)(self)

    async def __call__(self, event: Union[Message, CallbackQuery], *args, **kwargs):
        func_name = self.func.__name__
        logger = logging.getLogger(func_name)

        full_name = event.from_user.full_name
        user_id = event.from_user.id
        username = event.from_user.username
        text, chat_id = self._extract_text_and_chat_id(event)

        logger.info(f"{full_name}[{user_id}({username})] --- {text} [chat_id = {chat_id}]")

        return await self.func(event, *args, **kwargs)

    @staticmethod
    def _extract_text_and_chat_id(event):
        if isinstance(event, Message):
            text = event.text if event.text else 'not supported'
            chat_id = event.chat.id
        else:
            text = event.data
            chat_id = event.message.chat.id
        return text, chat_id
