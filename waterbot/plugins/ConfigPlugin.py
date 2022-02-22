from typing import Literal
import hikari
import lightbulb
from lightbulb import checks
from waterbot.utils import Utils

plugin = lightbulb.Plugin("Config")

@plugin.command
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option(name="channel", description="When someone levels up it will be announced in this channel.", type=hikari.TextableGuildChannel | Literal['none'], required=True)
@lightbulb.command("set-leveling-channel", "Set the leveling channel.")
@lightbulb.implements(lightbulb.SlashCommand)
async def set_leveling_channel_command(ctx: lightbulb.SlashContext):
    collection = Utils.get_database().load_collection("Guilds")
    channel: hikari.TextableGuildChannel = ctx.options.channel

    collection.update({
        "Guild": ctx.guild_id
    }, {
        "LevelingChannel": channel.id
    })

    await ctx.respond(Utils.quick_embed(f"**The leveling channel has now been set to `{channel.name}`!**", ctx))

@plugin.command
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option(name="role_id", description="A roles id.", required=True)
@lightbulb.option(name="level", description="The level you want to give the role.", required=True)
@lightbulb.command("add-auto-role", "Add auto role to the leveling system.")
@lightbulb.implements(lightbulb.SlashCommand)
async def add_auto_role_command(ctx: lightbulb.SlashContext):
    level = int(ctx.options.level)
    role = ctx.get_guild().get_role(ctx.options.role_id)

    collection = Utils.get_database().load_collection("Guilds")
    collection.push({ "Guild": ctx.guild_id }, "LevelingAutoRoles", { "Role": role.id, "Level": level })

    await ctx.respond(Utils.quick_embed(f"**Now when someone hits `level {level}` they will receive the following role: `{role.name}`!**", ctx))

@plugin.command
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option(name="role_id", description="A roles id.", required=True)
@lightbulb.option(name="level", description="The level you want to give the role.", required=True)
@lightbulb.command("remove-auto-role", "Remove auto role from the leveling system.")
@lightbulb.implements(lightbulb.SlashCommand)
async def remove_auto_role_command(ctx: lightbulb.SlashContext):
    level = int(ctx.options.level)
    role = ctx.get_guild().get_role(ctx.options.role_id)

    collection = Utils.get_database().load_collection("Guilds")
    auto_roles = collection.get_or_default({ "Guild": ctx.guild_id }, "LevelingAutoRoles", [])

    for auto_role in auto_roles:
        if auto_role["Level"] == level:
            role_to_give = ctx.get_guild().get_role(auto_role["Role"])
            if role_to_give.id == role.id:
                del auto_role
                break

    collection.update({ "Guild": ctx.guild_id }, { "LevelingAutoRoles": auto_roles })

    await ctx.respond(Utils.quick_embed(f"**Now when someone hits `level {level}` they will receive no role!**", ctx))

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)
