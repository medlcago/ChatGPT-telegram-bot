from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext

from decorators import message_logging
from filters import IsAdmin
from keyboards.inline import btn_send_message
from loader import bot
from loader import db
from states.admins import Administrators

command_send_message_router = Router()


@command_send_message_router.message(Command(commands=["send_message"], prefix="/"), IsAdmin())
@message_logging
async def command_send_message(message: types.Message, state: FSMContext):
    await message.reply("Введите сообщение, которое хотите отправить")
    await state.set_state(Administrators.SendMessage.message)


@command_send_message_router.callback_query(Text(text="send_message"), IsAdmin())
@message_logging
async def command_send_message(call: types.callback_query, state: FSMContext):
    await call.answer()
    await call.message.reply("Введите сообщение, которое хотите отправить")
    await state.set_state(Administrators.SendMessage.message)


@command_send_message_router.message(Administrators.SendMessage.message, IsAdmin())
@message_logging
async def get_recipient_user_id(message: types.Message, state: FSMContext):
    await state.update_data(message=message)
    await message.reply("Введите user_id пользователя, который получит данное сообщение")
    await state.set_state(Administrators.SendMessage.user_id)


@command_send_message_router.message(Administrators.SendMessage.user_id, IsAdmin())
@message_logging
async def message_to_send(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.text)

    message_to_user = ((await state.get_data()).get("message")).text
    user_id = (await state.get_data()).get("user_id")
    user_exists = await db.user_exists(user_id=user_id)

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


@command_send_message_router.callback_query(Administrators.SendMessage.confirmation,
                                            Text(text="confirmation_send_message"), IsAdmin())
@message_logging
async def confirmation_send_message(call: types.CallbackQuery, state: FSMContext):
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
        print(e)
        await call.message.edit_text(
            "Произошла ошибка при отправке сообщения. Возможно, пользователь заблокировал бота.")
    await state.clear()
    await call.answer()


@command_send_message_router.callback_query(Administrators.SendMessage.confirmation, Text(text="cancel_send_message"),
                                            IsAdmin())
@message_logging
async def cancel_send_message(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Действие было отменено.")
    await call.answer()
