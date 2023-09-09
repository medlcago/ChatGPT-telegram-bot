import asyncio

from aiogram import Bot, flags
from aiogram import Router
from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.command import Command, CommandObject

from data.config import Config
from decorators import MessageLogging, check_command_args
from exceptions import RequestProcessingError
from filters import ChatTypeFilter
from utils.neural_networks import SummarizeVideo

command_summary_router = Router()


@command_summary_router.message(Command(commands=["summary"]), ChatTypeFilter(is_group=False))
@MessageLogging
@check_command_args
@flags.rate_limit(rate=60, limit=1, key="summary")
async def command_summarize(message: types.Message, command: CommandObject, bot: Bot, config: Config):
    url = command.args
    loop = asyncio.get_event_loop()
    sent_message = await message.reply("Обработка запроса, ожидайте")
    summarize_video = SummarizeVideo(api_key=config.openai.api_key, api_base=config.openai.api_base,
                                     model="gpt-3.5-turbo-16k")
    response = await loop.run_in_executor(None, summarize_video.summarize_youtube_video, url,
                                          message.from_user.language_code)
    try:
        await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                    text=response, disable_web_page_preview=True, parse_mode="markdown")
    except (TelegramBadRequest, RequestProcessingError) as error:
        await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text=str(error))
