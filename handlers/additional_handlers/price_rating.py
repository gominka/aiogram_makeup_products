from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from keyboards.inline.search_keyboards import create_command_keyboard
from keyboards.reply import reply_keyboards
from states.custom_states import SelectCond

cond_router = Router()


async def handle_search_command(message, condition_suffix, state: FSMContext):
    await state.update_data(cond2=f"_{condition_suffix}")

    await state.set_state(SelectCond.number_selection)
    builder = ReplyKeyboardBuilder()

    builder.row(
        types.KeyboardButton(text="rating"),
        types.KeyboardButton(text="price")
    )
    await message.answer("Choose a condition: ", reply_markup=builder.as_markup(resize_keyboard=True))


@cond_router.message(Command(commands=['high', 'low']))
async def main_search_command(message: types.Message, state: FSMContext) -> None:
    """Handler triggered by the command /high, /low"""

    await handle_search_command(message, "less_than" if message.text[1:] == "high" else "greater_than", state)


@cond_router.callback_query(SelectCond.number_selection)
async def select_condition(message: types.Message, state: FSMContext) -> None:

    await state.update_data(cond1=message.text)
    await state.set_state(SelectCond.check_number_selection)

    await message.answer("Enter a number: ", reply_markup=reply_keyboards.EMPTY)


@cond_router.callback_query(SelectCond.check_number_selection)
async def select_cond(message: types.Message, state: FSMContext) -> None:
    msg_user = int(message.text)
    user_data = await state.get_data()

    if (user_data["cond1"] == "rating" and 1 <= msg_user <= 10) or user_data["cond1"] == "price":
        cond = user_data["cond1"] + user_data["cond2"]
        user_data["params"][cond] = msg_user

        search_command_markup = create_command_keyboard()

        await state.set_state(SelectCond.custom_state)
        await message.answer("Select a condition: ", reply_markup=search_command_markup)

    elif user_data["cond1"] == "rating":
        await state.set_state(SelectCond.number_selection)
        await message.answer("The number must be from 1 to 10: ", reply_markup=reply_keyboards.EMPTY)

        await select_condition(message)
