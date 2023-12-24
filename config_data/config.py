import os
from environs import Env
from peewee import ImproperlyConfigured
from dataclasses import dataclass
from pydantic.v1 import SecretStr


@dataclass
class DatabaseConfig:
    name: SecretStr


@dataclass
class TelegramBotConfig:
    token: SecretStr


def getenv_or_raise(key: str, default=None):
    value = os.getenv(key, default)
    if value is None:
        raise ImproperlyConfigured(f"Environment variable {key} is not set.")
    return value


@dataclass
class AppConfig:
    tg_bot: TelegramBotConfig
    database: DatabaseConfig


def load_config(path: str = None) -> AppConfig:
    env = Env()
    env.read_env(path)

    return AppConfig(
        tg_bot=TelegramBotConfig(token=SecretStr(getenv_or_raise("BOT_TOKEN"))),
        database=DatabaseConfig(name=SecretStr(getenv_or_raise("DB_NAME")))
    )


def load_default_commands() -> tuple:
    return (
        ("start", "Start the search"),
        ("brand", "Brand selection"),
        ("product_tag", "Tag selection"),
        ("product_type", "Type selection"),
        ("start_again", "Start again")
    )


# Load configuration
config = load_config()

# Access configuration values
BOT_TOKEN = config.tg_bot.token.get_secret_value()
DB_NAME = config.database.name.get_secret_value()

# Default commands
DEFAULT_COMMANDS = load_default_commands()
