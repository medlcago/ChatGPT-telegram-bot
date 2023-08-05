from aiogram import Router, types
from aiogram import html
from aiogram.filters.command import Command

from data.templates import START_MESSAGE
from decorators import MessageLogging
from filters import ChatTypeFilter
from keyboards.inline import btn_my_profile
from loader import db

command_start_help_router = Router()


def cmd_start_help(username, language="ru"):
    message = START_MESSAGE.get(language, START_MESSAGE["en"])
    return message.format(username=username)


@command_start_help_router.message(Command(commands=["start", "help"], prefix="/"), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_start_help(message: types.Message):
    if not (await db.user_exists(message.from_user.id)):
        await db.add_user(message.from_user.id, message.from_user.full_name)
    await message.answer(
        cmd_start_help(username=html.quote(message.from_user.full_name), language=message.from_user.language_code))
    await message.answer(f"Текущая модель: {html.quote(await db.get_chat_type(message.from_user.id))}\n"
                         f"Отправьте сообщение, чтобы начать диалог\n\n"
                         f"/switch - Сменить модель", reply_markup=btn_my_profile)
