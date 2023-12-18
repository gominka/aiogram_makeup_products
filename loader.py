from aiogram import Bot, Dispatcher

from config.config import BOT_TOKEN


# Bot, storage and dispatcher instances
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
