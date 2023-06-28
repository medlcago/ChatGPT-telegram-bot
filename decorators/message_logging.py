import datetime
import logging
from functools import wraps

from aiogram import types


class MessageLogging:
    def __init__(self, func):
        self.func = func
        wraps(func)(self)

    async def __call__(self, event, **kwargs):
        logging.info(f"Function {self.func.__name__} called")

        full_name = event.from_user.full_name
        user_id = event.from_user.id
        username = event.from_user.username
        text, chat_id = self._extract_text_and_chat_id(event)

        time_format = '%d-%m-%Y %H:%M:%S'
        timezone_offset = datetime.timedelta(hours=3)
        current_time = datetime.datetime.now(datetime.timezone(timezone_offset)).strftime(time_format)

        log_message = (
            f"{full_name}[{user_id}({username})] --- {text} [{current_time}] [chat_id = {chat_id}]"
        )
        print(log_message)

        return await self.func(event, **kwargs)

    @staticmethod
    def _extract_text_and_chat_id(event):
        if isinstance(event, types.Message):
            text = event.text if event.text else 'not supported'
            chat_id = event.chat.id
        else:
            text = event.data
            chat_id = event.message.chat.id
        return text, chat_id
