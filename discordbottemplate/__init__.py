import discord
import json

from pathlib import Path

from .bot import client
from .cogs import *

try:
    with (Path(__file__).parent.parent / 'token.json').open() as tf:
        BOT_TOKEN = json.load(tf)["token"]

except FileNotFoundError:
    raise Exception("token.json was not found")
except KeyError:
    raise Exception("token.json does not contain a 'token' key")