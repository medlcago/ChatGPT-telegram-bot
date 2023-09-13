from aiogram import Bot
from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject

from data.config import Config
from database.db import Database
from decorators import CheckTimeLimits, MessageLogging, check_command_args
from filters import ChatTypeFilter
from language.translator import LocalizedTranslator
from utils.neural_networks import ChatBot

command_gpt_groups_router = Router()


@command_gpt_groups_router.message(Command(commands=["gpt"], prefix="!"), ChatTypeFilter(is_group=True))
@MessageLogging
@check_command_args
@CheckTimeLimits
async def command_gpt(message: types.Message, command: CommandObject, bot: Bot, config: Config, request: Database, translator: LocalizedTranslator):
    prompt = command.args
    gpt_bot = ChatBot(api_key=config.openai.api_key, api_base=config.openai.api_base, model=config.models.default_model)
    sent_message = await message.reply(translator.get("processing-request-message"))
    bot_response = await gpt_bot.chat(prompt=prompt)
    try:
        await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                    text=bot_response, parse_mode="markdown")
    except TelegramBadRequest as error:
        await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                    text=str(error))
