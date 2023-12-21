from asyncio.log import logger

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database.models import User
from states.custom_states import StartState

from user_interface import text

start_router = Router()


def get_user_info(message: types.Message) -> tuple:
    """Retrieve user information from a Telegram message."""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    return user_id, username, first_name, last_name


@start_router.message(Command(commands=["start"]))
async def start_command_handler(message: types.Message, state: FSMContext) -> None:
    """Handler for the /start command."""
    user_id, username, first_name, last_name = get_user_info(message)

    await state.set_state(StartState.start_state)
    try:
        User(user_id=user_id, username=username, first_name=first_name, last_name=last_name).save()
        logger.info(f'A new user has been added. User_id: {user_id}')
        await message.reply(text.START_MSG)
    except Exception:
        await message.answer(text=text.HELP_MSG)




@start_router.message(Command("start_again"))
async def start_command_handler(message: types.Message, state: FSMContext) -> None:
    """Handler for the /start_again command."""

    user_id, _, _, _ = get_user_info(message)

    await message.reply(text="Previously selected conditions have been reset")
    await state.clear()
    await message.answer(text=text.HELP_MSG)
