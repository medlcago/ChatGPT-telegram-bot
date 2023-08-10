from aiogram import Router, types
from aiogram.filters.text import Text

from decorators import MessageLogging
from keyboards.inline import btn_promocode_activation
from loader import db

command_profile_router = Router()


@command_profile_router.callback_query(Text(text="my_profile"))
@MessageLogging
async def command_profile(call: types.CallbackQuery):
    await call.answer()
    user_id = call.from_user.id
    is_subscriber = await db.check_user_subscription(user_id)
    status = ("отсутствует", "присутствует")[is_subscriber]
    current_model = await db.get_chat_type(user_id)
    message = f"""👤 Ваш профиль
├ ID: <code>{user_id}</code>
├ Подписка: <code>{status}</code>
└ Текущая модель: <code>{current_model}</code>"""
    if is_subscriber:
        await call.message.answer(message)
    else:
        await call.message.answer(message, reply_markup=btn_promocode_activation)
