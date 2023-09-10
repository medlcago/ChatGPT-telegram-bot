from aiogram import Router, types, F, flags
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode

from database.db import Database
from decorators import MessageLogging
from exceptions import ActivationError
from filters import ChatTypeFilter
from keyboards.inline import contact_admin_button
from states.users import Users

command_promocode_router = Router()


async def promocode_activation_common(*, promocode, user_id, request: Database):
    if await request.check_user_subscription(user_id=user_id):
        return "Промокод не был активирован, т.к вы уже являетесь подписчиком."
    if await request.check_promocode(promocode):
        if await request.update_user_subscription_status(user_id=user_id, is_subscriber=True):
            return f"Промокод {hcode(promocode)} был успешно активирован ✅"
        raise ActivationError("Произошла ошибка при активации промокода. Пожалуйста, свяжитесь с администратором.")
    return f"Промокод {hcode(promocode)} не является действительным."


@command_promocode_router.message(Command(commands=["promocode"]), ChatTypeFilter(is_group=False))
@MessageLogging
@flags.skip
async def command_promocode(message: types.Message, state: FSMContext):
    await message.answer(
        f"Введите действительный промокод.\nПример промокода: {hcode('PROMO-LKG-000-QQQ')}\n\nЧтобы отменить это действие, используй /cancel")
    await state.set_state(Users.PromocodeActivation.promocode)


@command_promocode_router.callback_query(F.data.in_({"activate_promocode"}))
@MessageLogging
@flags.skip
async def command_promocode(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Активация промокода")
    await call.message.answer(
        f"Введите действительный промокод.\nПример промокода: {hcode('PROMO-LKG-000-QQQ')}\n\nЧтобы отменить это действие, используй /cancel")
    await state.set_state(Users.PromocodeActivation.promocode)


@command_promocode_router.message(F.text.regexp(r"^PROMO-[A-Z]{3}-\d{3}-[A-Z]{3}$"), Users.PromocodeActivation.promocode)
@MessageLogging
@flags.skip
async def promocode_activation(message: types.Message, state: FSMContext, request: Database):
    promocode = message.text
    user_id = message.from_user.id
    try:
        result = await promocode_activation_common(promocode=promocode, user_id=user_id, request=request)
        await message.reply(result)
    except ActivationError as error:
        await message.reply(str(error), reply_markup=contact_admin_button)
    await state.clear()


@command_promocode_router.message(Users.PromocodeActivation.promocode)
@MessageLogging
@flags.skip
async def promocode_activation(message: types.Message, state: FSMContext):
    promocode = message.text
    await message.reply(
        f"Промокод {hcode(promocode)} не является действительным.\nПример промокода: {hcode('PROMO-LKG-000-QQQ')}")
    await state.clear()
