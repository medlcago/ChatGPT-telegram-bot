from aiogram import Router, types, Bot, flags
from aiogram import html
from aiogram.filters.command import Command, CommandObject

from data.templates import START_MESSAGE
from database.db import Database
from decorators import MessageLogging
from filters import ChatTypeFilter
from keyboards.inline import btn_my_profile
from utils.misc import payload_decode

command_start_help_router = Router()


async def cmd_start_help(username, language="ru"):
    message = START_MESSAGE.get(language, START_MESSAGE["en"])
    return message.format(username=username)


@command_start_help_router.message(Command(commands=["start", "help"]), ChatTypeFilter(is_group=False))
@MessageLogging
@flags.rate_limit(limit=120, key="start")
async def command_start_help(message: types.Message, command: CommandObject, request: Database, bot: Bot):
    referrer_id = payload_decode(payload=command.args)
    user_id = message.from_user.id
    fullname = message.from_user.full_name
    current_model = await request.get_user_chat_type(user_id=user_id)

    if await request.user_exists(user_id=user_id) is None:
        if referrer_id and referrer_id.isdigit() and user_id != int(referrer_id) and await request.user_exists(
                user_id=referrer_id):
            await request.add_user(user_id=user_id, fullname=fullname, referrer=referrer_id)
            await bot.send_message(chat_id=referrer_id, text=f"<b>Новый реферал — <code>{user_id}</code>!</b>")
        else:
            await request.add_user(user_id=user_id, fullname=fullname)

    await message.answer(
        await cmd_start_help(username=html.quote(message.from_user.full_name),
                             language=message.from_user.language_code))
    await message.answer(f"Текущая модель: {current_model}\n"
                         f"Отправьте сообщение, чтобы начать диалог\n\n"
                         f"/ref - Реферальная ссылка\n"
                         f"/switch - Сменить модель\n"
                         f"/models - Список доступных моделей", reply_markup=btn_my_profile)
