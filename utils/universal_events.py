from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from decorators import MessageLogging
from filters import ChatTypeFilter
from language.translator import LocalizedTranslator

universal_events_router = Router()


@universal_events_router.callback_query(F.data.in_({"close", "delete"}))
@MessageLogging
async def delete_message(call: types.CallbackQuery):
    await call.answer("OK!")
    await call.message.delete()


@universal_events_router.message(Command(commands=["cancel"], prefix="/"), ChatTypeFilter(is_group=False))
@MessageLogging
async def cancel_action(message: types.Message, state: FSMContext, translator: LocalizedTranslator):
    await state.clear()
    await message.reply(translator.get("cancel-message"))
