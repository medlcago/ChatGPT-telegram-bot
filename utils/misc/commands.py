from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
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
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
