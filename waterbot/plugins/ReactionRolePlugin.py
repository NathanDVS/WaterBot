import hikari
import lightbulb
import hikari.channels
from lightbulb import checks
from waterbot.utils import Utils

plugin = lightbulb.Plugin("Reaction Role")

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option(name="emoji", description="A emoji.", required=True, type=str)
@lightbulb.option(name="role_id", description="The id for a role.", required=True, type=int)
@lightbulb.option(name="message_id", description="The id for a message.", required=True, type=int)
@lightbulb.option(name="channel", description="A text channel.", required=True, type=hikari.channels.TextableGuildChannel)
@lightbulb.command(name="reaction-role-add", description="Creates a reaction role.")
@lightbulb.implements(lightbulb.SlashCommand)
async def reaction_role_add_command(ctx: lightbulb.SlashContext):
    embed = Utils.embed(ctx)
    collection = Utils.get_database().load_collection("ReactionRoles")

    channel: hikari.channels.TextableGuildChannel = ctx.options.channel

    message = await channel.fetch_message(int(ctx.options.message_id))
    role = await ctx.get_guild().get_role(int(ctx.options.role_id))

    parsed_emoji: str = ctx.options.emoji

    if parsed_emoji.__contains__("<"):
        parsed_emoji = ":" + parsed_emoji.split(":")[1] + ":"

    embed.description = f"**Reaction Role Created!\n[Go To Message](https://discord.com/channels/{ctx.message.guild.id}/{channel.id}/{message.id})\n`Role:` {role.name}\n`Emoji:` {parsed_emoji}\n`Channel:` {channel.name.title()}**"

    await message.add_reaction(parsed_emoji)

    collection.create({
        "Guild": message.guild.id,
        "Message": message.id,
        "Channel": channel.id,
        "Emoji": parsed_emoji,
        "Role": role.id,
    })

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option(name="emoji", description="A emoji.", required=True)
@lightbulb.option(name="message_id", description="The id for a message.", required=True)
@lightbulb.option(name="channel", description="A text channel.", required=True, type=hikari.channels.TextableGuildChannel)
@lightbulb.command(name="reaction-role-delete", description="Deletes a reaction role.")
@lightbulb.implements(lightbulb.SlashCommand)
async def reaction_role_delete_command(ctx: lightbulb.SlashContext):
    embed = Utils.embed(ctx)
    collection = Utils.get_database().load_collection("ReactionRoles")

    channel: hikari.channels.TextableGuildChannel = ctx.options.channel
    message = await channel.fetch_message(int(ctx.options.message_id))
    parsed_emoji: str = ctx.options.emoji

    if parsed_emoji.__contains__("<"):
        parsed_emoji = ":" + parsed_emoji.split(":")[1] + ":"

    await message.clear_reaction(ctx.options.emoji)

    collection.delete({
        "Message": message.id,
        "Channel": channel.id,
        "Emoji": parsed_emoji,
    })

    embed.description = "**Removed the reaction role.**"

    await ctx.respond(embed)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)