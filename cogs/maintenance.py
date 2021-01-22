from discord.ext import commands
from discord.ext.commands import ExtensionNotFound

from utils.checks import check_owner


def setup(bot):
    bot.add_cog(Maintenance(bot))


class Maintenance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(check_owner)
    def reload_cog(self, ctx, cog):
        try:
            self.bot.reload_extension(f"cogs.{cog}")
        except ExtensionNotFound as e:
            await ctx.send(f"Cog {cog} does not exist.", delay=15)
        except Exception as e:
            await ctx.send(f"Error loading cog {cog}, check console.", delay=15)
        else:
            await ctx.send(f"Reloaded cog {cog} successfully.", delay=15)

    @commands.command()
    @commands.check(check_owner)
    def status(self, ctx):
        #TODO:
        # database status
        # cpu load
        # memory
        # uptime
        pass
