import asyncio

from aiogram import Bot
from aiogram import Router
from aiogram import html
from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.command import Command, CommandObject

from decorators import MessageLogging
from filters import ChatTypeFilter
from utils.neural_networks import summarize_youtube_video

command_summary_router = Router()


@command_summary_router.message(Command(commands=["summary"], prefix="/"), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_summarize(message: types.Message, command: CommandObject, bot: Bot):
    url = command.args
    if url:
        loop = asyncio.get_event_loop()
        sent_message = await message.reply("Обработка запроса, ожидайте")
        summarize = html.quote(
            await loop.run_in_executor(None, summarize_youtube_video, url, message.from_user.language_code))
        try:
            await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                        text=summarize, disable_web_page_preview=True)
        except TelegramBadRequest as error:
            await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text=str(error))
    else:
        if message.from_user.language_code == "ru":
            await message.reply(
                f"Команда <b><i>{command.prefix + command.command}</i></b> оказалась пустой, запрос не может быть выполнен.")
        else:
            await message.reply(
                f"The command <b><i>{command.prefix + command.command}</i></b> was empty, the request could not be completed.")
