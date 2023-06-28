from aiogram import Router, types
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext

from decorators import MessageLogging
from filters import IsAdmin
from loader import db
from states.admins import Administrators

command_remove_admin_router = Router()


async def remove_admin(user_id: str, from_user_id):
    if user_id and user_id.isnumeric():
        user = await db.user_exists(user_id=user_id)
        if user:
            if user.is_admin:
                if user.user_id != from_user_id:
                    await db.add_or_remove_admin(user_id=user_id, is_admin=False)
                    return f"<b>{user.fullname}({user.user_id})</b> удален из администраторов."
                else:
                    return "Нельзя удалить самого себя!"
            else:
                return f"<b>{user.fullname}({user.user_id})</b> не является администратором."
        else:
            return f"user_id <i>{user_id}</i> не найден в базе данных."
    else:
        return "Oops :("


@command_remove_admin_router.message(Command(commands=["remove_admin"], prefix="/"), IsAdmin())
@MessageLogging
async def command_remove_admin(message: types.Message, command: CommandObject):
    user_id = command.args
    from_user_id = message.from_user.id
    result = await remove_admin(user_id, from_user_id)
    await message.reply(result)


@command_remove_admin_router.callback_query(Text(text="remove_admin"), IsAdmin())
@MessageLogging
async def command_remove_admin(call: types.CallbackQuery, state: FSMContext):
    sent_message = await call.message.reply("Введите user_id администратора, которого хотите удалить")
    await state.set_state(Administrators.RemoveAdmin.user_id)
    await state.update_data(sent_message=sent_message)
    await call.answer()


@command_remove_admin_router.message(Administrators.RemoveAdmin.user_id, IsAdmin())
@MessageLogging
async def command_remove_admin(message: types.Message, state: FSMContext):
    user_id = message.text
    from_user_id = message.from_user.id
    sent_message = (await state.get_data()).get("sent_message")
    result = await remove_admin(user_id, from_user_id)
    await message.reply(result)

    await sent_message.delete()
    await state.clear()
