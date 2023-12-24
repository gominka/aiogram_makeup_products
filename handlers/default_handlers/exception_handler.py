from asyncio.log import logger
import functools
from loader import bot


TIMEOUT = 10


#
# def exc_handler(method: Callable) -> Callable:
#     """ Decorator. Logs the exception to the called function, notifies the user of the error """
#     @functools.wraps(method)
#     async def wrapped(message: types.Message) -> None:
#         try:
#             method(message)
#         except ValueError as exception:
#             if isinstance(message, types.CallbackQuery):
#                 message = message.message
#             if exception.__class__.__name__ == 'JSONDecodeError':
#                 await exc_handler(method)(message)
#             else:
#                 if str(exception) == 'Range Error':
#                     await bot.send_message(chat_id=message.chat.id, text="Enter a number")
#
#                 await bot.register_next_step_handler(message=message, callback=exc_handler(method))
#
#         except IntegrityError:
#             await bot.send_message(chat_id=message.chat.id, text=text.HELP_MSG)
#
#         except Exception:
#             logger.error("An unexpected error occurred:")
#             await bot.reply_to(message, "To start the search, click /start")
#
#     return wrapped
def error_handler(handler):
    """Decorator to handle errors and notify the user."""

    @functools.wraps(handler)
    async def wrapped(*args, **kwargs):
        try:
            return await handler(*args, **kwargs)
        except Exception as e:
            print(e)
            await handle_error(*args, e)

    return wrapped


async def handle_error(message, exception):
    await message.reply("To start the search, click /start")
    logger.error(f"An unexpected error occurred: {exception}")
