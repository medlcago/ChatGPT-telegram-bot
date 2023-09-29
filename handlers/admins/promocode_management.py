from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from database.db import Database
from decorators import MessageLogging
from filters import IsAdmin
from states.admins import Administrators
from utils.misc import validate_and_add_promocode, deactivate_promocode

promocode_management_router = Router()


# Создание промокода
@promocode_management_router.callback_query(F.data.in_({"create_promocode"}), IsAdmin())
@MessageLogging
async def command_add_promocode(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Создание промокода")
    sent_message = await call.message.answer("Введите кол-во активаций промокода (целое число) > 0")
    await state.set_state(Administrators.CreatePromocode.activations_count)
    await state.update_data(sent_message=sent_message)


@promocode_management_router.message(Administrators.CreatePromocode.activations_count, IsAdmin())
@MessageLogging
async def add_promocode(message: types.Message, state: FSMContext, request: Database):
    activations_count = message.text
    sent_message = (await state.get_data()).get("sent_message")
    result = await validate_and_add_promocode(activations_count=activations_count, request=request)
    await message.reply(result)

    await sent_message.delete()
    await state.clear()


# Деактивация промокода
@promocode_management_router.callback_query(F.data.in_({"deactivate_promocode"}), IsAdmin())
@MessageLogging
async def command_delete_promocode(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Деактивация промокода")
    sent_message = await call.message.answer("Введите промокод, который необходимо деактивировать")
    await state.set_state(Administrators.CreatePromocode.promocode)
    await state.update_data(sent_message=sent_message)


@promocode_management_router.message(Administrators.CreatePromocode.promocode, IsAdmin())
@MessageLogging
async def delete_promocode(message: types.Message, state: FSMContext, request: Database):
    promocode = message.text
    sent_message = (await state.get_data()).get("sent_message")
    result = await deactivate_promocode(promocode=promocode, request=request)
    await message.reply(result)

    await sent_message.delete()
    await state.clear()
