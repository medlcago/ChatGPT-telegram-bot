from aiogram import Router, F, flags
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.db import Database
from decorators import MessageLogging
from keyboards.inline_main import promocode_activation_button, get_back_button
from language.translator import LocalizedTranslator

command_profile_router = Router()


@command_profile_router.callback_query(F.data == "my_profile")
@MessageLogging
@flags.rate_limit(rate=180, limit=3, key="profile")
async def command_profile(call: CallbackQuery, request: Database, translator: LocalizedTranslator):
    await call.answer()
    user_id = call.from_user.id

    user = await request.get_user(user_id=user_id)

    is_subscriber = user.is_subscriber
    status = ("❌", "✅")[is_subscriber]
    referral_count = await request.get_user_referral_count(user_id)
    current_model = user.chat_type
    message = translator.get("my-profile-message", user_id=user_id, status=status, referral_count=referral_count,
                             current_model=current_model)

    builder = get_back_button(back="start")
    if is_subscriber:
        await call.message.edit_text(text=message, reply_markup=builder.as_markup())
    else:
        await call.message.edit_text(
            text=message,
            reply_markup=builder.attach(InlineKeyboardBuilder.from_markup(promocode_activation_button)).as_markup()
        )
