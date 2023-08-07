from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from data.config import BOT_TOKEN, connection_db_string
from utils.database import Database

bot = Bot(token=BOT_TOKEN, parse_mode="html")
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db = Database(url=connection_db_string)
