from aiogram import Router, types
from aiogram.filters.command import Command

from data.config import Config
from decorators import MessageLogging
from filters import ChatTypeFilter

command_models_router = Router()


@command_models_router.message(Command(commands=["models"]), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_models(message: types.Message, config: Config):
    available_models = "\n".join(config.models.available_models)
    await message.reply(f"Доступные модели:\n{available_models}")
