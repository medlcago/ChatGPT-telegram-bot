from bot.database.db import Database
from bot.utils import is_number


async def activate_subscription(*, user_id: str | int, request: Database):
    user_id = is_number(user_id)
    if not user_id:
        return "Аргумент не является идентификатором пользователя."

    user = await request.get_user(user_id=user_id)
    if user is None:
        return f"user_id <i>{user_id}</i> не найден в базе данных."

    if user.is_subscriber:
        return f"<b>{user.fullname}({user.user_id})</b> уже является подписчиком."

    if await request.update_user_subscription_status(user_id=user_id, is_subscriber=True):
        return f"<b>{user.fullname}({user.user_id})</b> получил подписку."
    return f"Произошла ошибка. <b>{user.fullname}({user.user_id})</b> не получил подписку."


async def deactivate_subscription(*, user_id: str | int, request: Database):
    user_id = is_number(user_id)
    if not user_id:
        return "Аргумент не является идентификатором пользователя."

    user = await request.get_user(user_id=user_id)
    if user is None:
        return f"user_id <i>{user_id}</i> не найден в базе данных."

    if user.is_subscriber:
        if await request.update_user_subscription_status(user_id=user_id, is_subscriber=False):
            return f"<b>{user.fullname}({user.user_id})</b> лишился подписки."
        return f"Произошла ошибка. <b>{user.fullname}({user.user_id})</b> не лишился подписки."
    return f"<b>{user.fullname}({user.user_id})</b> не является подписчиком."
