from aiogram import Router, types, Bot, F, flags
from aiogram.utils.deep_linking import create_start_link

from bot.database.db import Database
from bot.decorators import MessageLogging
from bot.keyboards.inline_utils import create_inline_keyboard

command_affiliate_program_router = Router()


@command_affiliate_program_router.callback_query(F.data == "affiliate_program")
@MessageLogging
@flags.rate_limit(rate=180, limit=3, key="affiliate_program")
async def callback_affiliate_program(call: types.CallbackQuery, bot: Bot, request: Database):
    await call.answer()
    user_id = call.from_user.id

    start_link = await create_start_link(bot=bot, payload=str(user_id), encode=True)
    referral_count = await request.get_user_referral_count(user_id)
    message = f"""<b>📊 Статистика:
├ Вы пригласили: {referral_count}

⤵️ Ваши ссылки:
├ <code>{start_link}</code></b>"""
    await call.message.edit_text(
        text=message,
        reply_markup=create_inline_keyboard(
            width=1,
            start="🔙 Назад"
        )
    )
