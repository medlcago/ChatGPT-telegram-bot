from aiogram import Router, types
from aiogram.filters.text import Text

from decorators import MessageLogging
from filters import IsAdmin
from loader import db

command_statistics_router = Router()


@command_statistics_router.callback_query(Text(text="statistics"), IsAdmin())
@MessageLogging
async def command_statistics(call: types.CallbackQuery):
    await call.answer()
    creator = "@medlcago"
    number_users = len(await db.get_all_users())
    number_blocked = len(await db.get_all_blocked())
    number_administrators = len(await db.get_admins())
    message = f"""📊 Общая статистика бота:
├ Создатель: {creator} 
├ Количество пользователей в боте: <b>{number_users}</b>
├ Количество заблокированных: <b>{number_blocked}</b> 
└ Количество администраторов в боте: <b>{number_administrators}</b>"""
    await call.message.reply(message)
