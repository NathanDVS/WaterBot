import hikari
import lightbulb
from waterbot.utils import Hypixel, Utils
from hikari.messages import MessageFlag

plugin = lightbulb.Plugin("Owner")

@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("update-presence", "Updates the bots presence.")
@lightbulb.implements(lightbulb.SlashCommand)
async def update_presence_command(ctx: lightbulb.SlashContext):
    guilds = len(await ctx.app.rest.fetch_my_guilds())
    
    if guilds == 1:
        await ctx.bot.update_presence(activity=hikari.Activity(name=f"/help || {guilds} server", type=hikari.ActivityType.PLAYING), status=hikari.Status.DO_NOT_DISTURB)
    else:
        await ctx.bot.update_presence(activity=hikari.Activity(name=f"/help || {guilds} servers", type=hikari.ActivityType.PLAYING), status=hikari.Status.DO_NOT_DISTURB)

    await ctx.respond(Utils.quick_embed("**The bot has now updated its presence.**", ctx), flags=MessageFlag.EPHEMERAL)

@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("shutdown", "Shuts the bot down.")
@lightbulb.implements(lightbulb.SlashCommand)
async def shutdown_command(ctx: lightbulb.SlashContext):
    await ctx.respond(Utils.quick_embed("**The bot is shutting down ...**", ctx), flags=MessageFlag.EPHEMERAL)
    await ctx.bot.close()

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)
