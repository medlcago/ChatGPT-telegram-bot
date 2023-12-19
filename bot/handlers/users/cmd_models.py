from aiogram import Router, types
from aiogram.filters.command import Command

from config import Config
from bot.decorators import MessageLogging
from bot.filters import ChatTypeFilter
from bot.keyboards.inline_main import close_button

command_models_router = Router()


@command_models_router.message(Command(commands="models"), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_models(message: types.Message, config: Config):
    available_models = "\n".join(config.models.available_models)
    await message.reply(f"Доступные модели:\n{available_models}", reply_markup=close_button)
