from aiogram import Router, types
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext

from database.db import Database
from decorators import MessageLogging
from filters import IsAdmin, ChatTypeFilter
from states.admins import Administrators

user_management_router = Router()


async def block_user_common(*, user_id: str, request: Database):
    if user_id and user_id.isnumeric():
        user = await request.user_exists(user_id=user_id)
        if user:
            if user.is_blocked:
                return f"<b>{user.fullname}({user.user_id})</b> уже заблокирован."
            if await request.block_or_unblock_user(user_id=user_id, is_blocked=True):
                return f"<b>{user.fullname}({user.user_id})</b> был заблокирован."
            return f"Произошла ошибка. <b>{user.fullname}({user.user_id})</b> не был заблокирован."
        return f"user_id <i>{user_id}</i> не найден в базе данных."
    return "Аргумент не является идентификатором пользователя."


async def unblock_user_common(*, user_id: str, request: Database):
    if user_id and user_id.isnumeric():
        user = await request.user_exists(user_id=user_id)
        if user:
            if user.is_blocked:
                if await request.block_or_unblock_user(user_id=user_id, is_blocked=False):
                    return f"<b>{user.fullname}({user.user_id})</b> был разблокирован."
                return f"Произошла ошибка. <b>{user.fullname}({user.user_id})</b> не был разблокирован."
            return f"<b>{user.fullname}({user.user_id})</b> не заблокирован."
        return f"user_id <i>{user_id}</i> не найден в базе данных."
    return "Аргумент не является идентификатором пользователя."


# Блокировка пользователя
@user_management_router.message(Command(commands=["block"], prefix="/"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_block_user(message: types.Message, command: CommandObject, request: Database):
    user_id = command.args
    result = await block_user_common(user_id=user_id, request=request)
    await message.reply(result)


@user_management_router.callback_query(Text(text="block_user"), IsAdmin())
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
    result = await block_user_common(user_id=user_id, request=request)
    await message.reply(result)

    await sent_message.delete()
    await state.clear()


# Разблокировка пользователя
@user_management_router.message(Command(commands=["unblock"], prefix="/"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_unblock_user(message: types.Message, command: CommandObject, request: Database):
    user_id = command.args
    result = await unblock_user_common(user_id=user_id, request=request)
    await message.reply(result)


@user_management_router.callback_query(Text(text="unblock_user"), IsAdmin())
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
    result = await unblock_user_common(user_id=user_id, request=request)
    await message.reply(result)

    await sent_message.delete()
    await state.clear()
