from aiogram.fsm.state import State, StatesGroup


class PromocodeActivation(StatesGroup):
    """
    Класс состояний для активации промокода.
    """
    promocode = State()


class ContactAdmin(StatesGroup):
    """
    Класс состояний для связи пользователя с администратором.
    """
    message = State()
    confirmation = State()


class Users:
    """
    Класс, объединяющий состояния для работы с пользователями.
    """
    PromocodeActivation = PromocodeActivation
    ContactAdmin = ContactAdmin
