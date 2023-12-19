from aiogram import Router, types, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.inline.search_keyboards import create_search_command_keyboard
from loader import dp
from site_ip.main_request import BASE_PARAMS, get_conditions_list

router = Router()


class SelectCond(StatesGroup):
    choosing_condition = State()
    custom_state = State()


# Define constant for the continue search callback
CHECK_AMOUNT_PRODUCTS_CALLBACK = 'check_amount_products'

# Define constant for the cancel search condition callback
CANCEL_SEARCH_COND_CALLBACK = 'cancel_search_cond'

# Define constant for the website link callback
WEBSITE_LINK_CALLBACK = 'website_link'


@router.message(Command(commands=['brand', 'product_tag', 'product_type']))
async def search_command_handler(message: types.Message, state: FSMContext) -> None:
    """Handle commands related to product search."""

    await state.update_data(search_cond=message.text[1:])

    user_data = await state.get_data()
    if "params" not in user_data:
        user_data["params"] = BASE_PARAMS

    buttons = [types.InlineKeyboardButton(text=condition, callback_data=condition)
               for condition in
               get_conditions_list(params=user_data["params"], selected_condition=user_data["search_cond"])]

    await message.answer(
        text="Select a condition:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 5] for i in range(0, len(buttons), 5)]))

    await state.set_state(SelectCond.choosing_condition)


@router.message(SelectCond.choosing_condition)
async def callback_search_command(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Process button clicks, condition selection."""
    print("1")
    user_data = await state.get_data()
    search_cond = user_data["search_cond"]
    user_data["params"][search_cond] = callback.data

    await callback.answer(
        text="Select a condition",
        reply_markup=create_search_command_keyboard(search_cond)
    )

    await state.set_state(SelectCond.custom_state)
