import asyncio
import tracemalloc
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
    user = message.from_user
    return user.id, user.username, user.first_name, user.last_name


async def add_new_user(user_id, username, first_name, last_name):
    try:
        User(user_id=user_id, username=username, first_name=first_name, last_name=last_name).save()
        logger.info(f'A new user has been added. User_id: {user_id}')
    except Exception as e:
        logger.error(f'Error adding a new user. User_id: {user_id}, Error: {str(e)}')


@start_router.message(Command(commands=["start"]))
async def start_command_handler(message: types.Message, state: FSMContext) -> None:
    """Handler for the /start command."""
    user_id, username, first_name, last_name = get_user_info(message)

    if not User.get_or_create(user_id=user_id):
        await add_new_user(user_id, username, first_name, last_name)
        await message.reply(text.START_MSG)
    else:
        await message.answer(text=text.HELP_MSG)

    await state.set_state(StartState.start_state)


@start_router.message(Command("start_again"))
async def start_command_handler(message: types.Message, state: FSMContext) -> None:
    """Handler for the /start_again command."""
    tracemalloc.start()
    await message.reply(text="Previously selected conditions have been reset")
    await state.clear()

    await message.answer(text=text.HELP_MSG)
