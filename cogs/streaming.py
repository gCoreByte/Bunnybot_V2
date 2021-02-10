import datetime

import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter

from utils.checks import check_owner
from utils.database import check_if_connected
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
        # TODO: autodelete message when stream over
        if not streaming_after:
            return
        # user has just started streaming, check if they are in db
        guild_id = before.guild.id
        self.bot.db = check_if_connected(self.bot.db)
        cursor = self.bot.db.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM `{guild_id}` WHERE is_streamer = 1 AND user_id = %s", (before.id,))
        row = cursor.fetchone()
        if row is None:
            return
        cursor.close()
        # get channel to send streaming notif to
        cursor = self.bot.db.cursor(dictionary=True)
        cursor.execute("SELECT stream_channel FROM guild_data WHERE guild_id = %s", (guild_id,))
        channel_id = cursor.fetchone()["stream_channel"]
        channel = discord.utils.get(before.guild.text_channels, id=channel_id)
        # getting link
        if streaming_after:
            streaming_obj = None
            for i in after.activities:
                if isinstance(i, discord.Streaming):
                    streaming_obj = i
                    break
        # build the embed
        link = streaming_obj.url
        embed = discord.Embed(
            title=f"{before.name} is now streaming!",
            timestamp=datetime.datetime.now(),
            colour=0x967bb6,
            url=link,
            description=streaming_obj.url
        )
        embed.set_image(url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{streaming_obj.twitch_name}-1920x1080.jpg")
        # send the embed
        await channel.send(content="@everyone", embed=embed)

    @commands.check(check_owner)
    @commands.command()
    async def add_streamer(self, ctx, name):
        # check if given name is id:
        try:
            member = await MemberConverter().convert(ctx, name)
        except:
            await ctx.send(f"There are no matches for {name}, looking for partial name matches", delete_after=15)
            try:
                member = find_by_partial(name, ctx.guild)
            except TooManyMatches:
                await ctx.send(f"There are too many matches for the name {name}", delete_after=15)
                return
            except NoMatchFound:
                await ctx.send(f"There were no matches for the name {name}", delete_after=15)
                return
        # lets add the new streamers ID to the database
        try:
            self.bot.db = check_if_connected(self.bot.db)
            cursor = self.bot.db.cursor()
            cursor.execute(f"UPDATE `{ctx.guild.id}` SET is_streamer = 1 WHERE user_id = %s", (member.id,))
            cursor.close()
            self.bot.db.commit()
            await ctx.send("Added user to DB.", delete_after=15)
        except Exception as e:
            print(e)
            await ctx.send("Error adding user to DB. This shouldn't happen!")
            await ctx.send(e)

    @commands.check(check_owner)
    @commands.command()
    async def remove_streamer(self, ctx, name):
        try:
            member = await MemberConverter().convert(ctx, name)
        except:
            await ctx.send(f"There are no matches for {name}, looking for partial name matches", delete_after=15)
            try:
                member = find_by_partial(name, ctx.guild)
            except TooManyMatches:
                await ctx.send(f"There are too many matches for the name {name}", delete_after=15)
                return
            except NoMatchFound:
                await ctx.send(f"There were no matches for the name {name}", delete_after=15)
                return
        # remove the streamers ID from the database
        try:
            self.bot.db = check_if_connected(self.bot.db)
            cursor = self.bot.db.cursor()
            cursor.execute(f"UPDATE `{ctx.guild.id}` SET is_streamer = 0 WHERE user_id = %s", (member.id,))
            cursor.close()
            self.bot.db.commit()
            await ctx.send("Removed user from DB.", delete_after=15)
        except:
            await ctx.send("Error removing user from DB. This shouldn't happen!")
