from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    search_state = State()
    condition_selection = State()
    custom_state = State()
    number_selection = State()
    check_number_selection = State()
    final_selection = State()


