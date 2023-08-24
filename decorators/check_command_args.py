from functools import wraps

from aiogram.filters import CommandObject
from aiogram.types import Message


def check_command_args(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        command: CommandObject = kwargs.get("command", None)
        if command is None:
            raise ValueError("Command argument missing.")
        if not command.args:
            if message.from_user.language_code == "ru":
                await message.reply(
                    f"Команда <b><i>{command.prefix + command.command}</i></b> оказалась пустой, запрос не может быть выполнен.")
            else:
                await message.reply(
                    f"The command <b><i>{command.prefix + command.command}</i></b> was empty, the request could not be completed.")
        else:
            await func(message, *args, **kwargs)

    return wrapper
