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
        f = open("test1.txt", "a")
        # check if the update is streaming to reduce DB reads
        streaming_before = any(isinstance(x, discord.Streaming) for x in before.activities)
        streaming_after = any(isinstance(x, discord.Streaming) for x in after.activities)
        if streaming_before == streaming_after and not streaming_after:
            return
        if not streaming_after:
            return
        f.write(f"STREAMING UPDATE AS {after.id}")
        f.write(f"Streaming before: {streaming_before}")
        f.write(f"Streaming after: {streaming_after}")
        # user has just started streaming, check if they are in db
        f.write(str(1))
        guild_id = before.guild.id
        self.bot.db = check_if_connected(self.bot.db)
        cursor = self.bot.db.cursor(dictionary=True)
        f.write(str(2))
        cursor.execute(f"SELECT * FROM `{guild_id}` WHERE is_streamer = 1 AND user_id = %s", (before.id,))
        row = cursor.fetchone()
        f.write(str(3)+"\n")
        f.write(str(row))
        if row is None:
            f.write(f"USER {after.id} IS NOT IN DB\n")
            return
        cursor.close()
        f.write(str(4))
        # get channel to send streaming notif to
        cursor = self.bot.db.cursor(dictionary=True)
        f.write(str(5))
        cursor.execute("SELECT stream_channel FROM guild_data WHERE guild_id = %s", (guild_id,))
        f.write(str(6))
        f.write(str(7))
        channel_id = cursor.fetchone()["stream_channel"]
        f.write(str(8))
        f.write(str(channel_id))
        channel = discord.utils.get(before.guild.text_channels, id=channel_id)
        f.write(str(9))
        # getting link
        f.write(str(10))
        streaming_obj = None
        if streaming_after:
            for i in after.activities:
                f.write(str(i))
                if isinstance(i, discord.Streaming):
                    print(str(11))
                    streaming_obj = i
                    break
        f.write("BUILDING EMBED\n")
        # build the embed
        f.write(str(12))
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
        self.bot.db = check_if_connected(self.bot.db)
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
