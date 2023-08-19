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


class GrantSubscription(StatesGroup):
    """
    Класс состояний для выдачи подписки.
    """
    user_id = State()


class RemoveSubscription(StatesGroup):
    """
    Класс состояний для удаления подписки.
    """
    user_id = State()


class BlockUser(StatesGroup):
    """
    Класс состояний для блокировки пользователя.
    """
    user_id = State()


class UnblockUser(StatesGroup):
    """
    Класс состояний для разблокировки пользователя.
    """
    user_id = State()


class CreatePromocode(StatesGroup):
    """
    Класс состояний для создания промокода.
    """
    promocode = State()
    activations_count = State()


class Administrators:
    """
    Класс, объединяющий состояния для работы администраторов.
    """
    Mailing = Mailing
    SendMessage = SendMessage
    AddAdmin = AddAdmin
    RemoveAdmin = RemoveAdmin
    GrantSubscription = GrantSubscription
    RemoveSubscription = RemoveSubscription
    BlockUser = BlockUser
    UnblockUser = UnblockUser
    CreatePromocode = CreatePromocode
