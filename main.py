import asyncio
import logging
from datetime import datetime

from database.models import create_models
from handlers.additional_handlers import price_rating, search_callback, history
from handlers.default_handlers import start_commands, search_router
from loader import dp, bot


def setup_logging():
    logging.basicConfig(level=logging.INFO)


def setup_dispatcher():
    dp.include_routers(
        start_commands.start_router,
        search_router.search_router,
        price_rating.cond_router,
        search_callback.search_call_router,
        history.history_router
    )


async def main():
    dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    await bot.delete_webhook(drop_pending_updates=True)

    setup_dispatcher()

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    create_models()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
