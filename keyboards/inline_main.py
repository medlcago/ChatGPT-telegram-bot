from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.callbacks import ComeBack, SendMessageAction, SendMessage, ReplyUserAction, ReplyUser, Model
from keyboards.inline_utils import create_inline_keyboard

my_profile_and_affiliate_program_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="👤 Мой профиль", callback_data="my_profile")
    ],
    [
        InlineKeyboardButton(text="🤝 Партнерская программа", callback_data="affiliate_program")
    ]
])

admin_panel_buttons = InlineKeyboardMarkup(inline_keyboard=[
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

        InlineKeyboardButton(text="❌ Закрыть панель", callback_data="close")
    ]
])

contact_admin_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✉️ Связаться с администратором", callback_data="contact_admin")
    ]
])

promocode_activation_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Активировать промокод", callback_data="activate_promocode")
    ]
])


def get_back_button(back: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад", callback_data=ComeBack(back=back))
    return builder


def get_activate_subscription_button() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.attach(InlineKeyboardBuilder.from_markup(contact_admin_button))
    builder.attach(InlineKeyboardBuilder.from_markup(promocode_activation_button))
    builder.adjust(1, 1)
    return builder


def get_confirmation_button(recipients: str) -> InlineKeyboardBuilder:
    if recipients not in ("one", "all", "creator"):
        raise ValueError("recipients must be one of: 'one', 'all', 'creator'")
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить",
                   callback_data=SendMessage(action=SendMessageAction.confirmation, recipients=recipients))
    builder.button(text="❌ Отмена",
                   callback_data=SendMessage(action=SendMessageAction.cancel, recipients=recipients))
    builder.adjust(1, 1)
    return builder


def get_reply_to_user_button(user_id: int, message_id: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="✉️ Ответить", callback_data=ReplyUser(action=ReplyUserAction.reply_to_user, user_id=user_id,
                                                               message_id=message_id))
    builder.button(text="❌ Оставить без ответа",
                   callback_data=ReplyUser(action=ReplyUserAction.dont_reply_to_user, user_id=user_id,
                                           message_id=message_id))
    builder.adjust(1, 1)
    return builder


def get_model_list_button(models: list, add_close_button: bool = False) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for model in models:
        builder.button(text=model, callback_data=Model(model=model))
    builder.adjust(2, 2)
    if add_close_button:
        builder.row(InlineKeyboardButton(text="❌ Закрыть", callback_data="close"))
    return builder
