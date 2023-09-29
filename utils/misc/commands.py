from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_bot_commands(bot: Bot):
    ru_commands = [
        BotCommand(
            command="start",
            description="Запуск бота"
        ),
        BotCommand(
            command="help",
            description="Помощь"
        ),
        BotCommand(
            command="models",
            description="Список моделей"
        )
    ]

    en_commands = [
        BotCommand(
            command="start",
            description="Start bot"
        ),
        BotCommand(
            command="help",
            description="Help"
        ),
        BotCommand(
            command="models",
            description="List of models"
        )
    ]

    await bot.set_my_commands(ru_commands, language_code="ru", scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(en_commands, language_code="en", scope=BotCommandScopeAllPrivateChats())
