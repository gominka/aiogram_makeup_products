from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage


import config_data.config as config

# Bot, storage and dispatcher instances
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
