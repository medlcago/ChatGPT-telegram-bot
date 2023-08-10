from aiogram.fsm.state import State, StatesGroup


class PromocodeActivation(StatesGroup):
    """
    Класс состояний для активации промокода.
    """
    promo_code = State()


class Users:
    """
    Класс, объединяющий состояния для работы с пользователями.
    """
    PromocodeActivation = PromocodeActivation
