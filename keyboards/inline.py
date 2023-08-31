from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

btn_my_profile = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="👤 Мой профиль", callback_data="my_profile")
    ]
])

btn_cmd_admin = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Рассылка", callback_data="send_all"),
        InlineKeyboardButton(text="Статистика", callback_data="statistics")
    ],
    [
        InlineKeyboardButton(text="Сообщение пользователю", callback_data="send_message")
    ],
    [
        InlineKeyboardButton(text="Cписок пользователей", callback_data="user_list"),
        InlineKeyboardButton(text="Cписок администраторов", callback_data="admin_list")
    ],
    [
        InlineKeyboardButton(text="Добавить администратора", callback_data="add_admin"),
        InlineKeyboardButton(text="Удалить администратора", callback_data="remove_admin")
    ],
    [
        InlineKeyboardButton(text="Выдать подписку", callback_data="grant_sub"),
        InlineKeyboardButton(text="Забрать подписку", callback_data="remove_sub")
    ],
    [
        InlineKeyboardButton(text="Заблокировать пользователя", callback_data="block_user"),
        InlineKeyboardButton(text="Разблокировать пользователя", callback_data="unblock_user")
    ],
    [
        InlineKeyboardButton(text="Создать промокод", callback_data="create_promocode"),
        InlineKeyboardButton(text="Деактивировать промокод", callback_data="deactivate_promocode")
    ],
    [
        InlineKeyboardButton(text="Информация о сервере", callback_data="server_info")
    ],
    [

        InlineKeyboardButton(text="❌ Закрыть панель", callback_data="close_admin_panel")
    ]
])

btn_contact_admin = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✉️ Связаться с администратором", callback_data="contact_admin")
    ]
])

btn_promocode_activation = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Активировать промокод", callback_data="activate_promocode")
    ]
])


class ComeBack(CallbackData, prefix="back"):
    back: str


def get_keyboard_back(back: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад", callback_data=ComeBack(back=back))
    return builder


def get_keyboard_activate_subscription() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.attach(InlineKeyboardBuilder.from_markup(btn_contact_admin))
    builder.attach(InlineKeyboardBuilder.from_markup(btn_promocode_activation))
    builder.adjust(1, 1)
    return builder


class SendMessageAction(str, Enum):
    confirmation = "confirmation"
    cancel = "cancel"


class SendMessage(CallbackData, prefix="send"):
    action: SendMessageAction
    recipients: str


def get_keyboard_message(recipients: str) -> InlineKeyboardBuilder:
    if recipients not in ("one", "all", "creator"):
        raise ValueError("recipients must be one of: 'one', 'all', 'creator'")
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить",
                   callback_data=SendMessage(action=SendMessageAction.confirmation, recipients=recipients))
    builder.button(text="❌ Отмена",
                   callback_data=SendMessage(action=SendMessageAction.cancel, recipients=recipients))
    builder.adjust(1, 1)
    return builder


class ReplyUserAction(str, Enum):
    reply_to_user = "reply_to_user"
    dont_reply_to_user = "dont_reply_to_user"


class ReplyUser(CallbackData, prefix="reply"):
    action: ReplyUserAction
    user_id: int
    message_id: int


def get_keyboard_reply_to_user(user_id: int, message_id: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="✉️ Ответить", callback_data=ReplyUser(action=ReplyUserAction.reply_to_user, user_id=user_id,
                                                               message_id=message_id))
    builder.button(text="❌ Оставить без ответа",
                   callback_data=ReplyUser(action=ReplyUserAction.dont_reply_to_user, user_id=user_id,
                                           message_id=message_id))
    builder.adjust(1, 1)
    return builder


class Model(CallbackData, prefix="model"):
    model: str


def get_models_list(models: list) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for model in models:
        builder.button(text=model, callback_data=Model(model=model))
    builder.adjust(2, 2)
    return builder
