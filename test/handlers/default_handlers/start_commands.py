from loguru import logger
from telebot.types import Message
from database.models import User
from handlers.default_handlers.exception_handler import exc_handler
from user_interface import text
from loader import bot
import states.custom_states


@bot.message_handler(commands=['start'], state="*")
@exc_handler
def start_command_handler(message: Message) -> None:
    """Handler for the /start command."""
    user_id, username, first_name, last_name, chat_id = get_user_info(message)

    bot.set_state(user_id=user_id, state=states.custom_states.UserState.search_state, chat_id=chat_id)
    create_and_save_user(user_id, username, first_name, last_name)
    User(user_id=user_id, username=username, first_name=first_name, last_name=last_name).save()
    logger.info(f'A new user has been added. User_id: {user_id}')

    bot.send_message(chat_id=message.chat.id, text=text.START_MSG)




