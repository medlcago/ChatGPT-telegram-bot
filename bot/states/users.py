from aiogram.fsm.state import State, StatesGroup


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
    ContactAdmin = ContactAdmin
