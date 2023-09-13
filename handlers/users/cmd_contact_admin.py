from aiogram import Router, F, types, flags, Bot
from aiogram.fsm.context import FSMContext

from data.config import Config
from keyboards.inline import get_confirmation_button, SendMessage, get_reply_to_user_button
from language.translator import LocalizedTranslator
from states.users import Users

command_contact_admin_router = Router()


@command_contact_admin_router.callback_query(F.data == "contact_admin")
@flags.skip
async def command_contact_admin(call: types.CallbackQuery, state: FSMContext, translator: LocalizedTranslator):
    await call.answer("Связь с администратором")
    await call.message.answer(translator.get("contact-admin-message"))
    await state.set_state(Users.ContactAdmin.message)


@command_contact_admin_router.message(F.content_type.in_({"text"}), Users.ContactAdmin.message)
@flags.skip
async def message_to_administrator(message: types.Message, state: FSMContext, translator: LocalizedTranslator):
    message_to_admin = message.text
    await state.update_data(message=message)
    await message.answer(translator.get("message-to-administrator-message", message=message_to_admin),
                         reply_markup=get_confirmation_button("creator").as_markup())
    await state.set_state(Users.ContactAdmin.confirmation)


@command_contact_admin_router.callback_query(Users.ContactAdmin.confirmation, SendMessage.filter((F.action == "confirmation") & (F.recipients == "creator")))
@flags.skip
async def confirmation_send_message(call: types.CallbackQuery, state: FSMContext, bot: Bot, config: Config):
    message: types.Message = (await state.get_data()).get("message")
    creator_user_id = config.creator_user_id
    message_id = message.message_id
    user_id = message.from_user.id
    message_to_admin = f"🔔 Новое сообщение от пользователя - <b>{user_id}</b>\n\n{message.text}"

    markup = get_reply_to_user_button(user_id, message_id).as_markup()

    await call.message.delete()
    await bot.send_message(chat_id=creator_user_id, text=message_to_admin, reply_markup=markup)
    await call.message.answer(f"Message sent successfully.",
                              reply_to_message_id=message_id)
    await call.answer("OK!")
    await state.clear()


@command_contact_admin_router.callback_query(Users.ContactAdmin.confirmation, SendMessage.filter((F.action == "cancel") & (F.recipients == "creator")))
@flags.skip
async def cancel_send_message(call: types.CallbackQuery, state: FSMContext, translator: LocalizedTranslator):
    await state.clear()
    await call.message.edit_text(translator.get("cancel-message"))
    await call.answer()
