from aiogram import Router, F, types, flags
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.decorators import MessageLogging
from bot.filters import ChatTypeFilter
from bot.language.translator import LocalizedTranslator

universal_handler_router = Router()


@universal_handler_router.callback_query(F.data.in_({"close", "delete"}))
@MessageLogging
@flags.skip
async def delete_message(call: types.CallbackQuery):
    await call.answer("OK!")
    await call.message.delete()


@universal_handler_router.message(Command(commands="cancel", prefix="/"), ChatTypeFilter(is_group=False))
@MessageLogging
@flags.skip
async def cancel_action(message: types.Message, state: FSMContext, translator: LocalizedTranslator):
    await state.clear()
    await message.reply(translator.get("cancel-message"))
