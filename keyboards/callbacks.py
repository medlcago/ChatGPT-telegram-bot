from enum import Enum

from aiogram.filters.callback_data import CallbackData


class ComeBack(CallbackData, prefix="back"):
    back: str


class SendMessageAction(str, Enum):
    confirmation = "confirmation"
    cancel = "cancel"


class SendMessage(CallbackData, prefix="send"):
    action: SendMessageAction
    recipients: str


class ReplyUserAction(str, Enum):
    reply_to_user = "reply_to_user"
    dont_reply_to_user = "dont_reply_to_user"


class ReplyUser(CallbackData, prefix="reply"):
    action: ReplyUserAction
    user_id: int
    message_id: int


class Model(CallbackData, prefix="model"):
    model: str
