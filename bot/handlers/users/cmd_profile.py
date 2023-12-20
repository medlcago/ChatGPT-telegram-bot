from aiogram import Router, F, flags
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot.database.db import Database
from bot.decorators import MessageLogging
from bot.keyboards.inline_utils import create_inline_keyboard
from bot.language.translator import LocalizedTranslator
from keyboards.inline_main import close_button

command_profile_router = Router()


@command_profile_router.callback_query(F.data == "my_profile")
@command_profile_router.message(Command(commands="profile"))
@MessageLogging
@flags.rate_limit(rate=180, limit=3, key="profile")
async def command_profile(event: CallbackQuery | Message, request: Database, translator: LocalizedTranslator):
    user_id = event.from_user.id
    user = await request.get_user(user_id=user_id)

    is_subscriber = user.is_subscriber
    status = ("❌", "✅")[is_subscriber]
    referral_count = await request.get_user_referral_count(user_id)
    current_model = user.chat_type
    requests_limit = user.limit
    command_count = user.command_count

    message = translator.get("my-profile-message",
                             user_id=user_id,
                             status=status,
                             referral_count=referral_count,
                             current_model=current_model,
                             command_count=command_count,
                             requests_limit=requests_limit,
                             )

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(
            text=message,
            reply_markup=create_inline_keyboard(
                width=1,
                start="🔙 Назад"
            )
        )
        await event.answer("OK!")
    else:
        await event.answer(
            text=message,
            reply_markup=close_button
        )
