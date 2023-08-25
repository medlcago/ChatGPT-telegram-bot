import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from data.config import load_config
from handlers import admins, general, groups, users
from middlewares import (
    DatabaseMiddleware,
    BlockMiddleware,
    DebugMiddleware,
    SubscribersMiddleware,
    ConfigMiddleware,
    RedisMiddleware)
from settings.database.setup import create_db_session
from settings.redis.setup import create_redis_session
from utils.misc import set_commands


def middlewares_registration(dp: Dispatcher, config, session_pool, redis):
    dp.message.outer_middleware(DatabaseMiddleware(session_pool))
    dp.callback_query.outer_middleware(DatabaseMiddleware(session_pool))

    dp.message.outer_middleware(RedisMiddleware(redis))
    dp.callback_query.outer_middleware(RedisMiddleware(redis))

    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))

    dp.message.outer_middleware(BlockMiddleware())
    dp.callback_query.outer_middleware(BlockMiddleware())

    dp.message.outer_middleware(DebugMiddleware())
    dp.callback_query.outer_middleware(DebugMiddleware())

    dp.message.outer_middleware(SubscribersMiddleware())
    dp.callback_query.outer_middleware(SubscribersMiddleware())


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
    dp.include_router(users.command_ref_router)
    dp.include_router(users.command_promocode_router)
    dp.include_router(users.command_summary_router)
    dp.include_router(users.command_limits_router)
    dp.include_router(users.command_models_router)
    dp.include_router(users.handle_chat_router)


async def main():
    config = load_config()
    bot = Bot(token=config.tg.token, parse_mode="html")
    dp = Dispatcher(storage=MemoryStorage())
    session_pool = await create_db_session(url=config.db.connection_db_string)
    redis = await create_redis_session(url=config.redis.redis_url)

    routers_registration(dp=dp)
    middlewares_registration(dp=dp, config=config, session_pool=session_pool, redis=redis)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S')

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
