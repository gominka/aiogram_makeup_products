import asyncio
import logging
from datetime import datetime
from handlers.default_handlers import start_commands, search_commands
from loader import dp, bot


async def main():
    dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    dp.include_routers(start_commands.router, search_commands.router)

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
