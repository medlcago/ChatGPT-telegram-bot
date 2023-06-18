from aiogram import types, Router
from aiogram.filters.command import Command

from decorators import message_logging
from filters import IsAdmin
from keyboards.inline import btn_cmd_admin

command_admin_router = Router()


@command_admin_router.message(Command(commands=["admin"], prefix="/"), IsAdmin())
@message_logging
async def command_admin(message: types.Message):
    await message.answer("Панель администратора", reply_markup=btn_cmd_admin)
