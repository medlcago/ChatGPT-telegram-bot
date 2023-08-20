import asyncio

from aiogram import Router
from aiogram import html
from aiogram import types
from aiogram.filters import Command, CommandObject
from aiogram.types import URLInputFile

from data.config import Config
from decorators import MessageLogging
from utils.neural_networks import ImageGenerator

command_image_router = Router()


@command_image_router.message(Command(commands=["image"], prefix="!/"))
@MessageLogging
async def command_image(message: types.Message, command: CommandObject, config: Config):
    prompt = command.args
    if prompt:
        loop = asyncio.get_event_loop()
        prompt = html.quote(prompt)
        image_generator = ImageGenerator(api_key=config.openai.api_key, api_base=config.openai.api_base, model="sdxl")
        sent_message = await message.reply("Обработка запроса, ожидайте")
        image = URLInputFile(
            await loop.run_in_executor(None, image_generator.generate_image, prompt),
            filename=prompt
        )
        if image:
            await message.reply_photo(photo=image,
                                      caption=f"👨 <b>Запрос отправлен пользователем</b>: {message.from_user.mention_html()}\n\n"
                                              f"🎈 <b>Айди сообщения</b>: <code>{message.message_id}</code>\n\n"
                                              f"🤔 <b>Запрос</b>: <code>{prompt}</code>")
            await sent_message.delete()
        else:
            await message.reply(f"❌ <b>OpenAI API не смог обработать запрос</b>: {prompt}")
    else:
        if message.from_user.language_code == "ru":
            await message.reply(
                f"Команда <b><i>{command.prefix + command.command}</i></b> оказалась пустой, запрос не может быть выполнен.")
        else:
            await message.reply(
                f"The command <b><i>{command.prefix + command.command}</i></b> was empty, the request could not be completed.")
