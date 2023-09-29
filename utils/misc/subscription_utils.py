from database.db import Database


async def activate_subscription(*, user_id: str, request: Database):
    if user_id and user_id.isnumeric():
        user_id = int(user_id)
        user = await request.get_user(user_id=user_id)
        if user:
            if user.is_subscriber:
                return f"<b>{user.fullname}({user.user_id})</b> уже является подписчиком."
            if await request.update_user_subscription_status(user_id=user_id, is_subscriber=True):
                return f"<b>{user.fullname}({user.user_id})</b> получил подписку."
            return f"Произошла ошибка. <b>{user.fullname}({user.user_id})</b> не получил подписку."
        return f"user_id <i>{user_id}</i> не найден в базе данных."
    return "Аргумент не является идентификатором пользователя."


async def deactivate_subscription(*, user_id: str, request: Database):
    if user_id and user_id.isnumeric():
        user_id = int(user_id)
        user = await request.get_user(user_id=user_id)
        if user:
            if user.is_subscriber:
                if await request.update_user_subscription_status(user_id=user_id, is_subscriber=False):
                    return f"<b>{user.fullname}({user.user_id})</b> лишился подписки."
                return f"Произошла ошибка. <b>{user.fullname}({user.user_id})</b> не лишился подписки."
            return f"<b>{user.fullname}({user.user_id})</b> не является подписчиком."
        return f"user_id <i>{user_id}</i> не найден в базе данных."
    return "Аргумент не является идентификатором пользователя."
