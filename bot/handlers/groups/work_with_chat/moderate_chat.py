from aiogram import Router, F, types
from aiogram.filters import Command

from config import main_chat_ids
from bot.filters import ChatTypeFilter

moderate_chat_router = Router()
moderate_chat_router.message.filter(F.chat.id.in_(main_chat_ids))


@moderate_chat_router.message(Command(commands=["ban"], prefix="!.?", ignore_case=True),
                              F.reply_to_message,
                              ChatTypeFilter(is_group=True))
async def command_ban(message: types.Message):
    await message.chat.ban(user_id=message.reply_to_message.from_user.id)
    full_name = message.reply_to_message.from_user.mention_html()
    sticker = "CAACAgIAAx0CYVbdjQACBjxkxZ8Xvc59VUYCJeJG8DFKghHzfgACvwEAAhZCawovE0xX2Fzjzi8E"
    await message.reply(f"Пользователь {full_name} был заблокирован.")
    await message.answer_sticker(sticker=sticker)


@moderate_chat_router.message(Command(commands=["unban"], prefix="!.?", ignore_case=True),
                              F.reply_to_message,
                              ChatTypeFilter(is_group=True))
async def command_unban(message: types.Message):
    await message.chat.unban(user_id=message.reply_to_message.from_user.id)
    full_name = message.reply_to_message.from_user.mention_html()
    await message.reply(f"Пользователь {full_name} был разблокирован.")
