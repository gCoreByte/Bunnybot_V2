from discord.ext import commands


def setup(bot):
    bot.add_cog(Firstjoin(bot))


class Firstjoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        # TODO

        pass

    async def on_guild_join(self, guild):
        # TODO
        pass

    async def on_member_ban(self, guild, member):
        # TODO
        pass