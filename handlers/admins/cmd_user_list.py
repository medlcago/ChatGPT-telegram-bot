from aiogram import Router, types, F
from aiogram.filters.command import Command

from database.db import Database
from decorators import MessageLogging
from filters import IsAdmin, ChatTypeFilter
from keyboards.inline import btn_back_admin_panel

command_user_list_router = Router()


async def user_list(*, request: Database):
    users = await request.get_all_users()
    if users:
        data = (f"{user.fullname}({user.user_id})" for user in users)
        return '<b>Пользователи бота:</b>\n' + "\n".join(data)
    return "Пользователи отсутствуют."


@command_user_list_router.message(Command(commands=["user_list"], prefix="/"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_user_list(message: types.Message, request: Database):
    result = await user_list(request=request)
    await message.reply(result)


@command_user_list_router.callback_query(F.data.in_({"user_list"}), IsAdmin())
@MessageLogging
async def command_user_list(call: types.CallbackQuery, request: Database):
    result = await user_list(request=request)
    await call.message.edit_text(result, reply_markup=btn_back_admin_panel)
    await call.answer("Успех!")
