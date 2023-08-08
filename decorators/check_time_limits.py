from datetime import datetime, timedelta
from functools import wraps

import pytz
from aiogram import types

from data import config
from loader import db


class CheckTimeLimits:
    def __init__(self, handler):
        self.handler = handler
        wraps(handler)(self)

    async def __call__(self, message: types.Message, *args, **kwargs):
        moscow_tz = pytz.timezone('Europe/Moscow')
        now = datetime.now(moscow_tz)
        user_id = message.from_user.id

        if await db.check_admin_permissions(user_id=user_id):
            return await self.handler(message, *args, **kwargs)

        date_format = '%Y-%m-%d %H:%M:%S'
        command_count = await db.get_command_count(user_id)
        last_command_time = await db.get_last_command_time(user_id)

        if last_command_time is not None:
            time_since_last_command = now - last_command_time

            if time_since_last_command < timedelta(seconds=30):
                await message.reply("Пожалуйста, подождите 30 секунд между запросами.")
                return

            if time_since_last_command > timedelta(hours=1):
                command_count = 0
                await db.reset_command_count(user_id)

        if command_count < config.request_limit:
            await db.increment_command_count(user_id)
            await db.update_last_command_time(user_id, now.strftime(date_format))
            return await self.handler(message, *args, **kwargs)

        date_format = '%d.%m.%Y %H:%M:%S'
        await message.reply(
            f"Превышен часовой лимит запросов.\nПопробуйте снова <code>{(last_command_time + timedelta(hours=1)).strftime(date_format)}</code>"
            f"\n\nПодробнее /limits")
        return