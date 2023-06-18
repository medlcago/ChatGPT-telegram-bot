from aiogram import types, Router
from aiogram.filters.command import Command

from decorators import message_logging
from filters import ChatTypeFilter
from loader import db

command_all_mention_router = Router()


@command_all_mention_router.message(Command(commands=["all"], prefix="@"), ChatTypeFilter(is_group=True, chat_id=-1001525007729))
@message_logging
async def command_all_mention(message: types.Message):
    members = await db.get_members()
    usernames = (f'@{member.get("username")}' for member in members)
    await message.reply("<b>Уебища, общий сбор:</b>\n" + "\n".join(usernames), disable_web_page_preview=True)
