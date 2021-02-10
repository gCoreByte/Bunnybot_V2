from discord.ext import commands


def setup(bot):
    bot.add_cog(Firstjoin(bot))


class Firstjoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot