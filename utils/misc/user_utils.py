from database.db import Database
from utils import is_number


async def suspend_user(*, user_id: str | int, request: Database):
    user_id = is_number(user_id)
    if not user_id:
        return "Аргумент не является идентификатором пользователя."

    user = await request.get_user(user_id=user_id)
    if user is None:
        return f"user_id <i>{user_id}</i> не найден в базе данных."

    if user.is_admin:
        return f"Нельзя заблокировать администратора <b>{user.fullname}({user.user_id})</b>."

    if user.is_blocked:
        return f"<b>{user.fullname}({user.user_id})</b> уже заблокирован."

    if await request.update_user_block_status(user_id=user_id, is_blocked=True):
        return f"<b>{user.fullname}({user.user_id})</b> был заблокирован."
    return f"Произошла ошибка. <b>{user.fullname}({user.user_id})</b> не был заблокирован."


async def unsuspend_user(*, user_id: str | int, request: Database):
    user_id = is_number(user_id)
    if not user_id:
        return "Аргумент не является идентификатором пользователя."

    user = await request.get_user(user_id=user_id)
    if user is None:
        return f"user_id <i>{user_id}</i> не найден в базе данных."

    if user.is_blocked:
        if await request.update_user_block_status(user_id=user_id, is_blocked=False):
            return f"<b>{user.fullname}({user.user_id})</b> был разблокирован."
        return f"Произошла ошибка. <b>{user.fullname}({user.user_id})</b> не был разблокирован."
    return f"<b>{user.fullname}({user.user_id})</b> не заблокирован."
