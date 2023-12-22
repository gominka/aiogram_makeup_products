from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from handlers.default_handlers.exception_handler import exc_handler
from keyboards.inline.search_keyboards import create_search_command_keyboard
from site_ip.main_request import BASE_PARAMS, get_conditions_list
from states.custom_states import SelectCond

search_router = Router()


@search_router.message(Command(commands=['brand', 'product_tag', 'product_type']))
@exc_handler
async def search_command_handler(message: types.Message, state: FSMContext) -> None:
    """Handle commands related to product search."""
    search_condition = message.text[1:]

    await state.update_data(search_cond=search_condition)
    await state.update_data(params=BASE_PARAMS)

    user_data = await state.get_data()
    conditions_list = get_conditions_list(params=user_data["params"],
                                          selected_condition=search_condition)

    buttons = [
        types.InlineKeyboardButton(text=condition, callback_data=condition)
        for condition in conditions_list
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 5] for i in range(0, len(buttons), 5)])

    await message.answer(text="Select a condition:", reply_markup=keyboard)
    await state.set_state(SelectCond.choosing_condition)


@search_router.callback_query(SelectCond.choosing_condition)
async def callback_search_command(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Process button clicks, condition selection."""

    user_data = await state.get_data()
    search_condition = user_data["search_cond"]
    selected_condition = callback.data

    user_data["params"][search_condition] = selected_condition

    await callback.message.answer(
        text="Select a condition",
        reply_markup=create_search_command_keyboard(search_condition)
    )

    await state.set_state(SelectCond.custom_state)
