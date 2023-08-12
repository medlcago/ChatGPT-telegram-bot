import asyncio
from aiogram import types, Router, F, html
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject

from data import config
from decorators import CheckTimeLimits, MessageLogging
from filters import ChatTypeFilter, IsAdmin, IsSubscription
from keyboards.inline import btn_promocode_activation
from loader import db, bot
from utils.neural_networks import ChatBot

handle_chat_router = Router()


@handle_chat_router.message(Command(commands=["switch"]), ChatTypeFilter(is_group=False), IsSubscription())
@handle_chat_router.message(Command(commands=["switch"]), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def switch_chat_type(message: types.Message, command: CommandObject):
    chat_type = command.args
    if chat_type:
        if chat_type in config.models:
            await message.reply(
                html.quote(
                    f"Текущая модель: {await db.switch_chat_type(user_id=message.from_user.id, chat_type=chat_type)}"))
        else:
            available_models = "\n".join(config.models)
            await message.reply(f"Ошибка смены модели. Повторите попытку.\n\nДоступные модели:\n{available_models}")
    else:
        if message.from_user.language_code == "ru":
            await message.reply(
                f"Команда <b><i>{command.prefix + command.command}</i></b> оказалась пустой, запрос не может быть выполнен.")
        else:
            await message.reply(
                f"The command <b><i>{command.prefix + command.command}</i></b> was empty, the request could not be completed.")


@handle_chat_router.message(Command(commands=["switch"]), ChatTypeFilter(is_group=False))
@MessageLogging
async def switch_chat_type(message: types.Message, command: CommandObject):
    if message.from_user.language_code == "ru":
        await message.reply(
            f"Команда <b><i>{command.prefix + command.command}</i></b> доступна только premium пользователям.",
            reply_markup=btn_promocode_activation)
    else:
        await message.reply(
            f"The command <b><i>{command.prefix + command.command}</i></b> is only available to premium users.",
            reply_markup=btn_promocode_activation)


@MessageLogging
@CheckTimeLimits
async def command_gpt(message: types.Message, model: str):
    loop = asyncio.get_event_loop()
    gpt_bot = ChatBot(api_key=config.OpenAI_API_KEY, model=model)
    sent_message = await message.reply("Обработка запроса, ожидайте")
    bot_response = await loop.run_in_executor(None, gpt_bot.chat, message.text)
    try:
        await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text=bot_response,
                                    parse_mode="markdown", disable_web_page_preview=True)
    except TelegramBadRequest as error:
        await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                    text=error.message)


@handle_chat_router.message(ChatTypeFilter(is_group=False), F.content_type.in_({'text'}))
@MessageLogging
async def handle_chat(message: types.Message):
    model = await db.get_chat_type(user_id=message.from_user.id)

    if model:
        await command_gpt(message, model)
    else:
        await message.reply("Ошибка: модель не найдена.")


@handle_chat_router.message(ChatTypeFilter(is_group=False))
@MessageLogging
async def handle_non_text_message(message: types.Message):
    if message.from_user.language_code == "ru":
        await message.reply(
            "К сожалению, бот умеет работать только с текстом. Пожалуйста, повторите свой запрос в текстовом виде.")
    else:
        await message.reply("Unfortunately, the bot can only work with text. Please, repeat your request in text form.")
