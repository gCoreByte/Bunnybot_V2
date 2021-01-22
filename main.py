import json
import discord
from discord.ext import commands

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
bot.load_extension("cogs.newmember")

# start bot

with open("config.json") as f:
    data = json.load(f)
    secret = data["discord"]["secret"]
bot.run(secret)