import random
import string

from aiogram.utils.markdown import hcode

from database.db import Database
from exceptions import ActivationError


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


async def validate_and_add_promocode(*, activations_count: str, request: Database):
    """
    Проверяет промокод на валидность, после чего добавляет его в базу данных.
    """
    if activations_count.isnumeric() and int(activations_count) > 0:
        promocode = generate_promocode()
        activations_count = int(activations_count)
        if await request.add_promocode(promocode=promocode, activations_count=activations_count):
            return f"Сгенерированный промокод: <code>{promocode}</code>\nКол-во активаций: {activations_count}"
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


async def activate_promocode(*, promocode, user_id, request: Database):
    """
    Проверяет промокод на валидность, после чего происходит его активация.
    """
    if await request.check_user_subscription_status(user_id=user_id):
        return "Промокод не был активирован, т.к вы уже являетесь подписчиком."
    if await request.check_promocode(promocode):
        if await request.update_user_subscription_status(user_id=user_id, is_subscriber=True):
            return f"Промокод {hcode(promocode)} был успешно активирован ✅"
        raise ActivationError("Произошла ошибка при активации промокода. Пожалуйста, свяжитесь с администратором.")
    return f"Промокод {hcode(promocode)} не является действительным."
