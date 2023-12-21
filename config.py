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
    context_limit: int


@dataclass
class ModelsConfig:
    available_models: list
    default_chat_model: str
    default_image_model: str


@dataclass
class Config:
    tg: TgBotConfig
    db: DbConfig
    redis: RedisConfig
    openai: OpenAIConfig
    models: ModelsConfig
    creator_user_id: int
    refresh_time: int  # время (в часах) следующего обновления данных
    debug: bool


def load_config(debug: bool = False, path: str | None = None) -> Config:
    env = Env()
    env.read_env(path=path)

    return Config(
        tg=TgBotConfig(
            token=env.str("BOT_TOKEN_DEBUG") if debug else env.str("BOT_TOKEN")
        ),
        redis=RedisConfig(
            redis_url=env.str("REDIS_URL")
        ),
        db=DbConfig(
            user=env.str("DB_USER_TEST"),
            password=env.str("DB_PASSWORD_TEST"),
            host=env.str("DB_HOST_TEST"),
            port=env.str("DB_PORT_TEST"),
            database=env.str("DB_DB_NAME_TEST"),
            connection_db_string=f'mysql+aiomysql://{env.str("DB_USER_TEST")}:{env.str("DB_PASSWORD_TEST")}@{env.str("DB_HOST_TEST")}:{env.str("DB_PORT_TEST")}/{env.str("DB_DB_NAME_TEST")}'
        ) if debug else DbConfig(
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            host=env.str("DB_HOST"),
            port=env.str("DB_PORT"),
            database=env.str("DB_NAME"),
            connection_db_string=f'mysql+aiomysql://{env.str("DB_USER")}:{env.str("DB_PASSWORD")}@{env.str("DB_HOST")}:{env.str("DB_PORT")}/{env.str("DB_NAME")}'
        ),
        openai=OpenAIConfig(
            api_key=env.str("OpenAI_API_KEY"),
            api_base=env.str("OpenAI_API_BASE"),
            context_limit=10
        ),
        models=ModelsConfig(
            available_models=[
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-16k-0613",
                "llama-2-70b-chat",
                "code-llama-34b-instruct",
                "falcon-180b-chat"
            ],
            default_chat_model="gpt-3.5-turbo",
            default_image_model="sdxl"
        ),
        creator_user_id=env.int("CREATOR_USER_ID"),
        refresh_time=12,
        debug=debug
    )


main_chat_ids = (-1001633082765, -1001525007729)

SUBSCRIBERS_ONLY = False
DEBUG = False

config = load_config(debug=False)
