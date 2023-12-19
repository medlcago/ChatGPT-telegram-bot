from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext

from bot.database.db import Database
from bot.decorators import MessageLogging, check_command_args
from bot.filters import IsAdmin, ChatTypeFilter
from bot.states.admins import Administrators
from bot.utils.misc import suspend_user, unsuspend_user
from keyboards.inline_main import close_button

user_management_router = Router()


# Блокировка пользователя
@user_management_router.message(Command(commands="block"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
@check_command_args
async def command_block_user(message: types.Message, command: CommandObject, request: Database):
    user_id = command.args
    result = await suspend_user(user_id=user_id, request=request)
    await message.reply(
        text=result,
        reply_markup=close_button
    )


@user_management_router.callback_query(F.data == "block_user", IsAdmin())
@MessageLogging
async def command_block_user(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Блокировка пользователя")
    sent_message = await call.message.reply("Введите user_id пользователя, которого необходимо заблокировать")
    await state.set_state(Administrators.BlockUser.user_id)
    await state.update_data(sent_message=sent_message)


@user_management_router.message(Administrators.BlockUser.user_id)
@MessageLogging
async def block_user(message: types.Message, state: FSMContext, request: Database):
    user_id = message.text
    sent_message = (await state.get_data()).get("sent_message")
    result = await suspend_user(user_id=user_id, request=request)
    await message.reply(
        text=result,
        reply_markup=close_button
    )
    await sent_message.delete()
    await state.clear()


# Разблокировка пользователя
@user_management_router.message(Command(commands="unblock"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
@check_command_args
async def command_unblock_user(message: types.Message, command: CommandObject, request: Database):
    user_id = command.args
    result = await unsuspend_user(user_id=user_id, request=request)
    await message.reply(
        text=result,
        reply_markup=close_button
    )


@user_management_router.callback_query(F.data.in_({"unblock_user"}), IsAdmin())
@MessageLogging
async def command_unblock_user(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Разблокировка пользователя")
    sent_message = await call.message.reply("Введите user_id пользователя, которого необходимо разблокировать")
    await state.set_state(Administrators.UnblockUser.user_id)
    await state.update_data(sent_message=sent_message)


@user_management_router.message(Administrators.UnblockUser.user_id)
@MessageLogging
async def unblock_user(message: types.Message, state: FSMContext, request: Database):
    user_id = message.text
    sent_message = (await state.get_data()).get("sent_message")
    result = await unsuspend_user(user_id=user_id, request=request)
    await message.reply(
        text=result,
        reply_markup=close_button
    )
    await sent_message.delete()
    await state.clear()
