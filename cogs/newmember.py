def setup(bot):
    bot.add_cog(Newmember(bot))


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot