from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext

from bot.database.db import Database
from bot.decorators import MessageLogging, check_command_args
from bot.filters import IsAdmin, ChatTypeFilter
from bot.states.admins import Administrators
from bot.utils.misc import activate_subscription, deactivate_subscription
from keyboards.inline_main import close_button

subscription_management_router = Router()


# Выдача подписки
@subscription_management_router.message(Command(commands="grant_sub"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
@check_command_args
async def command_grant_subscription(message: types.Message, command: CommandObject, request: Database):
    user_id = command.args
    result = await activate_subscription(user_id=user_id, request=request)
    await message.reply(
        text=result,
        reply_markup=close_button
    )


@subscription_management_router.callback_query(F.data == "grant_sub", IsAdmin())
@MessageLogging
async def command_grant_subscription(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Выдача подписки")
    sent_message = await call.message.reply("Введите user_id пользователя, который получит подписку")
    await state.set_state(Administrators.GrantSubscription.user_id)
    await state.update_data(sent_message=sent_message)


@subscription_management_router.message(Administrators.GrantSubscription.user_id)
@MessageLogging
async def grant_subscription(message: types.Message, state: FSMContext, request: Database):
    user_id = message.text
    sent_message = (await state.get_data()).get("sent_message")
    result = await activate_subscription(user_id=user_id, request=request)
    await message.reply(result)

    await sent_message.delete()
    await state.clear()


# Удаление подписки
@subscription_management_router.message(Command(commands="remove_sub"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
@check_command_args
async def command_remove_subscription(message: types.Message, command: CommandObject, request: Database):
    user_id = command.args
    result = await deactivate_subscription(user_id=user_id, request=request)
    await message.reply(
        text=result,
        reply_markup=close_button
    )


@subscription_management_router.callback_query(F.data == "remove_sub", IsAdmin())
@MessageLogging
async def command_remove_subscription(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Удаление подписки")
    sent_message = await call.message.reply("Введите user_id подписчика, которого хотите удалить")
    await state.set_state(Administrators.RemoveSubscription.user_id)
    await state.update_data(sent_message=sent_message)


@subscription_management_router.message(Administrators.RemoveSubscription.user_id)
@MessageLogging
async def remove_subscription(message: types.Message, state: FSMContext, request: Database):
    user_id = message.text
    sent_message = (await state.get_data()).get("sent_message")
    result = await deactivate_subscription(user_id=user_id, request=request)
    await message.reply(
        text=result,
        reply_markup=close_button
    )
    await sent_message.delete()
    await state.clear()
