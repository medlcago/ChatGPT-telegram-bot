from datetime import timedelta

from aiogram import Router, types, flags
from aiogram.filters.command import Command
from aiogram.utils.markdown import hitalic, hbold

from config import Config
from bot.database.db import Database
from bot.decorators import MessageLogging
from bot.filters import ChatTypeFilter
from bot.keyboards.inline_main import close_button

command_limits_router = Router()


@command_limits_router.message(Command(commands=["limits"]), ChatTypeFilter(is_group=False))
@MessageLogging
@flags.rate_limit(rate=180, limit=2, key="limits")
async def command_limits(message: types.Message, request: Database, config: Config):
    user = await request.get_user(user_id=message.from_user.id)

    date_format = '%d %b %Y %H:%M:%S'
    last_command_time = await request.get_user_last_command_time(user_id=message.from_user.id)
    full_name = message.from_user.full_name
    current_model = user.chat_type
    command_count = user.command_count
    requests_limit = user.limit
    requests_left = requests_limit - command_count
    refresh_time = config.refresh_time
    data_update_time = (last_command_time + timedelta(hours=refresh_time)).strftime(
        date_format) if last_command_time else ""

    message_reply = (f"{full_name}!\n\n"
                     f"Текущая модель: {current_model}\n\n"
                     f"Лимит запросов: {hitalic(requests_limit)}\n"
                     f"Осталось запросов: {hitalic(requests_left)}\n\n" +
                     (f"Данные будут сброшены {hbold(data_update_time)} (UTC+3)" if data_update_time else ""))

    await message.reply(
        text=message_reply,
        reply_markup=close_button
    )
