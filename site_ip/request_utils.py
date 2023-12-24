from asyncio.log import logger
import functools
from requests.exceptions import RequestException, Timeout, HTTPError, ConnectTimeout


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
