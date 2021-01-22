# check if user has admin rights to the bot
def check_owner(ctx):
    if ctx.author.id in ctx.bot.owner_ids:
        return True
    return False

