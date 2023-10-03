from aiogram import Router, types, F
from aiogram.filters.command import Command

from database.db import Database
from decorators import MessageLogging
from filters import IsAdmin, ChatTypeFilter
from keyboards.inline_main import get_back_button
from utils.misc import get_user_list

command_user_list_router = Router()


@command_user_list_router.message(Command(commands=["user_list"]), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_user_list(message: types.Message, request: Database):
    result = await get_user_list(request=request)
    await message.reply(result)


@command_user_list_router.callback_query(F.data.in_({"user_list"}), IsAdmin())
@MessageLogging
async def command_user_list(call: types.CallbackQuery, request: Database):
    result = await get_user_list(request=request)
    await call.message.edit_text(result, reply_markup=get_back_button(back="admin_panel").as_markup())
    await call.answer("OK!")
