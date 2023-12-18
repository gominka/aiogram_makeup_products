from telebot import types

import states
from handlers.default_handlers.exception_handler import exc_handler
from keyboards.inline.search_keyboards import create_command_keyboard
from keyboards.reply import reply_keyboards
from loader import bot


def set_user_state(user_id, chat_id, new_state):
    bot.set_state(user_id=user_id, state=new_state, chat_id=chat_id)


def send_message_with_keyboard(chat_id, text, keyboard):
    bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)


def handle_search_command(message, condition_suffix):
    msg_user = message.text[1:]
    user_id, chat_id = message.from_user.id, message.chat.id

    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        data["cond2"] = f"_{condition_suffix}"

    set_user_state(user_id, chat_id, states.custom_states.UserState.number_selection)
    send_message_with_keyboard(chat_id, "Choose a condition: ", reply_keyboards.get_reply_keyboard(["rating", "price"]))


@bot.message_handler(commands=['high', 'low'])
@exc_handler
def main_search_command(message: types.Message) -> None:
    """Handler triggered by the command /high, /low"""
    handle_search_command(message, "less_than" if message.text[1:] == "high" else "greater_than")


@bot.message_handler(state=states.custom_states.UserState.number_selection)
@exc_handler
def select_condition(message: types.Message) -> None:
    msg_user, user_id, chat_id = message.text, message.from_user.id, message.chat.id

    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        data["cond1"] = msg_user

    set_user_state(user_id, chat_id, states.custom_states.UserState.check_number_selection)
    send_message_with_keyboard(chat_id, "Enter a number: ", reply_keyboards.EMPTY)


@bot.message_handler(state=states.custom_states.UserState.check_number_selection)
@exc_handler
def select_cond(message: types.Message) -> None:
    msg_user = int(message.text)
    user_id = message.from_user.id
    chat_id = message.chat.id

    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        if (data["cond1"] == "rating" and 1 <= msg_user <= 10) or data["cond1"] == "price":
            cond = data["cond1"] + data["cond2"]
            data["params"][cond] = msg_user

            search_command_markup = create_command_keyboard()
            bot.set_state(user_id=user_id, state=states.custom_states.UserState.custom_state, chat_id=chat_id)
            bot.send_message(chat_id=chat_id, text="Select a condition ", reply_markup=search_command_markup)

        elif data["cond1"] == "rating":
            bot.set_state(user_id=user_id, state=states.custom_states.UserState.number_selection, chat_id=chat_id)
            bot.send_message(chat_id=message.chat.id, text="The number must be from 1 to 10",
                             reply_markup=reply_keyboards.EMPTY)
            select_condition(message)
