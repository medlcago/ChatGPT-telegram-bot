from datetime import timedelta

from aiogram import Router, types
from aiogram.filters.command import Command

from data import config
from decorators import MessageLogging
from filters import ChatTypeFilter
from loader import db

command_limits_router = Router()


@command_limits_router.message(Command(commands=["limits"], prefix="/"), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_limits(message: types.Message):
    date_format = '%d.%m.%Y %H:%M:%S'
    last_command_time = await db.get_last_command_time(message.from_user.id)
    message_reply = (f"{message.from_user.full_name}!\n\n"
                     f"Текущая модель: {await db.get_chat_type(message.from_user.id)}\n\n"
                     f"Твой лимит запросов в час: <i>{config.request_limit}</i>\n"
                     f"Сделано запросов: <i>{await db.get_command_count(message.from_user.id)}</i>\n" +
                     ((
                          f"\nДанные обновятся <b>{(last_command_time + timedelta(hours=1)).strftime(date_format)}</b>") if last_command_time else ""))
    await message.reply(message_reply)
