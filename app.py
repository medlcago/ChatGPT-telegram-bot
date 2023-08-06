async def main():
    import logging
    from loader import bot
    from utils import set_commands
    from data.config import DEBUG
    from middlewares import BlockMiddleware

    from routers import dp

    logging.basicConfig(level=logging.INFO)

    dp.message.middleware.register(BlockMiddleware())
    dp.callback_query.middleware.register(BlockMiddleware())

    await set_commands(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        if DEBUG:
            from filters import IsAdmin
            dp.message.filter(IsAdmin())
            dp.callback_query.filter(IsAdmin())
        await dp.start_polling(bot)
    except Exception as ex:
        logging.error(f"[!!! Exception] - {ex}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
