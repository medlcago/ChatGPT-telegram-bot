import logging

from aiogram import Bot, F, Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from database.db import Database
from decorators import MessageLogging
from filters import IsAdmin, ChatTypeFilter
from keyboards.callbacks import SendMessage
from keyboards.inline_main import get_confirmation_button
from states.admins import Administrators
from utils import is_number

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
    data = await state.get_data()

    message_to_user = data.get("message")
    user_id = is_number(message.text)
    if not user_id:
        await message.reply(f"<i>{message.text}</i> не является идентификатором пользователя.")
        return

    user_exists = await request.get_user(user_id=user_id)
    if user_exists:
        markup = get_confirmation_button("one").as_markup()
        caption = f"{message_to_user.text or message_to_user.caption}\n\nПолучатель:\n{user_exists.fullname}({user_id})"
        await message_to_user.copy_to(chat_id=message.chat.id,
                                      caption=caption,
                                      reply_markup=markup)

        await state.update_data(user_id=user_id)
        await state.update_data(recipient=f"{user_exists.fullname}({user_id})")
        await state.set_state(Administrators.SendMessage.confirmation)
    else:
        await message.reply(f"user_id <i>{user_id}</i> не найден в базе данных.")
        await state.clear()


@command_send_message_router.callback_query(Administrators.SendMessage.confirmation,
                                            SendMessage.filter((F.action == "confirmation") & (F.recipients == "one")),
                                            IsAdmin())
@MessageLogging
async def confirmation_send_message(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()

    message_to_user = data.get("message")
    user_id = data.get("user_id")
    reply_to_message_id = message_to_user.message_id
    from_chat_id = message_to_user.chat.id
    recipient = data.get("recipient")

    try:
        await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=reply_to_message_id)
        await call.message.delete()
        await call.message.answer(f"Сообщение успешно отправлено пользователю <b>{recipient}</b>",
                                  reply_to_message_id=reply_to_message_id)
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        await call.message.edit_text(
            "Произошла ошибка при отправке сообщения. Возможно, пользователь заблокировал бота.")
    finally:
        await state.clear()
        await call.answer()


@command_send_message_router.callback_query(Administrators.SendMessage.confirmation,
                                            SendMessage.filter((F.action == "cancel") & (F.recipients == "one")))
@MessageLogging
async def cancel_send_message(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()
    await call.message.answer("Действие было отменено.")
    await call.answer("Отменено")
