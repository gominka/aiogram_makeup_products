from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from site_ip.main_request import get_conditions_list



def create_search_command_keyboard(search_cond):
    """
    Create an inline keyboard for search commands.

    :param search_cond: The current search condition.
    :return: InlineKeyboardMarkup.
    """
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Continue the search",
        callback_data="check_amount_products"
    )

    builder.button(
        text="Cancel",
        callback_data="cancel_search_cond"
    )

    if search_cond == "brand":
        builder.button(
            text="Go to the website",
            callback_data="website_link"
        )
    builder.adjust(4)

    return builder.as_markup()


def create_website_link_keyboard(link):
    """Create a keyboard for a website link."""

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Go to the website",
        url=link)
    )
    builder.row(types.InlineKeyboardButton(
        text="Cancel",
        callback_data="cancel")
    )

    return builder.as_markup()


def create_command_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text='Continue the search',
                                       callback_data="check_amount_products"),
            types.InlineKeyboardButton(text="Cancel",
                                       callback_data="cancel_search_cond")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
