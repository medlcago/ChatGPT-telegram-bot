import random
import string


async def generate_promocode():
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
