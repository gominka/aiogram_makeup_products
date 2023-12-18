import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Environment variables are not loaded because the .env file is missing")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_NAME = os.getenv("DB_NAME")

DEFAULT_COMMANDS = (
    ("start", "Start the search"),
    ("brand", "Brand selection"),
    ("product_tag", "Tag selection"),
    ("product_type", "Type selection"),
    ("start_again", "Start again")
)