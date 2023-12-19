from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    search_state = State()
    condition_selection = State()
    custom_state = State()
    number_selection = State()
    check_number_selection = State()
    final_selection = State()


