from typing import Callable, Any, Awaitable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.language.translator import Translator


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]) -> Any:
        new_data = data.copy()
        translator: Translator = new_data["translator"]
        new_data["translator"] = translator(language=event.from_user.language_code)
        return await handler(event, new_data)
