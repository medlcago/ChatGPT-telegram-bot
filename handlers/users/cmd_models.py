from aiogram import Router, types
from aiogram.filters.command import Command

from data import config
from decorators import MessageLogging
from filters import ChatTypeFilter

command_models_router = Router()


@command_models_router.message(Command(commands=["models"], prefix="/"), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_models(message: types.Message):
    available_models = "\n".join(config.models)
    await message.reply(f"Доступные модели:\n{available_models}")
