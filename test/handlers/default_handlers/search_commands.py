from telebot import types

import states
from handlers.default_handlers.exception_handler import exc_handler
from keyboards.inline.search_keyboards import create_search_command_keyboard, create_name_selection_keyboard
from loader import bot
from site_ip.main_request import BASE_PARAMS

# Define constants for command strings
BRAND_COMMAND = '/brand'
PRODUCT_TAG_COMMAND = '/product_tag'
PRODUCT_TYPE_COMMAND = '/product_type'

# Define constant for the continue search callback
CHECK_AMOUNT_PRODUCTS_CALLBACK = 'check_amount_products'

# Define constant for the cancel search condition callback
CANCEL_SEARCH_COND_CALLBACK = 'cancel_search_cond'

# Define constant for the website link callback
WEBSITE_LINK_CALLBACK = 'website_link'


def get_user_data(user_id, chat_id):
    """Helper function to retrieve user data"""
    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        return data


def send_search_condition_message(chat_id, text, reply_markup):
    """Helper function to send search condition message"""
    bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


@bot.message_handler(commands=['brand', 'product_tag', 'product_type'], state="*")
@exc_handler
def search_command_handler(message: types.Message) -> None:
    """Handle commands related to product search."""

    command = message.text[1:]
    user_id = message.from_user.id
    chat_id = message.chat.id

    data = get_user_data(user_id, chat_id)
    data["search_cond"] = command

    if "params" not in data:
        data["params"] = BASE_PARAMS

    params = data["params"]
    search_cond = data["search_cond"]

    kb_cond = create_name_selection_keyboard(params, search_cond)

    bot.set_state(user_id=user_id, state=states.custom_states.UserState.condition_selection, chat_id=chat_id)

    send_search_condition_message(chat_id, "Select a condition:  ", kb_cond)


@bot.callback_query_handler(func=None, state=states.custom_states.UserState.condition_selection)
@exc_handler
def callback_search_command(call: types.CallbackQuery) -> None:
    """Process button clicks, condition selection."""

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    data = get_user_data(user_id, chat_id)
    search_cond = data["search_cond"]
    data["params"][search_cond] = call.data

    search_command_markup = create_search_command_keyboard(search_cond)

    send_search_condition_message(chat_id, "Select a condition ", search_command_markup)

    bot.set_state(user_id=user_id, state=states.custom_states.UserState.custom_state, chat_id=chat_id)
