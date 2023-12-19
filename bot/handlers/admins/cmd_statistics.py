from aiogram import Router, types, F

from bot.database.db import Database
from bot.decorators import MessageLogging
from bot.filters import IsAdmin
from bot.keyboards.inline_utils import create_inline_keyboard

command_statistics_router = Router()


@command_statistics_router.callback_query(F.data == "statistics", IsAdmin())
@MessageLogging
async def command_statistics(call: types.CallbackQuery, request: Database):
    creator = "@medlcago"
    number_users = len(await request.get_all_users())
    number_blocked = len(await request.get_all_blocked())
    number_administrators = len(await request.get_admins())
    message_text = f"""📊 Общая статистика бота:
├ Создатель: {creator} 
├ Пользователей в боте: <b>{number_users}</b>
├ Заблокировано: <b>{number_blocked}</b> 
└ Администраторов в боте: <b>{number_administrators}</b>"""
    await call.message.edit_text(
        text=message_text,
        reply_markup=create_inline_keyboard(
            width=1,
            admin_panel="Вернуться в админ панель",
            close="❌ Закрыть"
        )
    )
    await call.answer("OK!")
