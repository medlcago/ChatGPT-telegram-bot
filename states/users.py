from aiogram.fsm.state import State, StatesGroup


class PromocodeActivation(StatesGroup):
    """
    Класс состояний для активации промокода.
    """
    promocode = State()


class Users:
    """
    Класс, объединяющий состояния для работы с пользователями.
    """
    PromocodeActivation = PromocodeActivation
