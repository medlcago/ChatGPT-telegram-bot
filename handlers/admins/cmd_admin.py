from aiogram import types, Router, F
from aiogram.filters.command import Command, CommandObject

from decorators import MessageLogging
from filters import IsAdmin, ChatTypeFilter
from keyboards.inline import btn_cmd_admin

command_admin_router = Router()


@command_admin_router.message(Command(commands=["admin"], prefix="/"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_admin(message: types.Message):
    await message.answer("Панель администратора", reply_markup=btn_cmd_admin)


@command_admin_router.message(Command(commands=["admin"], prefix="/"), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_admin(message: types.Message, command: CommandObject):
    await message.reply(f"Недостаточно прав для использования команды <b><i>{command.prefix + command.command}</i></b>")


@command_admin_router.callback_query(F.data.in_({"back_admin_panel"}), IsAdmin())
@MessageLogging
async def back_admin_panel(call: types.CallbackQuery):
    await call.answer("Панель администратора")
    await call.message.edit_text("Панель администратора", reply_markup=btn_cmd_admin)


@command_admin_router.callback_query(F.data.in_({"close_admin_panel"}), IsAdmin())
@MessageLogging
async def close_admin_panel(call: types.CallbackQuery):
    await call.answer("Панель успешно удалена")
    await call.message.delete()
