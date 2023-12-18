from aiogram import types
from config_data.config import DEFAULT_COMMANDS


async def set_commands(dp):
    await dp.bot.set_my_commands(
        [types.BotCommand(name, description) for name, description in DEFAULT_COMMANDS]
    )
