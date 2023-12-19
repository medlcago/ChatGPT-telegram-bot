from aiogram import Router, types, F, flags

from bot.database.db import Database
from bot.decorators import MessageLogging
from bot.exceptions import ActivationError
from bot.keyboards.inline_main import contact_admin_button, close_button
from bot.utils.misc import activate_promocode

command_promocode_router = Router()


@command_promocode_router.message(F.text.regexp(r"^PROMO-[A-Z]{3}-\d{3}-[A-Z]{3}$"))
@MessageLogging
@flags.skip
async def promocode_activation(message: types.Message, request: Database):
    promocode = message.text
    user_id = message.from_user.id
    try:
        result = await activate_promocode(promocode=promocode, user_id=user_id, request=request)
        await message.reply(result, reply_markup=close_button)
    except ActivationError as error:
        await message.reply(str(error), reply_markup=contact_admin_button)
