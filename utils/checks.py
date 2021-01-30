# check if user has admin rights to the bot
def check_owner(ctx):
    if ctx.author.id in ctx.bot.owner_ids:
        return True
    return False

# check if user has manage_roles perm
def check_manage_roles(ctx):
    return ctx.author.guild_permissions.manage_roles

