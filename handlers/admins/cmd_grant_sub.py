from aiogram import Router, types
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext

from decorators import message_logging
from filters import IsAdmin
from loader import db
from states.admins import Administrators

command_grant_sub_router = Router()


async def grant_subscription_common(user_id: str):
    if user_id and user_id.isnumeric():
        user = await db.user_exists(user_id=user_id)
        if user:
            if user.is_subscriber:
                return f"<b>{user.fullname}({user.user_id})</b> уже является подписчиком."
            else:
                if await db.grant_or_remove_subscription(user_id=user_id, is_subscriber=True):
                    return f"<b>{user.fullname}({user.user_id})</b> получил подписку."
                return f"Произошла ошибка. <b>{user.fullname}({user.user_id})</b> не получил подписку."
        else:
            return f"user_id <i>{user_id}</i> не найден в базе данных."
    else:
        return "Oops :("


@command_grant_sub_router.message(Command(commands=["grant_sub"], prefix="/"), IsAdmin())
@message_logging
async def grant_subscription(message: types.Message, command: CommandObject):
    user_id = command.args
    result = await grant_subscription_common(user_id)
    await message.reply(result)


@command_grant_sub_router.callback_query(Text(text="grant_sub"), IsAdmin())
@message_logging
async def grant_subscription(call: types.CallbackQuery, state: FSMContext):
    sent_message = await call.message.reply("Введите user_id пользователя, который получит подписку")
    await state.set_state(Administrators.GrantSubscription.user_id)
    await state.update_data(sent_message=sent_message)
    await call.answer()


@command_grant_sub_router.message(Administrators.GrantSubscription.user_id, IsAdmin())
@message_logging
async def grant_subscription(message: types.Message, state: FSMContext):
    user_id = message.text
    sent_message = (await state.get_data()).get("sent_message")
    result = await grant_subscription_common(user_id)
    await message.reply(result)

    await sent_message.delete()
    await state.clear()
