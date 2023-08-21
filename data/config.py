import os
from dataclasses import dataclass

"""
-1001620211812 учебка
-1001525007729 уебища team🗿🥊💸
-1001803035829 Гринчи ББСО🍃💥👹
-1001633082765 Тестовая группа
"""

from dotenv import load_dotenv

load_dotenv()


@dataclass
class TgBotConfig:
    token: str


@dataclass
class DbConfig:
    user: str
    password: str
    database: str
    host: str
    port: str
    connection_db_string: str


@dataclass
class OpenAIConfig:
    api_key: str
    api_base: str


@dataclass
class ModelsConfig:
    available_models: list
    default_model: str
    request_limit: int


@dataclass
class Config:
    tg: TgBotConfig
    db: DbConfig
    openai: OpenAIConfig
    models: ModelsConfig


def load_config():
    return Config(
        tg=TgBotConfig(
            token=os.getenv("BOT_TOKEN"),
        ),
        db=DbConfig(
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port"),
            database=os.getenv("db"),
            connection_db_string=f'mysql+aiomysql://{os.getenv("user")}:{os.getenv("password")}@{os.getenv("host")}:{os.getenv("port")}/{os.getenv("db")}'
        ),
        openai=OpenAIConfig(
            api_key=os.getenv("OpenAI_API_KEY"),
            api_base=os.getenv("OpenAI_API_BASE")
        ),
        models=ModelsConfig(
            available_models=[
                "gpt-4",
                "gpt-4-0314",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0301",
                "gpt-3.5-turbo-16k",
                "llama-2-70b-chat"
            ],
            default_model="gpt-3.5-turbo",
            request_limit=20
        )
    )


main_chat_ids = (-1001633082765, -1001525007729)

response_chance = 0
response_delay = 5

SUBSCRIBERS_ONLY = False
DEBUG = False
