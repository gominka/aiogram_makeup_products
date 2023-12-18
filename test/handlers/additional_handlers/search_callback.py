from telebot import types

import states
from database.models import Selections
from handlers.default_handlers.exception_handler import exc_handler
from keyboards.inline.search_keyboards import create_website_link_keyboard, create_name_selection_keyboard
from loader import bot
from site_ip.main_request import make_response
from user_interface import text
from user_interface.text import DESCRIPTION

# Constants for Callback Data
CHECK_AMOUNT_PRODUCTS_CALLBACK = 'check_amount_products'
CANCEL_SEARCH_COND_CALLBACK = 'cancel_search_cond'
WEBSITE_LINK_CALLBACK = 'website_link'

# Constants for States
FINAL_SELECTION_STATE = states.custom_states.UserState.final_selection
CONDITION_SELECTION_STATE = states.custom_states.UserState.condition_selection
CUSTOM_STATE = states.custom_states.UserState.custom_state


def get_user_data(user_id, chat_id):
    """Helper function to retrieve user data."""
    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        return data


def handle_single_product_response(selected_product, user_id, chat_id):
    """Handle response when only one product is available."""
    Selections(user_id=user_id, product_name=selected_product["name"]).save()
    send_product_details(chat_id, selected_product)


def handle_multiple_products_response(params, user_id, chat_id):
    """Handle response when multiple products are available."""
    kb_cond = create_name_selection_keyboard(params, selected_condition="list_name_product")

    bot.set_state(user_id=user_id, state=FINAL_SELECTION_STATE, chat_id=chat_id)

    bot.send_message(chat_id=chat_id, reply_markup=kb_cond, text="Select a name:  ")


def send_product_details(chat_id, selected_product):
    """Send product details to the user."""
    bot.send_message(chat_id=chat_id, text=DESCRIPTION.format(
        selected_product["name"],
        selected_product["price"],
        selected_product["description"],
        selected_product["product_link"]))


@bot.callback_query_handler(func=lambda call: call.data in [CHECK_AMOUNT_PRODUCTS_CALLBACK])
def check_amount_products_callback(call: types.CallbackQuery) -> None:
    """Handle the 'check_amount_products' callback."""

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        params = data["params"]
        response = make_response(params=params)

    if len(response) == 1:
        handle_single_product_response(response[0], user_id, chat_id)
    elif 1 <= len(response) <= 3:
        handle_multiple_products_response(params, user_id, chat_id)
    else:
        bot.send_message(chat_id=call.message.chat.id, text=text.CONDITION)


@bot.callback_query_handler(func=None, state=FINAL_SELECTION_STATE)
@exc_handler
def callback_search_command(call: types.CallbackQuery) -> None:
    """Processing button clicks, condition selection"""
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        data["params"]["name"] = call.data
        params = data["params"]
        selected_product = make_response(params=params)[0]

        Selections(user_id=user_id, product_name=selected_product["name"]).save()

        send_product_details(chat_id, selected_product)

    bot.set_state(user_id=user_id, state=states.custom_states.UserState.custom_state, chat_id=chat_id)


@bot.callback_query_handler(func=lambda call: call.data in [CANCEL_SEARCH_COND_CALLBACK])
@exc_handler
def call_btn_file(call: types.CallbackQuery) -> None:
    bot.set_state(user_id=call.from_user.id, state=CONDITION_SELECTION_STATE, chat_id=call.message.chat.id)
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=lambda call: call.data in ["website_link"])
def handle_website_link_callback(call: types.CallbackQuery) -> None:
    """Processing of a button click, a link to the site"""
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        params = data["params"]

        urlkb = create_website_link_keyboard(make_response(params=params)[0][call.data])

        bot.send_message(chat_id=chat_id, text="To visit the website, click the button below", reply_markup=urlkb)