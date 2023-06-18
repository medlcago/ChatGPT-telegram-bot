import pytz
from aiogram import types
from datetime import datetime, timedelta
from functools import wraps

from data import config
from loader import db


def check_time_limits(handler):
    @wraps(handler)
    async def wrapper(message: types.Message, *args, **kwargs):
        moscow_tz = pytz.timezone('Europe/Moscow')
        now = datetime.now(moscow_tz)
        user_id = message.from_user.id

        if user_id in (item.user_id for item in await db.get_admins()):
            return await handler(message, *args, **kwargs)

        date_format = '%Y-%m-%d %H:%M:%S'
        command_count = await db.get_gpt4_command_count(user_id)
        last_command_time = await db.get_last_gpt4_command_time(user_id)

        if last_command_time is not None:
            time_since_last_command = now - last_command_time

            if time_since_last_command < timedelta(seconds=30):
                await message.reply("Пожалуйста, подождите 30 секунд между запросами.")
                return

            if time_since_last_command > timedelta(hours=1):
                command_count = 0
                await db.reset_gpt4_command_count(user_id)

        if command_count < config.request_limit:
            await db.increment_gpt4_command_count(user_id)
            await db.update_last_gpt4_command_time(user_id, now.strftime(date_format))
            return await handler(message, *args, **kwargs)

        date_format = '%d.%m.%Y %H:%M:%S'
        await message.reply(
            f"Превышен часовой лимит запросов.\nПопробуйте снова <code>{(last_command_time + timedelta(hours=1)).strftime(date_format)}</code>"
            f"\n\nПодробнее /limits")
        return

    return wrapper
