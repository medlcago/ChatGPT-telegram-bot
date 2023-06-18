import os

import poe

"""
-1001620211812 учебка
-1001525007729 уебища team🗿🥊💸
-1001803035829 Гринчи ББСО🍃💥👹
-1001633082765 Тестовая группа
"""

from dotenv import load_dotenv

load_dotenv()

OpenAI_API_KEY = os.getenv("OpenAI_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
model = "gpt-3.5-turbo"
BOT_TOKEN = os.getenv("BOT_TOKEN")

client_poe = poe.Client(token=os.getenv("POE_TOKEN"))

current_dir = os.path.abspath(os.path.dirname(__file__))
COOKIE_PATH = os.path.join(current_dir, 'cookie.json')

host = os.getenv("host")
port = int(os.getenv("port"))
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")

response_chance = 0
response_delay = 5

request_limit = 15

DEBUG = False
