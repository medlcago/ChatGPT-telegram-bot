from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.filters import CommandObject
from aiogram.types import Message

from bot.database.db import Database
from bot.keyboards.inline_main import close_button
from bot.utils import deeplink_decode
from config import Config


class UserRegistrationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        registration = get_flag(data, "registration")
        if registration is None:
            return await handler(event, data)

        command: CommandObject = data.get("command")
        request: Database = data.get("request")
        config: Config = data.get("config")

        referrer_id = deeplink_decode(payload=command.args)
        user_id = event.from_user.id
        fullname = event.from_user.full_name
        username = event.from_user.username

        if await request.get_user(user_id=user_id) is None:
            if referrer_id and user_id != referrer_id and await request.get_user(user_id=referrer_id):
                await request.add_user(user_id=user_id, fullname=fullname, referrer=referrer_id)
                await event.bot.send_message(chat_id=referrer_id,
                                             text=f"<b>Новый реферал — <code>{fullname}[{user_id}]</code>!</b>"
                                             )
            else:
                await request.add_user(user_id=user_id, fullname=fullname)
            await event.bot.send_message(
                chat_id=config.creator_user_id,
                text=f"<b>Новый пользователь!</b>\n\n"
                     f"<b>username:</b> {'@' + username if username else '❌'}\n"
                     f"<b>user_id:</b> <code>{user_id}</code>",
                reply_markup=close_button
            )
        return await handler(event, data)
