from asyncio.log import logger
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database.models import User
from handlers.default_handlers.exception_handler import error_handler
from site_ip.main_request import BASE_PARAMS
from states.custom_states import StartState
from user_interface import text

start_router = Router()


def get_user_info(message: types.Message) -> tuple:
    """Retrieve user information from a Telegram message."""
    user = message.from_user
    return user.id, user.username, user.first_name, user.last_name


@start_router.message(Command(commands=["start"]))
@error_handler
async def start_command_handler(message: types.Message, state: FSMContext) -> None:
    """Handler for the /start command."""
    user_id, username, first_name, last_name = get_user_info(message)

    if not User.get_or_create(user_id=user_id):
        User(user_id=user_id, username=username, first_name=first_name, last_name=last_name).save()
        logger.info(f'A new user has been added. User_id: {user_id}')

        await message.reply(text.START_MSG)
    else:
        await message.answer(text=text.HELP_MSG)

    await state.set_state(StartState.start_state)
    await state.update_data(params=BASE_PARAMS)


@start_router.message(Command("start_again"))
@error_handler
async def start_command_handler(message: types.Message, state: FSMContext) -> None:
    """Handler for the /start_again command."""
    await message.reply(text="Previously selected conditions have been reset")
    await state.clear()
    await state.update_data(params=BASE_PARAMS)
    await message.answer(text=text.HELP_MSG)
