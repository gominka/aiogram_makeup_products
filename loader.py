from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from config_data.config import load_config, AppConfig


def create_bot(conf: AppConfig):
    return Bot(token=conf.tg_bot.token.get_secret_value(), parse_mode=ParseMode.HTML)


def create_dispatcher():
    return Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)


config = load_config()
bot = create_bot(config)
dp = create_dispatcher()
