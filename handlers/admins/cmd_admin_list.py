from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.filters.text import Text

from decorators import message_logging
from filters import IsAdmin
from loader import db

command_admin_list_router = Router()


async def admin_list():
    admins = await db.get_admins()
    if admins:
        data = (f"{admin.fullname}({admin.user_id})" for admin in admins)
        return '<b>Администраторы бота:</b>\n' + "\n".join(data)
    else:
        return "Администраторы отсутствуют."


@command_admin_list_router.message(Command(commands=["admin_list"], prefix="/"), IsAdmin())
@message_logging
async def command_admin_list(message: types.Message):
    result = await admin_list()
    await message.reply(result)


@command_admin_list_router.callback_query(Text(text="admin_list"), IsAdmin())
@message_logging
async def command_admin_list(call: types.CallbackQuery):
    result = await admin_list()
    await call.message.reply(result)
    await call.answer()
