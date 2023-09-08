from aiogram import Router, types, F, flags
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hcode

from database.db import Database
from decorators import MessageLogging
from keyboards.inline import btn_promocode_activation, get_keyboard_back

command_profile_router = Router()


@command_profile_router.callback_query(F.data.in_({"my_profile"}))
@MessageLogging
@flags.rate_limit(rate=180, limit=3, key="profile")
async def command_profile(call: types.CallbackQuery, request: Database):
    await call.answer()
    user_id = call.from_user.id

    user = await request.get_user(user_id=user_id)

    is_subscriber = user.is_subscriber
    status = ("отсутствует", "присутствует")[is_subscriber]
    referral_count = await request.get_user_referral_count(user_id)
    current_model = user.chat_type
    message = f"""👤 Ваш профиль
├ ID: {hcode(user_id)}
├ Подписка: {hcode(status)}
├ Кол-во рефералов: {hcode(referral_count)}
└ Текущая модель: {hcode(current_model)}"""
    builder = get_keyboard_back(back="start")
    if is_subscriber:
        await call.message.edit_text(message, reply_markup=builder.as_markup())
    else:
        await call.message.edit_text(message,
                                     reply_markup=builder.attach(InlineKeyboardBuilder.from_markup(
                                         btn_promocode_activation)).as_markup())
