from aiogram import Router
from aiogram import html
from aiogram import types
from aiogram.filters import Command, CommandObject
from aiogram.types import URLInputFile

from data.config import Config
from decorators import MessageLogging, check_command_args
from utils.neural_networks import ImageGenerator

command_image_router = Router()


@command_image_router.message(Command(commands=["image"], prefix="!/"))
@MessageLogging
@check_command_args
async def command_image(message: types.Message, command: CommandObject, config: Config):
    prompt = html.quote(command.args)
    image_generator = ImageGenerator(api_key=config.openai.api_key, api_base=config.openai.api_base, model="sdxl")
    sent_message = await message.reply("Обработка запроса, ожидайте")
    image_response = await image_generator.generate_image(prompt=prompt)
    if image_response:
        image = URLInputFile(
            image_response,
            filename=prompt
        )
        await message.reply_photo(photo=image,
                                  caption=f"👨 <b>Запрос отправлен пользователем</b>: {message.from_user.mention_html()}\n\n"
                                          f"🎈 <b>Айди сообщения</b>: <code>{message.message_id}</code>\n\n"
                                          f"🤔 <b>Запрос</b>: <code>{prompt}</code>")
        await sent_message.delete()
    else:
        await message.reply(f"❌ <b>OpenAI API не смог обработать запрос</b>: {prompt}")
