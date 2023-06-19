import logging

import poe
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from data.config import BOT_TOKEN, POE_TOKEN
from utils.database.db import Database

poe.logger.setLevel(logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="html")
client_poe = poe.Client(token=POE_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db = Database()
