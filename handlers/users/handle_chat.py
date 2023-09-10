from aiogram import Bot, Router, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject

from data.config import Config
from database.db import Database
from decorators import CheckTimeLimits, MessageLogging
from exceptions import RequestProcessingError
from filters import ChatTypeFilter, IsAdmin, IsSubscription
from keyboards.inline import btn_promocode_activation, get_models_list, Model
from utils.neural_networks import ChatBot

handle_chat_router = Router()


@handle_chat_router.message(Command(commands=["switch"]), ChatTypeFilter(is_group=False), IsSubscription())
@handle_chat_router.message(Command(commands=["switch"]), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def switch_chat_type(message: types.Message, config: Config):
    available_models = config.models.available_models
    await message.answer("Выберите модель ниже 👇", reply_markup=get_models_list(available_models).as_markup())


@handle_chat_router.callback_query(Model.filter())
@MessageLogging
async def switch_chat_type(call: types.CallbackQuery, callback_data: Model, request: Database):
    await request.clear_user_dialog_history(user_id=call.from_user.id)
    model = callback_data.model
    current_model = await request.update_user_chat_type(user_id=call.from_user.id, chat_type=model)
    await call.message.edit_text(f"Текущая модель: <b><i>{current_model}</i></b>\n\nИстория сообщений была очищена.")
    await call.answer(current_model)


@handle_chat_router.message(Command(commands=["switch"]), ChatTypeFilter(is_group=False))
@MessageLogging
async def switch_chat_type_non_premium(message: types.Message, command: CommandObject):
    if message.from_user.language_code == "ru":
        await message.reply(
            f"Команда <b><i>{command.prefix + command.command}</i></b> доступна только premium пользователям.",
            reply_markup=btn_promocode_activation)
    else:
        await message.reply(
            f"The command <b><i>{command.prefix + command.command}</i></b> is only available to premium users.",
            reply_markup=btn_promocode_activation)


@handle_chat_router.message(Command(commands=["clear"]), ChatTypeFilter(is_group=False))
async def clear_history(message: types.Message, request: Database):
    await request.clear_user_dialog_history(user_id=message.from_user.id)
    await message.reply("История сообщений была очищена.")


@handle_chat_router.message(ChatTypeFilter(is_group=False), F.content_type.in_({'text'}))
@MessageLogging
@CheckTimeLimits
async def handle_chat(message: types.Message, request: Database, bot: Bot, config: Config):
    user_id = message.from_user.id
    prompt = message.text
    model = await request.get_user_chat_type(user_id=user_id)
    available_models = config.models.available_models

    if model and model in available_models:
        old_messages = await request.get_user_dialog(user_id=user_id)
        if len(old_messages) >= config.openai.context_limit:
            await request.clear_user_dialog_history(user_id=user_id)
            await message.answer("История сообщений была автоматически очищена.")

        old_messages = "\n".join(old_messages)
        gpt_bot = ChatBot(api_key=config.openai.api_key, api_base=config.openai.api_base, model=model)
        sent_message = await message.reply("Обработка запроса, ожидайте")
        try:
            bot_response = await gpt_bot.chat(prompt=prompt, history=old_messages)
            await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                        text=bot_response,
                                        parse_mode="markdown", disable_web_page_preview=True)
            await request.add_message_to_dialog(user_id=user_id,
                                                messages=[prompt, bot_response])
        except (TelegramBadRequest, RequestProcessingError) as error:
            await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                        text=str(error))
    else:
        await message.reply("Ошибка: модель не найдена.")


@handle_chat_router.message(ChatTypeFilter(is_group=False))
@MessageLogging
async def handle_non_text_message(message: types.Message):
    if message.from_user.language_code == "ru":
        await message.reply(
            "К сожалению, бот умеет работать только с текстом. Пожалуйста, повторите свой запрос в текстовом виде.")
    else:
        await message.reply("Unfortunately, the bot can only work with text. Please, repeat your request in text form.")
