import asyncio


async def main():
    import logging
    from loader import dp, bot
    from utils import set_commands

    from handlers import users
    from handlers import groups
    from handlers import admins

    logging.basicConfig(level=logging.INFO)

    await set_commands(bot)

    dp.include_router(users.command_start_router)
    dp.include_router(users.command_help_users_router)
    dp.include_router(users.command_image_users_router)
    dp.include_router(users.command_summary_router)
    dp.include_router(users.command_limits_router)

    dp.include_router(groups.command_gpt_groups_router)
    dp.include_router(groups.command_image_groups_router)
    dp.include_router(groups.command_all_mention_router)

    dp.include_router(admins.command_admin_router)
    dp.include_router(admins.command_send_all_router)
    dp.include_router(admins.command_send_message_router)
    dp.include_router(admins.command_user_list_router)
    dp.include_router(admins.command_admin_list_router)
    dp.include_router(admins.command_server_router)
    dp.include_router(admins.command_add_admin_router)
    dp.include_router(admins.command_remove_admin_router)

    dp.include_router(users.handle_chat_router)

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except Exception as ex:
        logging.error(f"[!!! Exception] - {ex}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
