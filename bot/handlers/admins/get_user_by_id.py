from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot.database.db import Database
from bot.filters import IsAdmin
from bot.keyboards.inline_main import close_button
from bot.states.admins import Administrators
from bot.utils.misc import info_about_user

get_user_by_id_router = Router()


@get_user_by_id_router.callback_query(F.data == "get_user_by_id", IsAdmin())
async def get_user_by_id(call: CallbackQuery, state: FSMContext):
    sent_message = await call.message.answer(
        text="Вы хотите получить информацию о пользователе.\nПожалуйста, введите его ID"
    )
    await state.set_state(Administrators.UserInfo.user_id)
    await state.update_data(sent_message_id=sent_message.message_id)
    await call.answer("OK!")


@get_user_by_id_router.message(Administrators.UserInfo.user_id, F.text.regexp(r"^(\d+)$"))
async def get_user_by_id(message: Message, state: FSMContext, request: Database):
    data = await state.get_data()
    sent_message_id = data.get("sent_message_id")
    user_id = int(message.text)
    user = await request.get_user(user_id=user_id)
    if user:
        message_text = info_about_user(user=user)
        await message.reply(
            text=message_text,
            reply_markup=close_button
        )
    else:
        await message.reply(
            text=f"Не удалось получить информацию по ID <code>{user_id}</code>",
            reply_markup=close_button
        )

    await message.bot.delete_message(chat_id=message.chat.id, message_id=sent_message_id)
    await state.clear()
