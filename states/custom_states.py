from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class StartState(StatesGroup):
    start_state = State()


class SelectCond(StatesGroup):
    choosing_condition = State()
    custom_state = State()
    final_selection = State()

class FinalCond(StatesGroup):
    final_selection = State()

class UserState(StatesGroup):
    search_state = State()
    condition_selection = State()
    custom_state = State()
    number_selection = State()
    check_number_selection = State()
    final_selection = State()
