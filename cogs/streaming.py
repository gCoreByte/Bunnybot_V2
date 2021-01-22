import discord
from discord.ext import commands

from utils.checks import check_owner
from utils.exceptions import TooManyMatches, NoMatchFound
from utils.utility_functions import find_by_partial


def setup(bot):
    bot.add_cog(Streaming(bot))


class Streaming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # check if the update is streaming to reduce DB reads
        streaming_before = any(isinstance(x, discord.Streaming) for x in before.activities)
        streaming_after = any(isinstance(x, discord.Streaming) for x in after.activities)
        if streaming_before == streaming_after:
            return
        if not streaming_after:
            return
        # user has just started streaming, check if they are in db
        # TODO: check if in DB

    @commands.check(check_owner)
    @commands.command()
    def add_streamer(self, ctx, name):
        # check if given name is id:
            #TODO
        try:
            member = find_by_partial(name, ctx.guild)
        except TooManyMatches:
            await ctx.send(f"There are too many matches for the name {name}", delay=15)
            return
        except NoMatchFound:
            await ctx.send(f"There were no matches for the name {name}", delay=15)
            return
        # lets add the new streamers ID to the database
        # TODO: add streamer to database

    @commands.check(check_owner)
    @commands.command()
    def remove_streamer(self, ctx, name):
        # check if given name is id:
        # TODO
        try:
            member = find_by_partial(name, ctx.guild)
        except TooManyMatches:
            await ctx.send(f"There are too many matches for the name {name}", delay=15)
            return
        except NoMatchFound:
            await ctx.send(f"There were no matches for the name {name}", delay=15)
            return
        # remove the streamers ID from the database
        # TODO: remove streamer from database