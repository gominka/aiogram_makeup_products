import asyncio
import logging
from datetime import datetime
from handlers.default_handlers import start_commands, search_commands
from loader import dp, bot


async def main():
    dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_routers(start_commands.router, search_commands.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
