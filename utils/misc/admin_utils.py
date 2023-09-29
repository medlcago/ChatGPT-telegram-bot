from database.db import Database


async def assign_admin_rights(*, user_id: str, request: Database):
    if not user_id or not user_id.isnumeric():
        return "Аргумент не является идентификатором пользователя."

    user_id = int(user_id)

    user = await request.get_user(user_id=user_id)
    if user is None:
        return f"user_id <i>{user_id}</i> не найден в базе данных."

    if user.is_admin:
        return f"<b>{user.fullname}({user.user_id})</b> уже является администратором."

    if await request.update_admin_rights_status(user_id=user_id, is_admin=True):
        return f"<b>{user.fullname}({user.user_id})</b> назначен администратором."

    return f"<b>{user.fullname}({user.user_id})</b> не назначен администратором."


async def revoke_admin_rights(*, user_id: str, from_user_id: int, request: Database):
    if not user_id or not user_id.isnumeric():
        return "Аргумент не является идентификатором пользователя."

    user_id = int(user_id)

    user = await request.get_user(user_id=user_id)
    if user is None:
        return f"user_id <i>{user_id}</i> не найден в базе данных."

    if user.is_admin:
        if user.user_id != from_user_id:
            if await request.update_admin_rights_status(user_id=user_id, is_admin=False):
                return f"<b>{user.fullname}({user.user_id})</b> удален из администраторов."
            return f"<b>{user.fullname}({user.user_id})</b> не удален из администраторов."
        return "Нельзя удалить самого себя!"

    return f"<b>{user.fullname}({user.user_id})</b> не является администратором."


async def get_admin_list(*, request: Database):
    admins = await request.get_admins()
    if admins:
        data = (f"{admin.fullname}({admin.user_id})" for admin in admins)
        return '<b>Администраторы бота:</b>\n' + "\n".join(data)
    return "Администраторы отсутствуют."


async def get_user_list(*, request: Database):
    users = await request.get_all_users()
    if users:
        data = (f"{user.fullname}({user.user_id})" for user in users)
        return '<b>Пользователи бота:</b>\n' + "\n".join(data)
    return "Пользователи отсутствуют."
