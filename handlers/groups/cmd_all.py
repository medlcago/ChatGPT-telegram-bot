from aiogram import types, Router, F
from aiogram.filters.command import Command

from data.config import main_chat_ids
from decorators import MessageLogging
from filters import ChatTypeFilter
from loader import db

command_all_mention_router = Router()
command_all_mention_router.message.filter(F.chat.id.in_(main_chat_ids))


@command_all_mention_router.message(Command(commands=["all"], prefix="@"), ChatTypeFilter(is_group=True))
@MessageLogging
async def command_all_mention(message: types.Message):
    members = await db.get_members()
    usernames = (f'@{member.username}' for member in members)
    await message.reply("<b>Уебища, общий сбор:</b>\n" + "\n".join(usernames), disable_web_page_preview=True)
