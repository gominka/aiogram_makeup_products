from aiogram.fsm.state import State, StatesGroup


class StartState(StatesGroup):
    start_state = State()


class SelectCond(StatesGroup):
    choosing_condition = State()
    custom_state = State()
    final_selection = State()
    number_selection = State()
    check_number_selection = State()


class FinalCond(StatesGroup):
    final_selection = State()
