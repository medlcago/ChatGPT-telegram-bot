from database.db import Database


async def suspend_user(*, user_id: str, request: Database):
    if user_id and user_id.isnumeric():
        user_id = int(user_id)
        user = await request.get_user(user_id=user_id)
        if user:
            if user.is_admin:
                return f"Нельзя заблокировать администратора <b>{user.fullname}({user.user_id})</b>."
            if user.is_blocked:
                return f"<b>{user.fullname}({user.user_id})</b> уже заблокирован."
            if await request.update_user_block_status(user_id=user_id, is_blocked=True):
                return f"<b>{user.fullname}({user.user_id})</b> был заблокирован."
            return f"Произошла ошибка. <b>{user.fullname}({user.user_id})</b> не был заблокирован."
        return f"user_id <i>{user_id}</i> не найден в базе данных."
    return "Аргумент не является идентификатором пользователя."


async def unsuspend_user(*, user_id: str, request: Database):
    if user_id and user_id.isnumeric():
        user_id = int(user_id)
        user = await request.get_user(user_id=user_id)
        if user:
            if user.is_blocked:
                if await request.update_user_block_status(user_id=user_id, is_blocked=False):
                    return f"<b>{user.fullname}({user.user_id})</b> был разблокирован."
                return f"Произошла ошибка. <b>{user.fullname}({user.user_id})</b> не был разблокирован."
            return f"<b>{user.fullname}({user.user_id})</b> не заблокирован."
        return f"user_id <i>{user_id}</i> не найден в базе данных."
    return "Аргумент не является идентификатором пользователя."
