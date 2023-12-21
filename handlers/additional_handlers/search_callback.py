from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from database.models import Selections
from keyboards.inline.search_keyboards import create_website_link_keyboard
from site_ip.main_request import make_response, get_conditions_list
from states.custom_states import FinalCond, SelectCond
from user_interface import text
from user_interface.text import DESCRIPTION

search_call_router = Router()


@search_call_router.callback_query(F.data == "check_amount_products")
async def check_amount_products_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Handle the 'check_amount_products' callback."""

    user_data = await state.get_data()
    params = user_data["params"]
    response = make_response(params=user_data["params"])
    selected_product = make_response(params=params)[0]

    if len(response) == 1:
        Selections(user_id=callback.from_user.id, product_name=selected_product["name"]).save()
        await callback.message.answer(text=DESCRIPTION.format(
            selected_product["name"],
            selected_product["price"],
            selected_product["description"],
            selected_product["product_link"]))

    elif 1 <= len(response) <= 3:
        buttons = [
            types.InlineKeyboardButton(text=condition, callback_data=condition)
            for condition in get_conditions_list(params=user_data["params"], selected_condition="list_name_product")
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 5] for i in range(0, len(buttons), 5)])
        await callback.message.answer(text="Select a name:", reply_markup=keyboard)

        await state.set_state(FinalCond.final_selection)

    else:
        await callback.message.answer(
            text=text.CONDITION)


@search_call_router.callback_query(FinalCond.final_selection)
async def callback_search_command(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Processing button clicks, condition selection"""

    user_data = await state.get_data()
    user_data["params"]["name"] = callback.data
    params = user_data["params"]
    selected_product = make_response(params=params)[0]

    print(user_data)

    Selections(user_id=callback.from_user.id, product_name=selected_product["name"]).save()
    await callback.message.answer(text=DESCRIPTION.format(
        selected_product["name"],
        selected_product["price"],
        selected_product["description"],
        selected_product["product_link"]))

    await state.set_state(FinalCond.final_selection)


@search_call_router.callback_query(F.data == "cancel_search_cond")
async def call_btn_file(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SelectCond.choosing_condition)

    await callback.message.delete()


@search_call_router.callback_query(F.data == "website_link")
async def handle_website_link_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Processing of a button click, a link to the site"""

    user_data = await state.get_data()

    urlkb = create_website_link_keyboard(make_response(params=user_data["params"])[0][callback.data])

    await callback.message.answer(
        text="To visit the website, click the button below", reply_markup=urlkb)
