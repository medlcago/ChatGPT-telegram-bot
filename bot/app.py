import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from handlers import (
    users,
    admins,
    general,
    groups,
    universal_handler_router
)
from language.translator import Translator
from middlewares import (
    DatabaseMiddleware,
    BlockMiddleware,
    DebugMiddleware,
    SubscribersMiddleware,
    RateLimitMiddleware,
    TranslatorMiddleware,
    UserRegistrationMiddleware
)
from settings.database.setup import async_session_maker
from settings.redis.setup import create_redis_session
from utils.misc import set_bot_commands


def middlewares_registration(dp: Dispatcher, session_pool):
    dp.message.outer_middleware(DatabaseMiddleware(session_pool))
    dp.callback_query.outer_middleware(DatabaseMiddleware(session_pool))
    dp.my_chat_member.outer_middleware(DatabaseMiddleware(session_pool))

    dp.message.middleware(UserRegistrationMiddleware())

    dp.message.outer_middleware(TranslatorMiddleware())
    dp.callback_query.outer_middleware(TranslatorMiddleware())

    dp.message.middleware(BlockMiddleware())
    dp.callback_query.middleware(BlockMiddleware())

    dp.message.middleware(DebugMiddleware())
    dp.callback_query.middleware(DebugMiddleware())

    dp.message.middleware(SubscribersMiddleware())
    dp.callback_query.middleware(SubscribersMiddleware())

    dp.message.middleware(RateLimitMiddleware())
    dp.callback_query.middleware(RateLimitMiddleware())


def routers_registration(dp: Dispatcher):
    dp.include_router(universal_handler_router)
    dp.include_router(general.command_image_router)

    dp.include_router(admins.command_admin_router)
    dp.include_router(admins.command_contact_admin_router)
    dp.include_router(admins.command_all_router)
    dp.include_router(admins.command_send_message_router)
    dp.include_router(admins.command_user_list_router)
    dp.include_router(admins.command_admin_list_router)
    dp.include_router(admins.command_server_router)
    dp.include_router(admins.admin_management_router)
    dp.include_router(admins.promocode_management_router)
    dp.include_router(admins.subscription_management_router)
    dp.include_router(admins.command_statistics_router)
    dp.include_router(admins.user_management_router)
    dp.include_router(admins.get_user_by_id_router)

    dp.include_router(groups.command_gpt_groups_router)
    dp.include_router(groups.command_all_mention_router)
    dp.include_router(groups.moderate_chat_router)
    dp.include_router(groups.edit_chat_router)

    dp.include_router(users.user_activity_status_router)
    dp.include_router(users.command_start_help_router)
    dp.include_router(users.command_profile_router)
    dp.include_router(users.command_affiliate_program_router)
    dp.include_router(users.command_contact_admin_router)
    dp.include_router(users.command_promocode_router)
    dp.include_router(users.command_summary_router)
    dp.include_router(users.command_limits_router)
    dp.include_router(users.command_models_router)
    dp.include_router(users.handle_chat_router)


async def on_startup(bot: Bot):
    await set_bot_commands(bot=bot)


async def main():
    bot = Bot(token=config.tg.token, parse_mode="html")
    dp = Dispatcher(storage=MemoryStorage())
    dp.startup.register(on_startup)

    session_pool = async_session_maker
    redis = await create_redis_session(url=config.redis.redis_url)

    routers_registration(dp=dp)
    middlewares_registration(dp=dp, session_pool=session_pool)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
        datefmt='%d.%m.%Y %H:%M:%S'
    )
    logging.info(f"Bot running in {'DEBUG' if config.debug else 'RELEASE'} mode!")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot,
                               translator=Translator(),
                               config=config,
                               redis=redis
                               )
    except Exception as ex:
        logging.error(f"[!!! Exception] - {ex}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
