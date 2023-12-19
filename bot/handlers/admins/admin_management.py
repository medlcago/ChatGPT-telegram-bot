from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext

from bot.database.db import Database
from bot.decorators import MessageLogging, check_command_args
from bot.filters import IsAdmin, ChatTypeFilter
from bot.keyboards.inline_main import close_button
from bot.states.admins import Administrators
from bot.utils.misc import assign_admin_rights, revoke_admin_rights

admin_management_router = Router()


# Добавление администратора
@admin_management_router.message(Command(commands="add_admin"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
@check_command_args
async def command_add_admin(message: types.Message, command: CommandObject, request: Database):
    user_id = command.args
    result = await assign_admin_rights(user_id=user_id, request=request)
    await message.reply(
        text=result,
        reply_markup=close_button
    )


@admin_management_router.callback_query(F.data == "add_admin", IsAdmin())
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
    result = await assign_admin_rights(user_id=user_id, request=request)
    await message.reply(
        text=result,
        reply_markup=close_button
    )

    await sent_message.delete()
    await state.clear()


# Удаление администратора
@admin_management_router.message(Command(commands="remove_admin"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
@check_command_args
async def command_remove_admin(message: types.Message, command: CommandObject, request: Database):
    user_id = command.args
    from_user_id = message.from_user.id
    result = await revoke_admin_rights(user_id=user_id, from_user_id=from_user_id, request=request)
    await message.reply(
        text=result,
        reply_markup=close_button
    )


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
    result = await revoke_admin_rights(user_id=user_id, from_user_id=from_user_id, request=request)
    await message.reply(
        text=result,
        reply_markup=close_button
    )

    await sent_message.delete()
    await state.clear()
