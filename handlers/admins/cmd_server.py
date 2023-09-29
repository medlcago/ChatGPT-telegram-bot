from aiogram import types, Router, F
from aiogram.filters.command import Command

from decorators import MessageLogging
from filters import IsAdmin, ChatTypeFilter
from keyboards.inline import get_back_button
from utils.misc import get_server_system_info

command_server_router = Router()


@command_server_router.message(Command(commands=["server"]), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_server(message: types.Message):
    result = get_server_system_info()
    await message.reply(result)


@command_server_router.callback_query(F.data.in_({"server_info"}), IsAdmin())
@MessageLogging
async def command_server(call: types.CallbackQuery):
    result = get_server_system_info()
    await call.message.edit_text(result, reply_markup=get_back_button(back="admin_panel").as_markup())
    await call.answer("Успех!")
