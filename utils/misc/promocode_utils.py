import random
import string

from database.db import Database
from exceptions import ActivationError
from utils import is_number


def generate_promocode():
    """
    Генерирует промокод по шаблону r^PROMO-[A-Z]{3}-\d{3}-[A-Z]{3}$
    """
    letters = random.sample(string.ascii_uppercase, 3)
    prefix = "".join(letters)

    number = random.randint(100, 999)

    letters = random.sample(string.ascii_uppercase, 3)
    suffix = "".join(letters)

    promocode = f"PROMO-{prefix}-{number}-{suffix}"
    return promocode


async def validate_and_add_promocode(*, activations_count: str | int, request: Database):
    """
    Проверяет промокод на валидность, после чего добавляет его в базу данных.
    """
    activations_count = is_number(activations_count)
    if activations_count and activations_count > 0:
        promocode = generate_promocode()
        if await request.add_promocode(promocode=promocode, activations_count=activations_count):
            return f"Сгенерированный промокод: <code>{promocode}</code>\n\nКол-во активаций: <b>{activations_count}</b>"
        return "Произошла ошибка при создании промокода."
    return "Аргумент должен быть целым положительным числом."


async def deactivate_promocode(*, promocode: str, request: Database):
    """
    Деактивирует промокод и удаляет его из базы данных.
    """
    if await request.promocode_exists(promocode=promocode):
        if await request.delete_promocode(promocode=promocode):
            return f"Промокод <code>{promocode}</code> был деактивирован."
        return f"Промокод <code>{promocode}</code> не был деактивирован."
    return f"Промокод <code>{promocode}</code> не существует."


async def activate_promocode(*, promocode: str, user_id: str | int, request: Database):
    """
    Проверяет промокод на валидность, после чего происходит его активация.
    """
    if await request.check_user_subscription_status(user_id=user_id):
        return "Промокод не был активирован, т.к вы уже являетесь подписчиком."
    if await request.check_promocode(promocode):
        if await request.update_user_subscription_status(user_id=user_id, is_subscriber=True):
            return f"Промокод <code>{promocode}</code> был успешно активирован ✅"
        raise ActivationError("Произошла ошибка при активации промокода. Пожалуйста, свяжитесь с администратором.")
    return f"Промокод <code>{promocode}</code> не является действительным."
