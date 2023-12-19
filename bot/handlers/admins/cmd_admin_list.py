from aiogram import Router, types, F
from aiogram.filters.command import Command

from bot.database.db import Database
from bot.decorators import MessageLogging
from bot.filters import IsAdmin, ChatTypeFilter
from bot.keyboards.inline_main import close_button
from bot.keyboards.inline_utils import create_inline_keyboard
from bot.utils.misc import get_admin_list

command_admin_list_router = Router()


@command_admin_list_router.message(Command(commands="admin_list"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_admin_list(message: types.Message, request: Database):
    result = await get_admin_list(request=request)
    await message.reply(
        text=result,
        reply_markup=close_button
    )


@command_admin_list_router.callback_query(F.data == "admin_list", IsAdmin())
@MessageLogging
async def command_admin_list(call: types.CallbackQuery, request: Database):
    result = await get_admin_list(request=request)
    await call.message.edit_text(
        text=result,
        reply_markup=
        create_inline_keyboard(
            width=1,
            admin_panel="Вернуться в админ панель",
            close="❌ Закрыть"
        )
    )
    await call.answer("OK!")
