import os

"""
-1001620211812 учебка
-1001525007729 уебища team🗿🥊💸
-1001803035829 Гринчи ББСО🍃💥👹
-1001633082765 Тестовая группа
"""

from dotenv import load_dotenv

load_dotenv()

models = {
    "gpt-4": "beaver",
    "claude": "a2_2",
    "gpt-3.5-turbo": "gpt-3.5-turbo",
    "bing": "bing"
}

chat_type_mapping = {
    "gpt-3.5-turbo": 1,
    "gpt-4": 2,
    "bing": 3,
    "claude": 4
}

reverse_chat_type_mapping = {
    value: key for key, value in chat_type_mapping.items()
}

OpenAI_API_KEY = os.getenv("OpenAI_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
POE_TOKEN = os.getenv("POE_TOKEN")
COOKIE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cookie.json')

host = os.getenv("host")
port = int(os.getenv("port"))
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")

response_chance = 0
response_delay = 5

request_limit = 20

DEBUG = False
