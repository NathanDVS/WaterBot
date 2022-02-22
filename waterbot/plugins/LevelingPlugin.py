import hikari
import lightbulb
from waterbot.utils import Utils

plugin = lightbulb.Plugin("Leveling")

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.option(name="member", description="A member in the server.", required=False, type=hikari.Member)
@lightbulb.command("rank", "Shows the members rank on the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def rank_command(ctx: lightbulb.SlashContext):
    user: hikari.Member = ctx.member
    collection = Utils.get_database().load_collection("Users")

    if ctx.options.member:
        user = ctx.options.member

    xp = collection.get_or_default({ "Guild": ctx.get_guild().id, "User": user.id }, "Xp", 0)
    level = collection.get_or_default({ "Guild": ctx.get_guild().id, "User": user.id }, "Level", 1)

    embed = Utils.embed(ctx)

    if user.avatar_url != None:
        embed.set_author(name=f"{user.username}#{user.discriminator} Rank", icon=user.avatar_url.url)
    else:
        embed.set_author(name=f"{user.username}#{user.discriminator} Rank")

    embed.description = f"**Level: `Level {level}`**\n**Xp: `{xp} Xp`**"

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.command("levels", "Shows the leveling leaderboard for the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def levels_command(ctx: lightbulb.SlashContext):
    text = ""
    embed = Utils.embed(ctx)

    collection = Utils.get_database().load_collection("Users")
    raw_lb = collection.leaderboard({ "Guild": ctx.get_guild().id }, [("Xp", -1)], 5)

    if ctx.get_guild().icon_url != None:
        embed.set_author(name=f"{ctx.get_guild().name} Leveling Leaderboard", icon=ctx.get_guild().icon_url.url)
    else:
        embed.set_author(name=f"{ctx.get_guild().name} Leveling Leaderboard")
    
    count = 0

    for entry in raw_lb:
        user = ctx.bot.cache.get_user(entry['User'])

        try:
            text += f"**`{count + 1}.` {user.username}#{user.discriminator} - `Level {entry['Level'] or 0}`/`{entry['Xp'] or 0} Xp`**\n"
            count += 1
        except:
            continue

    if text != "":
        embed.description = text
    else:
        embed.description = "**There are no users on the leaderboard.**"

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.command("global-levels", "Shows the global leveling leaderboard.")
@lightbulb.implements(lightbulb.SlashCommand)
async def global_levels_command(ctx: lightbulb.SlashContext):
    text = ""
    embed = Utils.embed(ctx)

    collection = Utils.get_database().load_collection("Users")
    raw_lb = collection.leaderboard({}, [("Xp", -1)], 5)

    embed.set_author(name=f"Global Leveling Leaderboard", icon=ctx.get_guild().get_member(881566888897957909).avatar_url.url)
    
    count = 0

    for entry in raw_lb:
        user = ctx.bot.cache.get_user(entry['User'])

        try:
            text += f"**`{count + 1}.` {user.username}#{user.discriminator} - `Level {entry['Level'] or 0}`/`{entry['Xp'] or 0} Xp`**\n"
            count += 1
        except:
            continue

    if text != "":
        embed.description = text
    else:
        embed.description = "**There are no users on the leaderboard.**"

    await ctx.respond(embed)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)