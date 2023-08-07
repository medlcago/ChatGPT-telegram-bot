from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.filters.text import Text

from decorators import MessageLogging
from filters import IsAdmin, ChatTypeFilter
from keyboards.inline import btn_back_admin_panel
from loader import db

command_user_list_router = Router()


async def user_list():
    users = await db.get_all_users()
    if users:
        data = (f"{user.fullname}({user.user_id})" for user in users)
        return '<b>Пользователи бота:</b>\n' + "\n".join(data)
    else:
        return "Пользователи отсутствуют."


@command_user_list_router.message(Command(commands=["user_list"], prefix="/"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_user_list(message: types.Message):
    result = await user_list()
    await message.edit_text(result, reply_markup=btn_back_admin_panel)


@command_user_list_router.callback_query(Text(text="user_list"), IsAdmin())
@MessageLogging
async def command_user_list(call: types.CallbackQuery):
    result = await user_list()
    await call.message.edit_text(result, reply_markup=btn_back_admin_panel)
    await call.answer("Успех!")
