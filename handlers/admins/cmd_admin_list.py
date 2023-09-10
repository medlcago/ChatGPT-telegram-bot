from aiogram import Router, types, F
from aiogram.filters.command import Command

from database.db import Database
from decorators import MessageLogging
from filters import IsAdmin, ChatTypeFilter
from keyboards.inline import get_back_button

command_admin_list_router = Router()


async def admin_list(*, request: Database):
    admins = await request.get_admins()
    if admins:
        data = (f"{admin.fullname}({admin.user_id})" for admin in admins)
        return '<b>Администраторы бота:</b>\n' + "\n".join(data)
    return "Администраторы отсутствуют."


@command_admin_list_router.message(Command(commands=["admin_list"]), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_admin_list(message: types.Message, request: Database):
    result = await admin_list(request=request)
    await message.reply(result)


@command_admin_list_router.callback_query(F.data.in_({"admin_list"}), IsAdmin())
@MessageLogging
async def command_admin_list(call: types.CallbackQuery, request: Database):
    result = await admin_list(request=request)
    await call.message.edit_text(result, reply_markup=get_back_button(back="admin_panel").as_markup())
    await call.answer("Успех!")
