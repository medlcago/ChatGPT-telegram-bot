from aiogram import Router, types, F
from aiogram.filters.command import Command

from database.db import Database
from decorators import MessageLogging
from filters import IsAdmin, ChatTypeFilter
from keyboards.inline import get_back_button
from utils.misc import get_admin_list

command_admin_list_router = Router()


@command_admin_list_router.message(Command(commands=["admin_list"]), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_admin_list(message: types.Message, request: Database):
    result = await get_admin_list(request=request)
    await message.reply(result)


@command_admin_list_router.callback_query(F.data.in_({"admin_list"}), IsAdmin())
@MessageLogging
async def command_admin_list(call: types.CallbackQuery, request: Database):
    result = await get_admin_list(request=request)
    await call.message.edit_text(result, reply_markup=get_back_button(back="admin_panel").as_markup())
    await call.answer("OK!")
