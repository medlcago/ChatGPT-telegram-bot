from aiogram import types, Router, F
from aiogram.filters.command import Command

from bot.decorators import MessageLogging
from bot.filters import IsAdmin, ChatTypeFilter
from bot.keyboards.inline_main import admin_panel_buttons

command_admin_router = Router()


@command_admin_router.message(Command(commands="admin"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_admin(message: types.Message):
    await message.answer("Панель администратора", reply_markup=admin_panel_buttons)


@command_admin_router.message(Command(commands="admin"), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_admin(message: types.Message):
    await message.reply("Nice try, bro! 🤣")


@command_admin_router.callback_query(F.data == "admin_panel", IsAdmin())
@MessageLogging
async def back_admin_panel(call: types.CallbackQuery):
    await call.answer("Панель администратора")
    await call.message.edit_text("Панель администратора", reply_markup=admin_panel_buttons)
