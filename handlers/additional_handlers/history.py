from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.models import History
from handlers.additional_handlers.search_callback import send_product_details
from site_ip.main_request import BASE_PARAMS, make_response
from states.custom_states import SelectCond

history_router = Router()


async def get_product_names(user_id: int) -> list:
    """Retrieve product names for a given user."""
    product_names = set([name.product_name for name in History.select().where(History.user_id == user_id)])
    return list(product_names)


async def send_history_message(message: types.Message, product_names: list) -> None:
    """Send a message with the user's history."""
    message_text = "You have previously selected the following products:\n\n"

    buttons = [
        types.InlineKeyboardButton(text=condition, callback_data=condition)
        for condition in product_names
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 5] for i in range(0, len(buttons), 5)])
    await message.answer(text=message_text, reply_markup=keyboard)


@history_router.message(Command("history"))
async def start_command_handler(message: types.Message, state: FSMContext) -> None:
    """Handler for the /history command."""

    product_names = await get_product_names(message.from_user.id)

    await send_history_message(message, product_names)
    await state.set_state(SelectCond.product_details)


@history_router.callback_query(SelectCond.product_details)
async def callback_search_command(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Processing button clicks, name product selection"""

    params = BASE_PARAMS
    params["name"] = callback.data
    response = make_response(params=params)
    await send_product_details(callback, response[0])
    await state.set_state(SelectCond.custom_state)
