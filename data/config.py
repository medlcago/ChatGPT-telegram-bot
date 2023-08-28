from dataclasses import dataclass

from environs import Env

"""
-1001620211812 учебка
-1001525007729 уебища team🗿🥊💸
-1001803035829 Гринчи ББСО🍃💥👹
-1001633082765 Тестовая группа
"""


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
class RedisConfig:
    redis_url: str


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
    redis: RedisConfig
    openai: OpenAIConfig
    models: ModelsConfig
    creator_user_id: int


def load_config(mode: str, path: str | None = None) -> Config:
    env = Env()
    env.read_env(path=path)

    return Config(
        tg=TgBotConfig(
            token=env.str("BOT_TOKEN") if mode == "release" else env.str("BOT_TOKEN_DEBUG")
        ),
        redis=RedisConfig(
            redis_url=env.str("REDIS_URL")
        ),
        db=DbConfig(
            user=env.str("user"),
            password=env.str("password"),
            host=env.str("host"),
            port=env.str("port"),
            database=env.str("db"),
            connection_db_string=f'mysql+aiomysql://{env.str("user")}:{env.str("password")}@{env.str("host")}:{env.str("port")}/{env.str("db")}'
        ),
        openai=OpenAIConfig(
            api_key=env.str("OpenAI_API_KEY"),
            api_base=env.str("OpenAI_API_BASE")
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
        ),
        creator_user_id=env.int("CREATOR_USER_ID")
    )


main_chat_ids = (-1001633082765, -1001525007729)

response_chance = 0
response_delay = 5

SUBSCRIBERS_ONLY = False
DEBUG = False
