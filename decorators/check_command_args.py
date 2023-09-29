from functools import wraps

from aiogram.filters import CommandObject
from aiogram.types import Message

from language.translator import LocalizedTranslator


def check_command_args(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        command: CommandObject = kwargs.get("command", None)
        translator: LocalizedTranslator = kwargs.get("translator")
        if command is None:
            raise ValueError("Command argument missing.")
        if translator is None:
            return await message.answer(
                f"The command <b><i>{command.prefix + command.command}</i></b> was empty, the request could not be completed.")
        if not command.args:
            await message.reply(translator.get("empty-command-message", command=command.prefix + command.command))
        else:
            await func(message, *args, **kwargs)

    return wrapper
