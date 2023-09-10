from aiogram import Router, types, F

from database.db import Database
from decorators import MessageLogging
from filters import IsAdmin
from keyboards.inline import get_back_button

command_statistics_router = Router()


@command_statistics_router.callback_query(F.data.in_({"statistics"}), IsAdmin())
@MessageLogging
async def command_statistics(call: types.CallbackQuery, request: Database):
    await call.answer()
    creator = "@medlcago"
    number_users = len(await request.get_all_users())
    number_blocked = len(await request.get_all_blocked())
    number_administrators = len(await request.get_admins())
    message = f"""📊 Общая статистика бота:
├ Создатель: {creator} 
├ Количество пользователей в боте: <b>{number_users}</b>
├ Количество заблокированных: <b>{number_blocked}</b> 
└ Количество администраторов в боте: <b>{number_administrators}</b>"""
    await call.message.edit_text(message, reply_markup=get_back_button(back="admin_panel").as_markup())
