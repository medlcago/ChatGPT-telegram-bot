from aiogram import Router, types, flags, F
from aiogram import html
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery

from bot.database.db import Database
from bot.decorators import MessageLogging
from bot.filters import ChatTypeFilter
from bot.keyboards.inline_main import my_profile_and_affiliate_program_buttons
from bot.language.translator import LocalizedTranslator

command_start_help_router = Router()


@command_start_help_router.message(Command(commands="start"), ChatTypeFilter(is_group=False))
@MessageLogging
@flags.rate_limit(rate=120, limit=1, key="start")
@flags.registration
async def command_start(message: Message, request: Database, translator: LocalizedTranslator):
    await message.answer(translator.get("start-message", full_name=html.quote(message.from_user.full_name)))
    current_model = await request.get_user_chat_type(user_id=message.from_user.id)
    await message.answer(
        text=translator.get("sub-start-message", current_model=current_model),
        reply_markup=my_profile_and_affiliate_program_buttons
    )


@command_start_help_router.message(Command(commands="help"), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_help(message: types.Message, translator: LocalizedTranslator):
    await message.answer(translator.get("help-message"))


@command_start_help_router.callback_query(F.data == "start")
@MessageLogging
async def command_back_start(call: CallbackQuery, request: Database, translator: LocalizedTranslator):
    user_id = call.from_user.id
    current_model = await request.get_user_chat_type(user_id=user_id)
    await call.message.edit_text(
        text=translator.get("sub-start-message", current_model=current_model),
        reply_markup=my_profile_and_affiliate_program_buttons
    )
    await call.answer("OK!")
