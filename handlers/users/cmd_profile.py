from aiogram import Router, types
from aiogram.filters.text import Text

from loader import db

command_profile_router = Router()


@command_profile_router.callback_query(Text(text="my_profile"))
async def command_profile(call: types.CallbackQuery):
    await call.answer()
    user_id = call.from_user.id
    is_subscriber = ("отсутствует", "присутствует")[await db.check_user_subscription(user_id)]
    current_model = await db.get_chat_type(user_id)
    message = f"""👤 Ваш профиль
├ ID: <code>{user_id}</code>
├ Подписка: <code>{is_subscriber}</code>
└ Текущая модель: <code>{current_model}</code>"""
    await call.message.answer(message)
