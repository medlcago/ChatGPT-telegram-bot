from aiogram import Router, F, types, Bot
from aiogram.filters.command import Command
from aiogram.types import BufferedInputFile

from data.config import main_chat_ids
from filters import ChatTypeFilter

edit_chat_router = Router()
edit_chat_router.message.filter(F.chat.id.in_(main_chat_ids))


@edit_chat_router.message(Command(commands=["set_photo"], prefix="!.?", ignore_case=True),
                          F.reply_to_message.photo,
                          ChatTypeFilter(is_group=True))
async def command_set_photo(message: types.Message, bot: Bot):
    photo_id = await bot.get_file(message.reply_to_message.photo[-1].file_id)
    photo_path = photo_id.file_path
    photo = (await bot.download_file(file_path=photo_path)).read()
    await message.chat.set_photo(photo=BufferedInputFile(file=photo, filename="photo.jpg"))


@edit_chat_router.message(Command(commands=["delete_photo"], prefix="!.?", ignore_case=True),
                          ChatTypeFilter(is_group=True))
async def command_delete_photo(message: types.Message):
    await message.chat.delete_photo()
    await message.reply("Главная фотография была удалена.")


@edit_chat_router.message(Command(commands=["set_title"], prefix="!.?", ignore_case=True),
                          F.reply_to_message.text,
                          ChatTypeFilter(is_group=True))
async def command_set_title(message: types.Message):
    title = message.reply_to_message.text
    await message.chat.set_title(title)
