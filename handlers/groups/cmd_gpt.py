import asyncio

from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject

from data import config
from decorators import CheckTimeLimits
from decorators import MessageLogging
from filters import ChatTypeFilter
from loader import bot
from utils.misc.neural_networks import ChatBot

command_gpt_groups_router = Router()


@command_gpt_groups_router.message(Command(commands=["gpt"], prefix="!"), ChatTypeFilter(is_group=True))
@MessageLogging
@CheckTimeLimits
async def command_gpt(message: types.Message, command: CommandObject):
    args = command.args
    if args:
        loop = asyncio.get_event_loop()
        gpt_3_bot = ChatBot(api_key=config.OpenAI_API_KEY, model="gpt-3.5-turbo")
        sent_message = await message.reply("Обработка запроса, ожидайте")
        bot_response = await loop.run_in_executor(None, gpt_3_bot.chat, message.text)
        try:
            await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                        text=bot_response, parse_mode="markdown")
        except TelegramBadRequest as error:
            await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text=error)
    else:
        await message.reply(
            f"Команда <b><i>{command.prefix + command.command}</i></b> оказалась пустой, запрос не может быть выполнен.")
