from discord.ext import commands


def setup(bot):
    bot.add_cog(Ranking(bot))


class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot