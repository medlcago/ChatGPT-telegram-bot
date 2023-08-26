from datetime import timedelta

from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.utils.markdown import hitalic, hbold

from data.config import Config
from database.db import Database
from decorators import MessageLogging
from filters import ChatTypeFilter

command_limits_router = Router()


@command_limits_router.message(Command(commands=["limits"]), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_limits(message: types.Message, request: Database, config: Config):
    date_format = '%d.%m.%Y %H:%M:%S'
    last_command_time = await request.get_user_last_command_time(message.from_user.id)
    full_name = message.from_user.full_name
    current_model = await request.get_user_chat_type(user_id=message.from_user.id)
    request_limit = config.models.request_limit
    command_count = await request.get_user_command_count(user_id=message.from_user.id)
    data_update_time = (last_command_time + timedelta(hours=1)).strftime(date_format) if last_command_time else ""

    message_reply = (f"{full_name}!\n\n"
                     f"Текущая модель: {current_model}\n\n"
                     f"Лимит запросов в час: {hitalic(request_limit)}\n"
                     f"Сделано запросов: {hitalic(command_count)}\n\n" +
                     (f"Данные обновятся {hbold(data_update_time)} (UTC+3)" if data_update_time else ""))
    await message.reply(message_reply)
