from bot.database.models import User


def info_about_user(user: User) -> str:
    user_info = f"""<b>ID:</b> <code>{user.user_id}</code>
<b>fullname:</b> {user.fullname}
<b>Админ:</b> {('Нет', 'Да')[user.is_admin]}
<b>Заблокирован:</b> {('Нет', 'Да')[user.is_blocked]}
<b>Активен:</b> {('Нет', 'Да')[user.is_active]}
<b>Подписчик:</b> {('Нет', 'Да')[user.is_subscriber]}
"""
    return user_info
