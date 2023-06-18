import asyncio
from aiogram import Router
from aiogram import html
from aiogram import types
from aiogram.filters import Command, CommandObject
from aiogram.types import URLInputFile

from decorators import message_logging
from filters import ChatTypeFilter
from utils.misc.neural_networks import image_generator

command_image_users_router = Router()


@command_image_users_router.message(Command(commands="image", prefix="/"), ChatTypeFilter(is_group=False))
@message_logging
async def command_image(message: types.Message, command: CommandObject):
    user_request = command.args
    if user_request:
        loop = asyncio.get_event_loop()
        user_request = html.quote(user_request)
        sent_message = await message.reply("Обработка запроса, ожидайте")
        image = URLInputFile(
            await loop.run_in_executor(None, image_generator, user_request),
            filename=user_request
        )
        if image:
            await message.reply_photo(photo=image,
                                      caption=f"👨 <b>Запрос отправлен пользователем</b>: <code>{message.from_user.full_name}</code>\n\n"
                                              f"🎈 <b>Айди сообщения</b>: <code>{message.message_id}</code>\n\n"
                                              f"🤔 <b>Запрос</b>: <code>{user_request}</code>")
            await sent_message.delete()
        else:
            await message.reply(f"❌ <b>OpenAI API не смог обработать запрос</b>: {user_request}")
    else:
        if message.from_user.language_code == "ru":
            await message.reply(
                f"Команда <b><i>{command.prefix + command.command}</i></b> оказалась пустой, запрос не может быть выполнен.")
        else:
            await message.reply(
                f"The command <b><i>{command.prefix + command.command}</i></b> was empty, the request could not be completed.")
