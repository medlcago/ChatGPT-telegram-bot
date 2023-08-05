from aiogram import types, Router

from aiogram.filters.command import Command, CommandObject
from aiogram.filters.text import Text

from decorators import MessageLogging
from filters import IsAdmin
from keyboards.inline import btn_cmd_admin

command_admin_router = Router()


@command_admin_router.message(Command(commands=["admin"], prefix="/"), IsAdmin())
@MessageLogging
async def command_admin(message: types.Message):
    await message.answer("Панель администратора", reply_markup=btn_cmd_admin)


@command_admin_router.message(Command(commands=["admin"], prefix="/"))
@MessageLogging
async def command_admin(message: types.Message, command: CommandObject):
    await message.reply(f"Недостаточно прав для использования команды <b><i>{command.prefix + command.command}</i></b>")


@command_admin_router.callback_query(Text(text="close_admin_panel"), IsAdmin())
@MessageLogging
async def close_admin_panel(call: types.CallbackQuery):
    await call.answer("Панель успешно удалена")
    await call.message.delete()
