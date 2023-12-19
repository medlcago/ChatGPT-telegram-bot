from functools import wraps

from aiogram.filters import CommandObject
from aiogram.types import Message

from keyboards.inline_main import close_button


def check_command_args(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        command: CommandObject | None = kwargs.get("command", None)
        if command is None:
            raise ValueError("Command argument missing.")
        if not command.args:
            await message.reply(
                text=f"The command <b><i>{command.prefix + command.command}</i></b> was empty, the request could not be completed.",
                reply_markup=close_button
            )
        else:
            await func(message, *args, **kwargs)

    return wrapper
