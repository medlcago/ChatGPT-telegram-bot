from datetime import datetime, timedelta
from functools import wraps

import pytz
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from config import Config
from bot.database.db import Database


class CheckTimeLimits:
    def __init__(self, handler):
        self.handler = handler
        wraps(handler)(self)

    async def __call__(self, message: Message, *args, **kwargs):
        moscow_tz = pytz.timezone('Europe/Moscow')
        now = datetime.now(moscow_tz)
        user_id = message.from_user.id

        config: Config | None = kwargs.get("config", None)
        request: Database | None = kwargs.get("request", None)

        if config is None:
            raise ValueError("Config argument missing.")

        if request is None:
            raise ValueError("Request argument missing.")

        if await request.check_admin_permissions(user_id=user_id):
            return await self.handler(message, *args, **kwargs)

        date_format = '%Y-%m-%d %H:%M:%S'
        command_count = await request.get_user_command_count(user_id)
        last_command_time = await request.get_user_last_command_time(user_id)
        refresh_time = timedelta(hours=config.refresh_time)
        wait_time = timedelta(seconds=30)

        if last_command_time is not None:
            time_since_last_command = now - last_command_time

            if time_since_last_command < wait_time:
                seconds = (wait_time - time_since_last_command).seconds
                await message.reply(
                    f"⏳ Подождите еще {hbold(self._get_seconds_suffix(seconds))} перед тем, как отправить следующий запрос..")
                return

            if time_since_last_command > refresh_time:
                command_count = 0
                await request.reset_user_command_count(user_id)

        request_limit = await request.get_user_limit(user_id=user_id)
        if command_count < request_limit:
            await request.increment_user_command_count(user_id)
            await request.update_user_last_command_time(user_id, now.strftime(date_format))
            return await self.handler(message, *args, **kwargs)

        elapsed_time = datetime.now(moscow_tz) - last_command_time
        remaining_time = (refresh_time - elapsed_time)
        minutes = remaining_time // timedelta(minutes=1)

        await message.reply(
            f"Превышен лимит запросов за последние {hbold('12 часов.')}\nПопробуйте снова через {hbold(self._get_minutes_suffix(minutes))}"
            f"\n\nПодробнее /limits")
        return

    @staticmethod
    def _get_minutes_suffix(minutes: int) -> str:
        if minutes == 1:
            return f"{minutes} минуту"
        elif minutes % 100 in (11, 12, 13, 14):
            return f"{minutes} минут"
        elif minutes % 10 in (2, 3, 4):
            return f"{minutes} минуты"
        else:
            return f"{minutes} минут"

    @staticmethod
    def _get_seconds_suffix(seconds: int) -> str:
        if seconds % 10 == 1 and seconds % 100 != 11:
            return f"{seconds} секунду"
        elif seconds % 100 not in (12, 13, 14) and seconds % 10 in (2, 3, 4):
            return f"{seconds} секунды"
        return f"{seconds} секунд"
