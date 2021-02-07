from discord.ext import commands


def setup(bot):
    bot.add_cog(Newmember(bot))


class Newmember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot