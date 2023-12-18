from loguru import logger

import config_data.config as config
from loader import dp
from utils.misc.set_commands import set_commands


async def startup(dispatcher):
    """Triggers on startup, you may
    add filters and middlewares later."""
    await set_commands(dispatcher)
    logger.info("Bot has started")


async def shutdown(dispatcher):
    """Triggers on shutdown"""
    logger.info("Bot has stopped")


if __name__ == "__main__":
    # Starts long-polling mode
    executor.start_polling(
        dp, on_startup=startup, on_shutdown=shutdown,
        skip_updates=config.skip_updates
    )
