from discord.ext import commands
from utils.checks import check_manage_roles


def setup(bot):
    bot.add_cog(Moderation(bot))


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(check_manage_roles)
    async def set_member_xp(self, ctx, name, xp):
        #TODO
        pass

    @commands.command()
    @commands.check(check_manage_roles)
    async def purge(self, ctx, amount=10):
        #TODO
        pass

    @commands.command()
    @commands.check(check_manage_roles)
    async def mute(self, ctx, name, duration=10, unit="min", reason=None):
        #TODO
        pass

    @commands.command()
    @commands.check(check_manage_roles)
    async def mute_voice(self, ctx, name, duration=10, unit="min", reason=None):
        #TODO
        pass

    @commands.command()
    @commands.check(check_manage_roles)
    async def kick(self, ctx, name, reason=None):
        #TODO
        pass

    @commands.command()
    @commands.check(check_manage_roles)
    async def ban(self, ctx, name, reason=None):
        #TODO
        pass