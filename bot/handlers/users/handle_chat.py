from aiogram import Bot, Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery

from config import Config
from bot.database.db import Database
from bot.decorators import CheckTimeLimits, MessageLogging
from bot.exceptions import RequestProcessingError
from bot.filters import ChatTypeFilter
from bot.keyboards.callbacks import Model
from bot.keyboards.inline_main import get_model_list_button, close_button
from bot.keyboards.inline_utils import create_inline_keyboard
from bot.language.translator import LocalizedTranslator
from bot.utils.neural_networks import ChatBot

handle_chat_router = Router()


@handle_chat_router.message(Command(commands="switch"), ChatTypeFilter(is_group=False))
@MessageLogging
async def switch_chat_type(message: Message, config: Config, translator: LocalizedTranslator):
    available_models = config.models.available_models
    list_of_models = get_model_list_button(available_models, add_close_button=True)
    await message.answer(translator.get("model-selection-message"), reply_markup=list_of_models)


@handle_chat_router.callback_query(Model.filter())
@MessageLogging
async def switch_chat_type(call: CallbackQuery, callback_data: Model, request: Database,
                           translator: LocalizedTranslator):
    await request.clear_user_dialog_history(user_id=call.from_user.id)
    model = callback_data.model
    current_model = await request.update_user_chat_type(user_id=call.from_user.id, chat_type=model)
    await call.message.edit_text(translator.get("switch-chat-type-message", current_model=current_model))
    await call.answer(current_model)


@handle_chat_router.message(Command(commands=["switch"]), ChatTypeFilter(is_group=False))
@MessageLogging
async def switch_chat_type_non_premium(message: Message, command: CommandObject, translator: LocalizedTranslator):
    await message.reply(
        text=translator.get("non-premium-message", command=command.prefix + command.command),
        reply_markup=create_inline_keyboard(
            width=1,
            activate_promocode="✅ Активировать промокод",
            close="❌ Закрыть"
        )
    )


@handle_chat_router.message(Command(commands="clear"), ChatTypeFilter(is_group=False))
@MessageLogging
async def clear_history(message: Message, request: Database, translator: LocalizedTranslator):
    await request.clear_user_dialog_history(user_id=message.from_user.id)
    await message.reply(translator.get("clear-dialog-history-message"))


@handle_chat_router.message(ChatTypeFilter(is_group=False), F.content_type.in_({'text'}))
@MessageLogging
@CheckTimeLimits
async def handle_chat(message: Message, request: Database, bot: Bot, config: Config, translator: LocalizedTranslator):
    user_id = message.from_user.id
    prompt = message.text
    current_model = await request.get_user_chat_type(user_id=user_id)
    available_models = config.models.available_models

    if current_model and current_model in available_models:
        old_messages = await request.get_user_dialog(user_id=user_id)
        if len(old_messages) >= config.openai.context_limit:
            await request.clear_user_dialog_history(user_id=user_id)
            await message.answer(translator.get("clear-dialog-history-message"))

        old_messages = "\n".join(old_messages)
        gpt_bot = ChatBot(api_key=config.openai.api_key, api_base=config.openai.api_base, model=current_model)
        sent_message = await message.reply(translator.get("processing-request-message"))

        try:
            bot_response = await gpt_bot.chat(prompt=prompt, history=old_messages)
            await bot.edit_message_text(
                chat_id=sent_message.chat.id,
                message_id=sent_message.message_id,
                text=bot_response,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=close_button
            )
            await request.add_message_to_dialog(
                user_id=user_id,
                messages=[prompt, bot_response]
            )
        except (TelegramBadRequest, RequestProcessingError) as error:
            await bot.edit_message_text(
                chat_id=sent_message.chat.id,
                message_id=sent_message.message_id,
                text=str(error),
                reply_markup=close_button
            )
    else:
        await message.reply(
            text=translator.get("model-not-found", model=current_model),
            reply_markup=close_button
        )


@handle_chat_router.message(ChatTypeFilter(is_group=False))
@MessageLogging
async def handle_non_text_message(message: Message, translator: LocalizedTranslator):
    await message.reply(
        text=translator.get("non-text-message"),
        reply_markup=close_button
    )
