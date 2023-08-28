from aiogram import Router, F, types, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from filters import IsAdmin
from keyboards.inline import ReplyUser
from states.admins import Administrators

command_contact_admin_router = Router()


@command_contact_admin_router.callback_query(ReplyUser.filter(F.action == "dont_reply_to_user"), IsAdmin())
async def dont_reply_to_user(call: types.CallbackQuery, callback_data: ReplyUser, bot: Bot):
    user_id = callback_data.user_id
    message_id = callback_data.message_id
    try:
        await bot.send_message(chat_id=user_id, text="""🔔 Вам ответил администратор\n
Сообщение:\nАдминистратор решил оставить ваше сообщение без ответа.""", reply_to_message_id=message_id)
        await call.message.edit_text(f"""Вы успешно ответили пользователю - <b>{user_id}</b>\n
Ваш ответ:\nВы решили оставить сообщение без ответа.""")
    except TelegramBadRequest:
        await call.message.edit_text(
            f"Сообщение не было отправлено, так как пользователь <b>{user_id}</b> удалил свое обращение.")
    finally:
        await call.answer("OK!")


@command_contact_admin_router.callback_query(ReplyUser.filter(F.action == "reply_to_user"), IsAdmin())
async def reply_to_user(call: types.CallbackQuery, state: FSMContext, callback_data: ReplyUser):
    await call.answer()
    user_id = callback_data.user_id
    message_id = callback_data.message_id
    current_message = call.message
    sent_message = await call.message.reply(f"Введите ответ на сообщение пользователю <b>{user_id}</b>")
    await state.set_state(Administrators.ReplyUser.message)
    await state.update_data(user_id=user_id, sent_message=sent_message, current_message=current_message,
                            message_id=message_id)


@command_contact_admin_router.message(F.content_type.in_({"text"}), Administrators.ReplyUser.message)
async def message_to_user(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id = data.get("user_id")
    message_id = data.get("message_id")
    sent_message = data.get("sent_message")
    current_message = data.get("current_message")
    try:
        await bot.send_message(chat_id=user_id, text=f"""🔔 Вам ответил администратор\n
Сообщение:\n{message.text}""", reply_to_message_id=message_id)
        await message.reply(f"""Вы успешно ответили пользователю - <b>{user_id}</b>\n
Ваш ответ:\n{message.text}""")
    except TelegramBadRequest:
        await message.reply(
            f"Сообщение не было отправлено, так как пользователь <b>{user_id}</b> удалил свое обращение.")
    finally:
        await current_message.delete()
        await sent_message.delete()
        await state.clear()