from aiogram.fsm.state import State, StatesGroup


class Mailing(StatesGroup):
    """
    Класс состояний для реализации рассылки.
    """
    message = State()
    confirmation = State()


class SendMessage(StatesGroup):
    """
    Класс состояний для отправки сообщений пользователю.
    """
    message = State()
    user_id = State()
    confirmation = State()


class AddAdmin(StatesGroup):
    """
    Класс состояний для добавления администратора.
    """
    user_id = State()


class RemoveAdmin(StatesGroup):
    """
    Класс состояний для удаления администратора.
    """
    user_id = State()


class Administrators:
    """
    Класс, объединяющий состояния для управления администраторами.
    """
    Mailing = Mailing
    SendMessage = SendMessage
    AddAdmin = AddAdmin
    RemoveAdmin = RemoveAdmin
