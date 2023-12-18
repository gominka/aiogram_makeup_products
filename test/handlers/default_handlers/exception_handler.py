import logging
from typing import Callable, Union
import functools

from peewee import IntegrityError
from requests.exceptions import RequestException, Timeout, HTTPError, ConnectTimeout
from telebot import types
from loader import bot
from user_interface import text

logger = logging.getLogger(__name__)
TIMEOUT = 10


def handle_request_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except (ConnectTimeout, Timeout):
            logger.error("Connection timed out. Please check your internet connection or try again later.")
            return None
        except HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            return None
        except RequestException as e:
            logger.error(f"An error occurred: {e}")
            return None

    return wrapper


def exc_handler(method: Callable) -> Callable:
    """ Decorator. Logs the exception to the called function, notifies the user of the error """

    @functools.wraps(method)
    def wrapped(message: Union[types.Message, types.CallbackQuery]) -> None:
        try:
            method(message)
        except ValueError as exception:
            if isinstance(message, types.CallbackQuery):
                message = message.message
            if exception.__class__.__name__ == 'JSONDecodeError':
                exc_handler(method(message))
            else:
                if str(exception) == 'Range Error':
                    bot.send_message(chat_id=message.chat.id, text="Enter a number")

                bot.register_next_step_handler(message=message, callback=exc_handler(method))

        except IntegrityError:
            bot.send_message(chat_id=message.chat.id, text=text.HELP_MSG)

        except Exception as e:
            logger.exception("An unexpected error occurred:")
            bot.reply_to(message, "To start the search, click /start")

    return wrapped
