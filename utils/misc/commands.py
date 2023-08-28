from aiogram.types import BotCommand


async def get_bot_commands():
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
    return commands
