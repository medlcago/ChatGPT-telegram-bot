import logging

from aiogram import Bot, F
from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from database.db import Database
from decorators import MessageLogging
from filters import IsAdmin, ChatTypeFilter
from keyboards.inline import btn_send_message
from states.admins import Administrators

command_send_message_router = Router()


@command_send_message_router.message(Command(commands=["send_message"]), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_send_message(message: types.Message, state: FSMContext):
    await message.reply("Введите сообщение, которое хотите отправить")
    await state.set_state(Administrators.SendMessage.message)


@command_send_message_router.callback_query(F.data.in_({"send_message"}), IsAdmin())
@MessageLogging
async def command_send_message(call: types.callback_query, state: FSMContext):
    await call.answer()
    await call.message.reply("Введите сообщение, которое хотите отправить")
    await state.set_state(Administrators.SendMessage.message)


@command_send_message_router.message(Administrators.SendMessage.message)
@MessageLogging
async def get_recipient_user_id(message: types.Message, state: FSMContext):
    await state.update_data(message=message)
    await message.reply("Введите user_id пользователя, который получит данное сообщение")
    await state.set_state(Administrators.SendMessage.user_id)


@command_send_message_router.message(Administrators.SendMessage.user_id)
@MessageLogging
async def message_to_send(message: types.Message, state: FSMContext, request: Database):
    await state.update_data(user_id=message.text)

    message_to_user = ((await state.get_data()).get("message")).text
    user_id = (await state.get_data()).get("user_id")
    user_exists = await request.user_exists(user_id=user_id)

    if user_exists:
        await message.answer(f"Сообщение:\n{message_to_user}\n\nПолучатель:\n{user_exists.fullname}({user_id})",
                             reply_markup=btn_send_message)
        await state.set_state(Administrators.SendMessage.confirmation)

        reply_to_message_id = ((await state.get_data()).get("message")).message_id

        await state.update_data(reply_to_message_id=reply_to_message_id)
        await state.update_data(recipient=f"{user_exists.fullname}({user_id})")
    else:
        await message.reply(f"user_id <i>{user_id}</i> не найден в базе данных.")
        await state.clear()


@command_send_message_router.callback_query(Administrators.SendMessage.confirmation, F.data.in_({"confirmation_send_message"}), IsAdmin())
@MessageLogging
async def confirmation_send_message(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    message_to_user = ((await state.get_data()).get("message")).text
    user_id = (await state.get_data()).get("user_id")
    reply_to_message_id = (await state.get_data()).get("reply_to_message_id")
    recipient = (await state.get_data()).get("recipient")

    try:
        await bot.send_message(chat_id=user_id, text=message_to_user)
        await call.message.delete()
        await call.message.answer(f"Сообщение успешно отправлено пользователю <b>{recipient}</b>",
                                  reply_to_message_id=reply_to_message_id)
    except Exception as e:
        logging.error(e)
        await call.message.edit_text(
            "Произошла ошибка при отправке сообщения. Возможно, пользователь заблокировал бота.")
    await state.clear()
    await call.answer()


@command_send_message_router.callback_query(Administrators.SendMessage.confirmation, F.data.in_({"cancel_send_message"}))
@MessageLogging
async def cancel_send_message(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Действие было отменено.")
    await call.answer("Отменено")
