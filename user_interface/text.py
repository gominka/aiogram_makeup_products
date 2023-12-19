from user_interface import emoji

MAIN_COMMANDS = f"\n\n {emoji.start_condition['brand']} /brand - Select a brand" \
                f"\n\n {emoji.start_condition['product_tag']} /product_tag - Select a tag" \
                f"\n\n {emoji.start_condition['product_type']} /product_type - Select a type"

SEARCH_COMMANDS = f"\n\n{emoji.search_condition['high']} /high - Set a maximum price or rating" \
                  f"\n\n{emoji.search_condition['low']} /low - Set a minimum price or rating"\
                  f"\n\n{emoji.addition_condition['start_again']} /start_again - Start over"


START_MSG = "Welcome to Telegram Bot!" \
            "\n\n Select a condition to start the search: " + MAIN_COMMANDS

HELP_MSG = "List of available commands:" + MAIN_COMMANDS

CONDITION = "Select the command:" + MAIN_COMMANDS + SEARCH_COMMANDS

DESCRIPTION = "Name: {}\n\n" \
              "Price: {}\n\n" \
              "Product Description:\n" \
              "{}\n\n" \
              "Product Link:\n" \
              "{}"
