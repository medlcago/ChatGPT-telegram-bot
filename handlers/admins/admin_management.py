from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext

from database.db import Database
from decorators import MessageLogging, check_command_args
from filters import IsAdmin, ChatTypeFilter
from states.admins import Administrators

admin_management_router = Router()


async def add_admin_common(*, user_id: str, request: Database):
    if user_id and user_id.isnumeric():
        user = await request.get_user(user_id=user_id)
        if user:
            if user.is_admin:
                return f"<b>{user.fullname}({user.user_id})</b> уже является администратором."
            if await request.update_admin_rights_status(user_id=user_id, is_admin=True):
                return f"<b>{user.fullname}({user.user_id})</b> назначен администратором."
            return f"<b>{user.fullname}({user.user_id})</b> не назначен администратором."
        return f"user_id <i>{user_id}</i> не найден в базе данных."
    return "Аргумент не является идентификатором пользователя."


async def remove_admin_common(*, user_id: str, from_user_id: int, request: Database):
    if user_id and user_id.isnumeric():
        user = await request.get_user(user_id=user_id)
        if user:
            if user.is_admin:
                if user.user_id != from_user_id:
                    if await request.update_admin_rights_status(user_id=user_id, is_admin=False):
                        return f"<b>{user.fullname}({user.user_id})</b> удален из администраторов."
                    return f"<b>{user.fullname}({user.user_id})</b> не удален из администраторов."
                return "Нельзя удалить самого себя!"
            return f"<b>{user.fullname}({user.user_id})</b> не является администратором."
        return f"user_id <i>{user_id}</i> не найден в базе данных."
    return "Аргумент не является идентификатором пользователя."


# Добавление администратора
@admin_management_router.message(Command(commands=["add_admin"]), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
@check_command_args
async def command_add_admin(message: types.Message, command: CommandObject, request: Database):
    user_id = command.args
    result = await add_admin_common(user_id=user_id, request=request)
    await message.reply(result)


@admin_management_router.callback_query(F.data.in_({"add_admin"}), IsAdmin())
@MessageLogging
async def command_add_admin(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Добавление администратора")
    sent_message = await call.message.reply("Введите user_id пользователя, который получит права администратора")
    await state.set_state(Administrators.AddAdmin.user_id)
    await state.update_data(sent_message=sent_message)


@admin_management_router.message(Administrators.AddAdmin.user_id)
@MessageLogging
async def add_admin(message: types.Message, state: FSMContext, request: Database):
    user_id = message.text
    sent_message = (await state.get_data()).get("sent_message")
    result = await add_admin_common(user_id=user_id, request=request)
    await message.reply(result)

    await sent_message.delete()
    await state.clear()


# Удаление администратора
@admin_management_router.message(Command(commands=["remove_admin"]), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
@check_command_args
async def command_remove_admin(message: types.Message, command: CommandObject, request: Database):
    user_id = command.args
    from_user_id = message.from_user.id
    result = await remove_admin_common(user_id=user_id, from_user_id=from_user_id, request=request)
    await message.reply(result)


@admin_management_router.callback_query(F.data.in_({"remove_admin"}), IsAdmin())
@MessageLogging
async def command_remove_admin(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Удаление администратора")
    sent_message = await call.message.reply("Введите user_id администратора, которого хотите удалить")
    await state.set_state(Administrators.RemoveAdmin.user_id)
    await state.update_data(sent_message=sent_message)


@admin_management_router.message(Administrators.RemoveAdmin.user_id)
@MessageLogging
async def remove_admin(message: types.Message, state: FSMContext, request: Database):
    user_id = message.text
    from_user_id = message.from_user.id
    sent_message = (await state.get_data()).get("sent_message")
    result = await remove_admin_common(user_id=user_id, from_user_id=from_user_id, request=request)
    await message.reply(result)

    await sent_message.delete()
    await state.clear()
