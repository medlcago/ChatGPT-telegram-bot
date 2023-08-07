from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from filters import IsAdmin

command_cancel_router = Router()


@command_cancel_router.message(Command(commands=["cancel"], prefix="/"), IsAdmin())
async def command_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Действие было отменено.")
