import logging

from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import ChatMemberUpdated

from bot.database.db import Database

user_activity_status_router = Router()


@user_activity_status_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated, request: Database):
    logging.info(f"Пользователь {event.from_user.username}[{event.from_user.id}] заблокировал бота.")
    await request.update_user_active_status(user_id=event.from_user.id, is_active=False)


@user_activity_status_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def process_user_unblocked_bot(event: ChatMemberUpdated, request: Database):
    logging.info(f"Пользователь {event.from_user.username}[{event.from_user.id}] разблокировал бота.")
    await request.update_user_active_status(user_id=event.from_user.id, is_active=True)
