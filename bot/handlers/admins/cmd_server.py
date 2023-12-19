from aiogram import types, Router, F
from aiogram.filters.command import Command

from bot.decorators import MessageLogging
from bot.filters import IsAdmin, ChatTypeFilter
from bot.keyboards.inline_main import close_button
from bot.keyboards.inline_utils import create_inline_keyboard
from bot.utils.misc import get_server_system_info

command_server_router = Router()


@command_server_router.message(Command(commands="server"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_server(message: types.Message):
    result = get_server_system_info()
    await message.reply(
        text=result,
        reply_markup=close_button
    )


@command_server_router.callback_query(F.data == "server_info", IsAdmin())
@MessageLogging
async def command_server(call: types.CallbackQuery):
    result = get_server_system_info()
    await call.message.edit_text(
        text=result,
        reply_markup=create_inline_keyboard(
            width=1,
            admin_panel="Вернуться в админ панель",
            close="❌ Закрыть"
        )
    )
    await call.answer("OK!")
