from aiogram import Router, types, Bot, flags, F
from aiogram import html
from aiogram.filters.command import Command, CommandObject

from data.templates import START_MESSAGE
from database.db import Database
from decorators import MessageLogging
from filters import ChatTypeFilter
from keyboards.inline import my_profile_and_affiliate_program_buttons, ComeBack
from utils.misc import payload_decode

command_start_help_router = Router()


async def cmd_start_help(username, language="ru"):
    message = START_MESSAGE.get(language, START_MESSAGE["en"])
    return message.format(username=username)


@command_start_help_router.message(Command(commands=["start", "help"]), ChatTypeFilter(is_group=False))
@MessageLogging
@flags.rate_limit(rate=120, limit=1, key="start")
async def command_start_help(message: types.Message, command: CommandObject, request: Database, bot: Bot):
    referrer_id = payload_decode(payload=command.args)
    user_id = message.from_user.id
    fullname = message.from_user.full_name
    current_model = await request.get_user_chat_type(user_id=user_id)

    if await request.get_user(user_id=user_id) is None:
        if referrer_id and referrer_id.isdigit() and user_id != int(referrer_id) and await request.get_user(
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
                         f"/clear - Очистить историю диалога\n"
                         f"/switch - Сменить модель\n"
                         f"/models - Список доступных моделей", reply_markup=my_profile_and_affiliate_program_buttons)


@command_start_help_router.callback_query(ComeBack.filter(F.back == "start"))
async def command_back_start(call: types.CallbackQuery, request: Database):
    await call.answer()
    user_id = call.from_user.id
    current_model = await request.get_user_chat_type(user_id=user_id)
    await call.message.edit_text(f"Текущая модель: {current_model}\n"
                                 f"Отправьте сообщение, чтобы начать диалог\n\n"
                                 f"/clear - Очистить историю диалога\n"
                                 f"/switch - Сменить модель\n"
                                 f"/models - Список доступных моделей",
                                 reply_markup=my_profile_and_affiliate_program_buttons)
