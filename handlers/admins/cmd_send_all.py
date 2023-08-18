import asyncio
import logging

from aiogram import Bot
from aiogram import types, Router
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext

from database.db import Database
from decorators import MessageLogging
from filters import ChatTypeFilter
from filters import IsAdmin
from keyboards.inline import btn_send_all
from states.admins import Administrators

command_send_all_router = Router()


async def send_all(*, message_to_user: str, request: Database, bot: Bot, command: CommandObject = None):
    if message_to_user:
        count = 0
        users = await request.get_all_users()
        for user in users:
            try:
                await bot.send_message(chat_id=user.user_id, text=message_to_user)
                count += 1
            except Exception as e:
                logging.error(e)
            finally:
                await asyncio.sleep(2)
            return f"Рассылка завершена. Сообщение получили {count}/{len(users)}"
    return f"Команда <b><i>{command.prefix + command.command}</i></b> оказалась пустой, запрос не может быть выполнен."


@command_send_all_router.message(Command(commands=["send_all"], prefix="/"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_send_all(message: types.Message, command: CommandObject, request: Database, bot: Bot):
    args = command.args
    await message.reply(await send_all(message_to_user=args, request=request, bot=bot, command=command))


@command_send_all_router.callback_query(Text(text="send_all"), IsAdmin())
@MessageLogging
async def command_send_all(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите сообщение для рассылки")
    await state.set_state(Administrators.Mailing.message)
    await call.answer()


@command_send_all_router.message(Administrators.Mailing.message)
@MessageLogging
async def message_send_all(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    await message.answer(f"Сообщение для рассылки:\n{message.text}", reply_markup=btn_send_all)
    await state.set_state(Administrators.Mailing.confirmation)


@command_send_all_router.callback_query(Administrators.Mailing.confirmation, Text(text="confirmation_send_all"), IsAdmin())
@MessageLogging
async def confirmation_send_all(call: types.CallbackQuery, state: FSMContext, request: Database, bot: Bot):
    message_to_user = (await state.get_data()).get("message")
    await call.message.edit_text(await send_all(message_to_user=message_to_user, request=request, bot=bot))
    await call.answer()
    await state.clear()


@command_send_all_router.callback_query(Administrators.Mailing.confirmation, Text(text="cancel_send_all"))
@MessageLogging
async def cancel_send_all(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Действие было отменено.")
    await call.answer("Отменено")
