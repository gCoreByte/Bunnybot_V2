import datetime

from discord import Embed
from discord.ext import commands
from discord.ext.commands import ExtensionNotFound
import psutil
from utils.checks import check_owner


def setup(bot):
    bot.add_cog(Maintenance(bot))


class Maintenance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(check_owner)
    async def reload_cog(self, ctx, cog):
        try:
            self.bot.reload_extension(f"cogs.{cog}")
        except ExtensionNotFound as e:
            await ctx.send(f"Cog {cog} does not exist.", delete_after=15)
        except Exception as e:
            await ctx.send(f"Error loading cog {cog}, check console.", delete_after=15)
        else:
            await ctx.send(f"Reloaded cog {cog} successfully.", delete_after=15)

    @commands.command()
    @commands.check(check_owner)
    async def status(self, ctx):
        #TODO:
        # database status
        cpu_load = psutil.cpu_percent()
        mem_stats = psutil.virtual_memory()
        uptime = datetime.datetime.now() - self.bot.start_time
        embed = Embed(
            title="Bot status",
            timestamp=datetime.datetime.now(),
            colour=0x967bb6
        )
        embed.add_field(name="CPU load", value=f"{cpu_load}%", inline=False)
        embed.add_field(name="Memory stats", value=f"{mem_stats[2]}%", inline=False)
        embed.add_field(name="Uptime", value=str(uptime - datetime.timedelta(microseconds=uptime.microseconds)), inline=False)
        await ctx.send(embed=embed)
