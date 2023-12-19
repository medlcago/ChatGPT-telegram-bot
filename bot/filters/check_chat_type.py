from aiogram.filters import Filter
from aiogram.types import Message


class ChatTypeFilter(Filter):
    def __init__(self, is_group: bool, chat_id: int = None) -> None:
        self.is_group = is_group
        self.chat_id = chat_id

    async def __call__(self, message: Message) -> bool:
        if self.chat_id:
            return (message.chat.type != 'private' if self.is_group else message.chat.type == 'private') and (message.chat.id == self.chat_id)
        return message.chat.type != 'private' if self.is_group else message.chat.type == 'private'