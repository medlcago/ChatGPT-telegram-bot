from aiogram import Router, types
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext

from decorators import MessageLogging
from filters import IsAdmin
from loader import db
from states.admins import Administrators

command_remove_sub_router = Router()


async def remove_subscription(user_id: str):
    if user_id and user_id.isnumeric():
        user = await db.user_exists(user_id=user_id)
        if user:
            if user.is_subscriber:
                if await db.grant_or_remove_subscription(user_id=user_id, is_subscriber=False):
                    return f"<b>{user.fullname}({user.user_id})</b> лишился подписки."
                return "Произошла ошибка. <b>{user.fullname}({user.user_id})</b> не лишился подписки."
            else:
                return f"<b>{user.fullname}({user.user_id})</b> не является подписчиком."
        else:
            return f"user_id <i>{user_id}</i> не найден в базе данных."
    else:
        return "Oops :("


@command_remove_sub_router.message(Command(commands=["remove_sub"], prefix="/"), IsAdmin())
@MessageLogging
async def command_remove_subscription(message: types.Message, command: CommandObject):
    user_id = command.args
    result = await remove_subscription(user_id)
    await message.reply(result)


@command_remove_sub_router.callback_query(Text(text="remove_sub"), IsAdmin())
@MessageLogging
async def command_remove_subscription(call: types.CallbackQuery, state: FSMContext):
    sent_message = await call.message.reply("Введите user_id подписчика, которого хотите удалить")
    await state.set_state(Administrators.RemoveSubscription.user_id)
    await state.update_data(sent_message=sent_message)
    await call.answer()


@command_remove_sub_router.message(Administrators.RemoveSubscription.user_id, IsAdmin())
@MessageLogging
async def command_remove_subscription(message: types.Message, state: FSMContext):
    user_id = message.text
    sent_message = (await state.get_data()).get("sent_message")
    result = await remove_subscription(user_id)
    await message.reply(result)

    await sent_message.delete()
    await state.clear()
