import discord
import json

from pathlib import Path
from peewee import SqliteDatabase

# database is created in parent directory of this file
BOT_DB = SqliteDatabase(Path(__file__).parent.parent / 'birthdaybot.db')

try:
    with (Path(__file__).parent.parent / 'token.json').open() as tf:
        BOT_TOKEN = json.load(tf)["token"]

except FileNotFoundError:
    raise Exception("token.json was not found")
except KeyError:
    raise Exception("token.json does not contain a 'token' key")