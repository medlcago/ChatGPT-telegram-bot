from aiogram import Router, types, flags, F
from aiogram import html
from aiogram.filters.command import Command, CommandObject
from aiogram.types import Message, CallbackQuery

from bot.database.db import Database
from bot.decorators import MessageLogging
from bot.filters import ChatTypeFilter
from bot.keyboards.inline_main import my_profile_and_affiliate_program_buttons, close_button
from bot.language.translator import LocalizedTranslator
from bot.utils import deeplink_decode
from config import config

command_start_help_router = Router()


@command_start_help_router.message(Command(commands="start"), ChatTypeFilter(is_group=False))
@MessageLogging
@flags.rate_limit(rate=120, limit=1, key="start")
async def command_start(message: Message, command: CommandObject, request: Database, translator: LocalizedTranslator):
    referrer_id = deeplink_decode(payload=command.args)
    user_id = message.from_user.id
    fullname = message.from_user.full_name
    username = message.from_user.username

    if await request.get_user(user_id=user_id) is None:
        if referrer_id and user_id != referrer_id and await request.get_user(user_id=referrer_id):
            await request.add_user(user_id=user_id, fullname=fullname, referrer=referrer_id)
            await message.bot.send_message(chat_id=referrer_id,
                                           text=f"<b>Новый реферал — <code>{fullname}[{user_id}]</code>!</b>"
                                           )
        else:
            await request.add_user(user_id=user_id, fullname=fullname)

        await message.bot.send_message(
            chat_id=config.creator_user_id,
            text=f"<b>Новый пользователь!</b>\n\n"
                 f"<b>username:</b> {'@' + username if username else '❌'}\n"
                 f"<b>user_id:</b> <code>{user_id}</code>",
            reply_markup=close_button
        )

    await message.answer(translator.get("start-message", full_name=html.quote(message.from_user.full_name)))

    current_model = await request.get_user_chat_type(user_id=user_id)
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
