from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from decorators import MessageLogging
from filters import ChatTypeFilter

command_cancel_router = Router()


@command_cancel_router.message(Command(commands=["cancel"], prefix="/"), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Действие было отменено.")
