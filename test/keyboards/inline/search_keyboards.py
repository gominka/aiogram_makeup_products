from keyboa.keyboards import keyboa_maker
from telebot import types
from site_ip.main_request import get_conditions_list

# Constants
CONTINUE_SEARCH_CALLBACK = "check_amount_products"
CANCEL_SEARCH_CALLBACK = "cancel_search_cond"
WEBSITE_LINK_CALLBACK = "website_link"
GO_TO_WEBSITE_TEXT = 'Go to the website'
CANCEL_TEXT = 'Cancel'


def create_name_selection_keyboard(params, selected_condition):
    """
    Create a custom keyboard using keyboa_maker with conditions.

    :param params: List of conditions.
    :param selected_condition: The currently selected condition.
    :return: InlineKeyboardMarkup.
    """
    # Use the conditions_list to generate the keyboard
    return keyboa_maker(items=get_conditions_list(params=params, selected_condition=selected_condition),
                        copy_text_to_callback=True, items_in_row=5)


def create_search_command_keyboard(search_cond):
    """
    Create an inline keyboard for search commands.

    :param search_cond: The current search condition.
    :return: InlineKeyboardMarkup.
    """
    search_command_markup = types.InlineKeyboardMarkup(row_width=2)
    custom_search = types.InlineKeyboardButton(text='Continue the search', callback_data=CONTINUE_SEARCH_CALLBACK)
    cancel = types.InlineKeyboardButton(text=CANCEL_TEXT, callback_data=CANCEL_SEARCH_CALLBACK)

    if search_cond == "brand":
        website = types.InlineKeyboardButton(text=GO_TO_WEBSITE_TEXT, callback_data=WEBSITE_LINK_CALLBACK)
        search_command_markup.add(custom_search, website)
    else:
        search_command_markup.add(custom_search)

    search_command_markup.add(cancel)

    return search_command_markup


def create_website_link_keyboard(link):
    """Create a keyboard for a website link."""
    urlkb = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text=GO_TO_WEBSITE_TEXT, url=link)
    cancel_button = types.InlineKeyboardButton(text=CANCEL_TEXT, callback_data='cancel')
    urlkb.add(url_button, cancel_button)
    return urlkb


def create_command_keyboard():
    search_command_markup = types.InlineKeyboardMarkup(row_width=3)
    custom_search = types.InlineKeyboardButton(text='Continue the search', callback_data=CONTINUE_SEARCH_CALLBACK)
    cancel = types.InlineKeyboardButton(text=CANCEL_TEXT, callback_data=CANCEL_SEARCH_CALLBACK)
    search_command_markup.add(custom_search, cancel)
    return search_command_markup
