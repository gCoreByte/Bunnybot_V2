import json
import datetime
import sys
from pathlib import Path
import logging

import discord
from discord.ext import commands
from utils.database import connect_to_database
# initialize intents


intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)

# add cogs

bot.load_extension("cogs.maintenance")
bot.load_extension("cogs.ranking")
bot.load_extension("cogs.moderation")
bot.load_extension("cogs.streaming")
bot.load_extension("cogs.firstjoin")

# load bot variables

bot.root_dir = Path(sys.modules["__main__"].__file__).resolve().parent
bot.db = connect_to_database()
bot.start_time = datetime.datetime.now()
bot.owner_ids = set()

# prepare logging

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename=bot.root_dir / 'discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# start bot

with open(bot.root_dir / "config" / "config.json") as f:
    data = json.load(f)
    secret = data["discord"]["secret"]
    for owner_id in data["owners"]:
        bot.owner_ids.add(int(owner_id))
bot.run(secret)

