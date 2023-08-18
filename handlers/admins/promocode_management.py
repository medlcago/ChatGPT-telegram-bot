from aiogram import Router, types
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext

from database.db import Database
from decorators import MessageLogging
from filters import IsAdmin
from states.admins import Administrators
from utils.misc import generate_promocode

promocode_management_router = Router()


async def add_promocode_common(*, activations_count: str, request: Database):
    if activations_count.isnumeric() and int(activations_count) > 0:
        promocode = await generate_promocode()
        if await request.add_promocode(promocode=promocode, activations_count=activations_count):
            return f"Сгенерированный промокод: <code>{promocode}</code>\nКол-во активаций: {activations_count}"
        return "Произошла ошибка при создании промокода."
    return "Аргумент не является целым числом > 0"


async def delete_promocode_common(*, promocode: str, request: Database):
    if await request.promocode_exists(promocode=promocode):
        if await request.delete_promocode(promocode=promocode):
            return f"Промокод <code>{promocode}</code> был деактивирован."
        return f"Промокод <code>{promocode}</code> не был деактивирован."
    return f"Промокод <code>{promocode}</code> не существует."


# Создание промокода
@promocode_management_router.callback_query(Text(text="create_promocode"), IsAdmin())
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
    result = await add_promocode_common(activations_count=activations_count, request=request)
    await message.reply(result)

    await sent_message.delete()
    await state.clear()


# Деактивация промокода
@promocode_management_router.callback_query(Text(text="deactivate_promocode"), IsAdmin())
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
    result = await delete_promocode_common(promocode=promocode, request=request)
    await message.reply(result)

    await sent_message.delete()
    await state.clear()
