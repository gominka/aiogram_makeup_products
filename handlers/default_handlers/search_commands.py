from aiogram import Router, types, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.inline.search_keyboards import create_search_command_keyboard, create_name_selection_keyboard
from loader import dp
from site_ip.main_request import BASE_PARAMS

router = Router()


class SelectCond(StatesGroup):
    choosing_condition = State()
    choosing_food_size = State()


# Define constant for the continue search callback
CHECK_AMOUNT_PRODUCTS_CALLBACK = 'check_amount_products'

# Define constant for the cancel search condition callback
CANCEL_SEARCH_COND_CALLBACK = 'cancel_search_cond'

# Define constant for the website link callback
WEBSITE_LINK_CALLBACK = 'website_link'


async def send_search_condition_message(chat_id, text, reply_markup):
    """Helper function to send search condition message"""
    await dp.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


@router.message(Command(commands=['brand', 'product_tag', 'product_type']))
async def search_command_handler(message: types.Message, state: FSMContext) -> None:
    """Handle commands related to product search."""

    user_id, chat_id = message.from_user.id, message.chat.id

    user_data = await state.get_data()

    user_data["search_cond"] = message.text[1:]

    if "params" not in user_data:
        user_data["params"] = BASE_PARAMS

    await message.answer(
        text="Select a condition:",
        reply_markup=create_name_selection_keyboard(create_name_selection_keyboard(user_data["params"],
                                                                                   user_data["search_cond"]))
    )

    await state.set_state(SelectCond.choosing_condition)


@router.message(SelectCond.choosing_condition)
async def callback_search_command(call: types.CallbackQuery) -> None:
    """Process button clicks, condition selection."""

    user_id = call.from_user.id
    chat_id = call.message.chat.id

    data = await get_user_data(user_id, chat_id)
    search_cond = data["search_cond"]
    data["params"][search_cond] = call.data

    search_command_markup = create_search_command_keyboard(search_cond)

    await send_search_condition_message(chat_id, "Select a condition ", search_command_markup)

    await state.set_state(states.custom_states.UserState.custom_state)
