from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext

from decorators import MessageLogging
from filters import ChatTypeFilter
from keyboards.inline import btn_contact_admin
from loader import db
from states.users import Users

command_promocode_router = Router()


@command_promocode_router.message(Command(commands=["promocode"], prefix="/"), ChatTypeFilter(is_group=False))
@MessageLogging
async def command_promocode(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите действительный промокод.\nПример промокода: <code>PROMO-LKG-000-QQQ</code>\n\nЧтобы отменить это действие, используй /cancel")
    await state.set_state(Users.PromocodeActivation.promo_code)


@command_promocode_router.callback_query(Text(text="promocode"))
@MessageLogging
async def command_promocode(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Активация промокода")
    await call.message.answer(
        "Введите действительный промокод.\nПример промокода: <code>PROMO-LKG-000-QQQ</code>\n\nЧтобы отменить это действие, используй /cancel")
    await state.set_state(Users.PromocodeActivation.promo_code)


@command_promocode_router.message(F.text.regexp(r"^PROMO-[A-Z]{3}-\d{3}-[A-Z]{3}$"), Users.PromocodeActivation.promo_code)
@MessageLogging
async def promocode_activation(message: types.Message, state: FSMContext):
    promo_code = message.text
    user_id = message.from_user.id
    if await db.check_user_subscription(user_id=user_id):
        await message.reply("Промокод не был активирован, т.к вы уже являетесь подписчиком.")
        return
    if await db.check_promocode(promo_code):
        if await db.grant_or_remove_subscription(user_id=user_id, is_subscriber=True):
            await message.answer(
                f"Промокод <code>{promo_code}</code> был успешно активирован ✅")
        else:
            await message.answer("Произошла ошибка при активации подписки. Пожалуйста, свяжитесь с администратором.",
                                 reply_markup=btn_contact_admin)
    else:
        await message.answer(
            f"Промокод <code>{promo_code}</code> не является действительным.")
    await state.clear()


@command_promocode_router.message(Users.PromocodeActivation.promo_code)
@MessageLogging
async def promocode_activation(message: types.Message, state: FSMContext):
    promo_code = message.text
    await message.answer(
        f"Промокод <code>{promo_code}</code> не является действительным.\nПример промокода: <code>PROMO-LKG-000-QQQ</code>")
    await state.clear()
