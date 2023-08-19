from aiogram import Router, types
from aiogram import html
from aiogram.filters.command import Command

from data.templates import START_MESSAGE
from database.db import Database
from decorators import MessageLogging
from filters import ChatTypeFilter
from keyboards.inline import btn_my_profile

command_start_help_router = Router()


async def cmd_start_help(username, language="ru"):
    message = START_MESSAGE.get(language, START_MESSAGE["en"])
    return message.format(username=username)


@command_start_help_router.message(Command(commands=["start", "help"], prefix="/"), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_start_help(message: types.Message, request: Database):
    if await request.user_exists(message.from_user.id) is None:
        await request.add_user(message.from_user.id, message.from_user.full_name)
    await message.answer(
        await cmd_start_help(username=html.quote(message.from_user.full_name),
                             language=message.from_user.language_code))
    await message.answer(f"Текущая модель: {await request.get_user_chat_type(message.from_user.id)}\n"
                         f"Отправьте сообщение, чтобы начать диалог\n\n"
                         f"/switch - Сменить модель\n"
                         f"/models - Список доступных моделей", reply_markup=btn_my_profile)
