import os

"""
-1001620211812 учебка
-1001525007729 уебища team🗿🥊💸
-1001803035829 Гринчи ББСО🍃💥👹
-1001633082765 Тестовая группа
"""

from dotenv import load_dotenv

load_dotenv()

models = [
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-32k",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-16k",
]

default_model = "gpt-3.5-turbo"

OpenAI_API_KEY = os.getenv("OpenAI_API_KEY")
OpenAI_API_BASE = "https://chimeragpt.adventblocks.cc/api/v1"

BOT_TOKEN = os.getenv("BOT_TOKEN")

host = os.getenv("host")
port = int(os.getenv("port"))
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")

connection_db_string = f'mysql+aiomysql://{user}:{password}@{host}:{port}/{db}'

main_chat_ids = (-1001633082765, -1001525007729)

response_chance = 0
response_delay = 5

request_limit = 20

DEBUG = False
