async def main():
    import logging
    from loader import bot
    from utils import set_commands
    from middlewares import (
        BlockMiddleware,
        DebugMiddleware,
        SubscribersMiddleware)

    from routers import dp

    logging.basicConfig(level=logging.INFO)

    dp.message.middleware.register(BlockMiddleware())
    dp.callback_query.middleware.register(BlockMiddleware())

    dp.message.middleware.register(DebugMiddleware())
    dp.callback_query.middleware.register(DebugMiddleware())

    dp.message.middleware.register(SubscribersMiddleware())
    dp.callback_query.middleware.register(SubscribersMiddleware())

    await set_commands(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except Exception as ex:
        logging.error(f"[!!! Exception] - {ex}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    import asyncio
    import logging

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
