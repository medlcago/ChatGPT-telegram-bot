from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_cmd_admin = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Рассылка", callback_data="send_all")
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
        InlineKeyboardButton(text="Информация о сервере", callback_data="server_info")
    ],
    [
        InlineKeyboardButton(text="❌ Закрыть панель", callback_data="close_panel")
    ]
])

btn_send_all = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Подтвердить", callback_data="confirmation_send_all")
    ],
    [
        InlineKeyboardButton(text="Отмена", callback_data="cancel_send_all")
    ]
])

btn_send_message = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Подтвердить", callback_data="confirmation_send_message")
    ],
    [
        InlineKeyboardButton(text="Отмена", callback_data="cancel_send_message")
    ]
])
