from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext

from decorators import MessageLogging
from filters import ChatTypeFilter
from loader import db
from states.users import Users

command_promocode_router = Router()


async def promocode_activation_common(*, promocode, user_id):
    if await db.check_user_subscription(user_id=user_id):
        return "Промокод не был активирован, т.к вы уже являетесь подписчиком."
    if await db.check_promocode(promocode):
        if await db.grant_or_remove_subscription(user_id=user_id, is_subscriber=True):
            return f"Промокод <code>{promocode}</code> был успешно активирован ✅"
        return "Произошла ошибка при активации промокода. Пожалуйста, свяжитесь с администратором."
    return f"Промокод <code>{promocode}</code> не является действительным."


@command_promocode_router.message(Command(commands=["promocode"], prefix="/"), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_promocode(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите действительный промокод.\nПример промокода: <code>PROMO-LKG-000-QQQ</code>\n\nЧтобы отменить это действие, используй /cancel")
    await state.set_state(Users.PromocodeActivation.promocode)


@command_promocode_router.callback_query(Text(text="activate_promocode"))
@MessageLogging
async def command_promocode(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Активация промокода")
    await call.message.answer(
        "Введите действительный промокод.\nПример промокода: <code>PROMO-LKG-000-QQQ</code>\n\nЧтобы отменить это действие, используй /cancel")
    await state.set_state(Users.PromocodeActivation.promocode)


@command_promocode_router.message(F.text.regexp(r"^PROMO-[A-Z]{3}-\d{3}-[A-Z]{3}$"), Users.PromocodeActivation.promocode)
@MessageLogging
async def promocode_activation(message: types.Message, state: FSMContext):
    promocode = message.text
    user_id = message.from_user.id
    result = await promocode_activation_common(promocode=promocode, user_id=user_id)
    await message.reply(result)
    await state.clear()


@command_promocode_router.message(Users.PromocodeActivation.promocode)
@MessageLogging
async def promocode_activation(message: types.Message, state: FSMContext):
    promocode = message.text
    await message.reply(
        f"Промокод <code>{promocode}</code> не является действительным.\nПример промокода: <code>PROMO-LKG-000-QQQ</code>")
    await state.clear()
