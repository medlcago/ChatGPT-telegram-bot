import asyncio
import logging

from aiogram import Bot, F, types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from database.db import Database
from decorators import MessageLogging
from filters import ChatTypeFilter, IsAdmin
from keyboards.callbacks import SendMessage
from keyboards.inline_main import get_confirmation_button
from states.admins import Administrators

command_send_all_router = Router()


@command_send_all_router.message(Command(commands=["send_all"]), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_send_all(message: types.Message, state: FSMContext):
    await message.reply("Введите сообщение для рассылки")
    await state.set_state(Administrators.Mailing.message)


@command_send_all_router.callback_query(F.data.in_({"send_all"}), IsAdmin())
@MessageLogging
async def command_send_all(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите сообщение для рассылки")
    await state.set_state(Administrators.Mailing.message)
    await call.answer()


@command_send_all_router.message(Administrators.Mailing.message)
@MessageLogging
async def message_send_all(message: types.Message, state: FSMContext):
    markup = get_confirmation_button("all").as_markup()

    await message.copy_to(chat_id=message.chat.id, caption=f"{message.text or message.caption}\n\nПолучатель:\nВсе пользователи бота.",
                          reply_markup=markup)
    await state.update_data(message=message)
    await state.set_state(Administrators.Mailing.confirmation)


@command_send_all_router.callback_query(Administrators.Mailing.confirmation,
                                        SendMessage.filter((F.action == "confirmation") & (F.recipients == "all")),
                                        IsAdmin())
@MessageLogging
async def confirmation_send_all(call: types.CallbackQuery, state: FSMContext, request: Database, bot: Bot):
    data = await state.get_data()

    message_to_user = data.get("message")
    from_chat_id = message_to_user.chat.id
    message_id = message_to_user.message_id

    await call.answer("Рассылка была запущена.")
    await call.message.delete()
    sent_message = await call.message.answer("Рассылка была запущена.\n\n/cancel - Остановить рассылку", reply_to_message_id=message_id)

    count = 0
    users = await request.get_all_users(is_active=True)
    for user in users:
        if (await state.get_state()) != "Mailing.confirmation":
            break
        try:
            await bot.copy_message(chat_id=user.user_id, from_chat_id=from_chat_id, message_id=message_id)
            count += 1
        except Exception as e:
            logging.error(f"Error sending message: {e}")
        finally:
            await asyncio.sleep(2)
    result = f"Рассылка завершена. Сообщение получили {count}/{len(users)}"
    await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text=result)
    await state.clear()


@command_send_all_router.callback_query(Administrators.Mailing.confirmation,
                                        SendMessage.filter((F.action == "cancel") & (F.recipients == "all")))
@MessageLogging
async def cancel_send_all(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Действие было отменено.")
    await call.answer("Отменено")
