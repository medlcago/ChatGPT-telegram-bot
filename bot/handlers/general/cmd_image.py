from aiogram import Router, html, types, flags, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import URLInputFile

from config import Config
from bot.decorators import MessageLogging, check_command_args
from bot.exceptions import RequestProcessingError
from bot.keyboards.inline_main import close_button
from bot.language.translator import LocalizedTranslator
from bot.utils.neural_networks import ImageGenerator

command_image_router = Router()


@command_image_router.message(Command(commands="image", prefix="!/"))
@MessageLogging
@check_command_args
@flags.rate_limit(limit=30, key="image")
async def command_image(message: types.Message, command: CommandObject, config: Config, bot: Bot,
                        translator: LocalizedTranslator):
    prompt = html.quote(command.args)
    image_generator = ImageGenerator(
        api_key=config.openai.api_key,
        api_base=config.openai.api_base,
        model=config.models.default_image_model
    )
    sent_message = await message.reply(translator.get("processing-request-message"))
    try:
        image_response = await image_generator.generate_image(prompt=prompt)
        image = URLInputFile(
            image_response,
            filename=prompt
        )
        await message.reply_photo(photo=image,
                                  caption=f"👨 <b>Запрос отправлен пользователем</b>: {message.from_user.mention_html()}\n\n"
                                          f"🎈 <b>Айди сообщения</b>: <code>{message.message_id}</code>\n\n"
                                          f"🤔 <b>Запрос</b>: <code>{prompt}</code>",
                                  reply_markup=close_button
                                  )
        await sent_message.delete()
    except (TelegramBadRequest, RequestProcessingError) as error:
        await bot.edit_message_text(
            chat_id=sent_message.chat.id,
            message_id=sent_message.message_id,
            text=str(error),
            reply_markup=close_button
        )
