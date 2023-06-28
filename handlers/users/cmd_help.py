from aiogram import Router, types
from aiogram import html
from aiogram.filters.command import Command

from data.templates import HELP_MESSAGE
from decorators import MessageLogging
from filters import ChatTypeFilter

command_help_users_router = Router()


def cmd_help(language="ru"):
    message = HELP_MESSAGE.get(language, HELP_MESSAGE["en"])
    request = html.quote("<запрос>" if language == "ru" else "<request>")
    return message.format(request=request)


@command_help_users_router.message(Command(commands=["help"], prefix="/"), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_help(message: types.Message):
    await message.answer(cmd_help(message.from_user.language_code))
