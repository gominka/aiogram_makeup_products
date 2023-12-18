import os
from dataclasses import dataclass
from peewee import ImproperlyConfigured


# Whether to skip updates or not
skip_updates = False
@dataclass
class Config:
    tg_bot: load_telegram_bot_config()
    database: load_database_config()


def getenv(key: str, default=None):
    value = os.getenv(key, default)
    if value is None:
        raise ImproperlyConfigured(f"Environment variable {key} is not set.")
    return value


config = Config(
    tg_bot=load_telegram_bot_config(),
    database=load_database_config()
)

DB_NAME = config.database.name
BOT_TOKEN = config.tg_bot.token

# List of commands
DEFAULT_COMMANDS = (
    ("start", "Start the search"),
    ("brand", "Brand selection"),
    ("product_tag", "Tag selection"),
    ("product_type", "Type selection"),
    ("start_again", "Start again")
)
