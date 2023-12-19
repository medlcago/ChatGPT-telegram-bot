from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_inline_keyboard(width: int,
                           *args: str,
                           last_btn: dict | None = None,
                           **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=button
            ))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    kb_builder.row(*buttons, width=width)
    if last_btn:
        for button, text in last_btn.items():
            kb_builder.row(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))
    return kb_builder.as_markup()
