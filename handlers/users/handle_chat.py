import asyncio

from aiogram import html
from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject

from data import config
from decorators import message_logging, check_time_limits
from filters import ChatTypeFilter
from filters import IsAdmin
from loader import db, bot
from utils.misc.neural_networks import chat_bing, chat_gpt_3, chat_gpt_4, chat_claude

handle_chat_router = Router()


@message_logging
@handle_chat_router.message(Command(commands=["switch"]), ChatTypeFilter(is_group=False), IsAdmin())
async def switch_chat_type(message: types.Message, command: CommandObject):
    args = command.args
    if args:
        if args in config.models.keys():
            chat_type = config.chat_type_mapping.get(args, 1)
            await message.reply(
                html.quote(
                    f"Текущий тип чата: {await db.switch_chat_type(user_id=message.from_user.id, chat_type=chat_type)}"))
        else:
            await message.reply("Ошибка смены типа чата. Повторите попытку.")
    else:
        if message.from_user.language_code == "ru":
            await message.reply(
                f"Команда <b><i>{command.prefix + command.command}</i></b> оказалась пустой, запрос не может быть выполнен.")
        else:
            await message.reply(
                f"The command <b><i>{command.prefix + command.command}</i></b> was empty, the request could not be completed.")


@message_logging
@check_time_limits
async def command_bing(message: types.Message):
    sent_message = await message.reply("Обработка запроса, ожидайте")
    try:
        bot_response = await chat_bing(message.text, message.from_user.id)
    except Exception as error:
        await bot.edit_message_text(text=f"Ошибка: {error}", chat_id=sent_message.chat.id,
                                    message_id=sent_message.message_id)
    else:
        text = bot_response[0:4095] if len(bot_response) > 4095 else bot_response
        try:
            await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text=text,
                                        parse_mode='markdown', disable_web_page_preview=True)
        except TelegramBadRequest as error:
            await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                        text=error.message)


@message_logging
@check_time_limits
async def command_gpt_3(message: types.Message):
    loop = asyncio.get_event_loop()
    sent_message = await message.reply("Обработка запроса, ожидайте")
    bot_response = await loop.run_in_executor(None, chat_gpt_3, message.text)
    try:
        await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text=bot_response,
                                    parse_mode="markdown", disable_web_page_preview=True)
    except TelegramBadRequest as error:
        await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                    text=error.message)


@message_logging
@check_time_limits
async def command_gpt_4(message: types.Message):
    loop = asyncio.get_event_loop()
    sent_message = await message.reply("Обработка запроса, ожидайте")
    bot_response = await loop.run_in_executor(None, chat_gpt_4, message.text)
    try:
        await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text=bot_response,
                                    parse_mode="markdown", disable_web_page_preview=True)
    except TelegramBadRequest as error:
        await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                    text=error.message)


@message_logging
@check_time_limits
async def command_claude(message: types.Message):
    loop = asyncio.get_event_loop()
    sent_message = await message.reply("Обработка запроса, ожидайте")
    bot_response = await loop.run_in_executor(None, chat_claude, message.text)
    try:
        await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text=bot_response,
                                    parse_mode="markdown", disable_web_page_preview=True)
    except TelegramBadRequest as error:
        await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                    text=error.message)


@handle_chat_router.message(ChatTypeFilter(is_group=False), F.content_type.in_({'text'}))
@message_logging
async def handle_chat(message: types.Message):
    chat_type = await db.get_chat_type(user_id=message.from_user.id)

    chat_handlers = {
        "gpt-3": command_gpt_3,
        "gpt-4": command_gpt_4,
        "bing": command_bing,
        "claude": command_claude,
    }

    chat_handler = chat_handlers.get(chat_type)

    if chat_handler:
        await chat_handler(message)
    else:
        await message.reply("Ошибка: тип чата не найден.")


@handle_chat_router.message(ChatTypeFilter(is_group=False))
@message_logging
async def handle_non_text_message(message: types.Message):
    await message.reply("Oops, something went wrong. Please, try again.")
