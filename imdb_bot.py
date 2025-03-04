#!/usr/bin/env python3
from pyrogram import Client
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.filters import command, regex
# ... rest of your existing imports ...

# Add this import if missing
from pyrogram import Client, filters

# Your existing code
from contextlib import suppress
from re import findall, IGNORECASE
from imdb import Cinemagoer
from pycountry import countries as conn
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from config import config_dict

imdb = Cinemagoer()

# Initialize the Client properly
bot = Client(
    "imdb_bot",
    api_id=config_dict.API_ID,
    api_hash=config_dict.API_HASH,
    bot_token=config_dict.BOT_TOKEN
)

# ... rest of your existing code ...
