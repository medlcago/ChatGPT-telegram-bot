from aiogram import Router, types
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext

from decorators import MessageLogging
from filters import IsAdmin, ChatTypeFilter
from loader import db
from states.admins import Administrators

admin_management_router = Router()


async def add_admin_common(user_id: str):
    if user_id and user_id.isnumeric():
        user = await db.user_exists(user_id=user_id)
        if user:
            if user.is_admin:
                return f"<b>{user.fullname}({user.user_id})</b> уже является администратором."
            else:
                await db.add_or_remove_admin(user_id=user_id, is_admin=True)
                return f"<b>{user.fullname}({user.user_id})</b> назначен администратором."
        else:
            return f"user_id <i>{user_id}</i> не найден в базе данных."
    else:
        return "Аргумент не является идентификатором пользователя."


async def remove_admin_common(user_id: str, from_user_id):
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
        return "Аргумент не является идентификатором пользователя."


# Добавление администратора
@admin_management_router.message(Command(commands=["add_admin"], prefix="/"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def add_admin(message: types.Message, command: CommandObject):
    user_id = command.args
    result = await add_admin_common(user_id)
    await message.reply(result)


@admin_management_router.callback_query(Text(text="add_admin"), IsAdmin())
@MessageLogging
async def add_admin(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Добавление администратора")
    sent_message = await call.message.reply("Введите user_id пользователя, который получит права администратора")
    await state.set_state(Administrators.AddAdmin.user_id)
    await state.update_data(sent_message=sent_message)


@admin_management_router.message(Administrators.AddAdmin.user_id)
@MessageLogging
async def add_admin(message: types.Message, state: FSMContext):
    user_id = message.text
    sent_message = (await state.get_data()).get("sent_message")
    result = await add_admin_common(user_id)
    await message.reply(result)

    await sent_message.delete()
    await state.clear()


# Удаление администратора
@admin_management_router.message(Command(commands=["remove_admin"], prefix="/"), ChatTypeFilter(is_group=False),
                                 IsAdmin())
@MessageLogging
async def remove_admin(message: types.Message, command: CommandObject):
    user_id = command.args
    from_user_id = message.from_user.id
    result = await remove_admin_common(user_id, from_user_id)
    await message.reply(result)


@admin_management_router.callback_query(Text(text="remove_admin"), IsAdmin())
@MessageLogging
async def remove_admin(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Удаление администратора")
    sent_message = await call.message.reply("Введите user_id администратора, которого хотите удалить")
    await state.set_state(Administrators.RemoveAdmin.user_id)
    await state.update_data(sent_message=sent_message)


@admin_management_router.message(Administrators.RemoveAdmin.user_id)
@MessageLogging
async def remove_admin(message: types.Message, state: FSMContext):
    user_id = message.text
    from_user_id = message.from_user.id
    sent_message = (await state.get_data()).get("sent_message")
    result = await remove_admin_common(user_id, from_user_id)
    await message.reply(result)

    await sent_message.delete()
    await state.clear()
