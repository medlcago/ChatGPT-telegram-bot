import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from data.config import BOT_TOKEN
from handlers import admins, general, groups, users
from middlewares import (
    DatabaseMiddleware,
    BlockMiddleware,
    DebugMiddleware,
    SubscribersMiddleware)
from settings.database.setup import create_db_session
from utils.misc import set_commands


def middleware_registration(dp: Dispatcher, session_pool=None):
    if session_pool:
        dp.message.outer_middleware(DatabaseMiddleware(session_pool))
        dp.callback_query.outer_middleware(DatabaseMiddleware(session_pool))

    dp.message.middleware.register(BlockMiddleware())
    dp.callback_query.middleware.register(BlockMiddleware())

    dp.message.middleware.register(DebugMiddleware())
    dp.callback_query.middleware.register(DebugMiddleware())

    dp.message.middleware.register(SubscribersMiddleware())
    dp.callback_query.middleware.register(SubscribersMiddleware())


def routers_registration(dp: Dispatcher):
    dp.include_router(general.command_cancel_router)
    dp.include_router(general.command_image_router)

    dp.include_router(admins.command_admin_router)
    dp.include_router(admins.command_send_all_router)
    dp.include_router(admins.command_send_message_router)
    dp.include_router(admins.command_user_list_router)
    dp.include_router(admins.command_admin_list_router)
    dp.include_router(admins.command_server_router)
    dp.include_router(admins.admin_management_router)
    dp.include_router(admins.promocode_management_router)
    dp.include_router(admins.subscription_management_router)
    dp.include_router(admins.command_statistics_router)
    dp.include_router(admins.user_management_router)

    dp.include_router(groups.command_gpt_groups_router)
    dp.include_router(groups.command_all_mention_router)
    dp.include_router(groups.moderate_chat_router)
    dp.include_router(groups.edit_chat_router)

    dp.include_router(users.command_start_help_router)
    dp.include_router(users.command_profile_router)
    dp.include_router(users.command_promocode_router)
    dp.include_router(users.command_summary_router)
    dp.include_router(users.command_limits_router)
    dp.include_router(users.command_models_router)
    dp.include_router(users.handle_chat_router)


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="html")
    dp = Dispatcher(storage=MemoryStorage())

    routers_registration(dp=dp)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S')

    session_pool = await create_db_session()
    middleware_registration(dp=dp, session_pool=session_pool)

    await set_commands(bot)

    try:
        await dp.start_polling(bot)
    except Exception as ex:
        logging.error(f"[!!! Exception] - {ex}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
