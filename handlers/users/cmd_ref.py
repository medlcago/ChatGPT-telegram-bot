from aiogram import Router, types, Bot
from aiogram.filters.command import Command
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.markdown import hcode

from decorators import MessageLogging
from filters import ChatTypeFilter

command_ref_router = Router()


@command_ref_router.message(Command(commands=["ref"]), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_ref(message: types.Message, bot: Bot):
    start_link = await create_start_link(bot=bot, payload=str(message.from_user.id), encode=True)
    await message.reply(f"Ваша реферальная ссылка:\n{hcode(start_link)}")
