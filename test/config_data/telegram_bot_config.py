import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class TelegramBotConfig:
    token: str


def load_telegram_bot_config() -> TelegramBotConfig:
    load_dotenv()
    return TelegramBotConfig(token=os.getenv("BOT_TOKEN"))
