import hikari
import asyncio
import datetime
import lightbulb
import humanfriendly
from lightbulb import checks
from waterbot.utils import Utils
from hikari.messages import MessageFlag

plugin = lightbulb.Plugin("Moderation")

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.option(name="reason", description="The reason for kicking the member from the server.", required=False)
@lightbulb.option(name="member", description="A member in the server.", required=True, type=hikari.Member)
@lightbulb.command(name="kick", description="Kick a member from the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def kick_command(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx.options.member
    reason: str = "Unspecified"

    if ctx.options.reason:
        reason = ctx.options.reason

    author_tag = f"{ctx.author.username}#{ctx.author.discriminator}"
    member_tag = f"{member.username}#{member.discriminator}"

    embed = Utils.embed(ctx)

    embed.title = "Member Kicked!"
    embed.add_field(name="Who was kicked", value=f"**`{member_tag}`**")
    embed.add_field(name="Kicked by", value=f"**`{author_tag}`**")
    embed.add_field(name="Reason", value=f"**`{reason}`**", inline=False)
    
    await member.kick(reason=reason)
    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option(name="reason", description="The reason for banning the member from the server.", required=False)
@lightbulb.option(name="member", description="A member in the server.", required=True, type=hikari.Member)
@lightbulb.command(name="ban", description="Ban a member from the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ban_command(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx.options.member
    reason: str = "Unspecified"

    if ctx.options.reason:
        reason = ctx.options.reason

    author_tag = f"{ctx.author.username}#{ctx.author.discriminator}"
    member_tag = f"{member.username}#{member.discriminator}"

    embed = Utils.embed(ctx)

    embed.title = "Member Banned!"
    embed.add_field(name="Who was banned", value=f"**`{member_tag}`**", inline=True)
    embed.add_field(name="Banned by", value=f"**`{author_tag}`**", inline=True)
    embed.add_field(name="Reason", value=f"**`{reason}`**")

    await member.ban(reason=reason)
    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option(name="reason", description="The reason for unbanning the member from the server.", required=False)
@lightbulb.option(name="member_id", description="The members id that you want to unban.", required=True)
@lightbulb.command(name="unban", description="Unban a member from the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def unban_command(ctx: lightbulb.SlashContext):
    embed = Utils.embed(ctx)
    reason: str = "Unspecified"

    if ctx.options.reason:
        reason = ctx.options.reason

    user = None
    bans = await ctx.bot.rest.fetch_bans(ctx.get_guild().id)

    for ban in bans:
        if ban.user.id == ctx.options.member_id:
            user = ban.user

    if user == None:
        embed.description = "**No user was found with the member id provided.**"
        await ctx.respond(embed, flags=MessageFlag.EPHEMERAL)
        return

    await ctx.get_guild().unban(user=int(ctx.options.member_id), reason=reason)

    author_tag = f"{ctx.author.username}#{ctx.author.discriminator}"
    member_tag = f"{user.username}#{user.discriminator}"

    embed.title = "Member Unbanned!"
    embed.add_field(name="Who was unbanned", value=f"**`{member_tag}`**", inline=True)
    embed.add_field(name="Unbanned by", value=f"**`{author_tag}`**", inline=True)
    embed.add_field(name="Reason", value=f"**`{reason}`**")

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.BAN_MEMBERS))
@lightbulb.option(name="reason", description="The reason for unbanning the member from the server.", required=False)
@lightbulb.option(name="duration", description="How long you would like the timeout to last for.", required=True)
@lightbulb.option(name="member", description="The member you want to set a timeout for.", type=hikari.Member, required=True)
@lightbulb.command(name="timeout", description="Set a timeout for a member in the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def timeout_command(ctx: lightbulb.SlashContext):
    embed = Utils.embed(ctx)
    reason: str = "Unspecified"

    if ctx.options.reason:
        reason = str(ctx.options.reason)

    user: hikari.Member = ctx.options.member
    time = humanfriendly.parse_timespan(str(ctx.options.duration))

    author_tag = f"{ctx.author.username}#{ctx.author.discriminator}"
    member_tag = f"{user.username}#{user.discriminator}"

    embed.title = "Member Timeout!"
    embed.add_field(name="Who has a timeout", value=f"**`{member_tag}`**", inline=True)
    embed.add_field(name="Timeout given by", value=f"**`{author_tag}`**", inline=True)
    embed.add_field(name="Reason", value=f"**`{reason}`**")

    await user.edit(reason=reason, communication_disabled_until=datetime.datetime.utcnow()+datetime.timedelta(seconds=time))

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.MANAGE_GUILD))
@lightbulb.option(name="reason", description="The reason for unbanning the member from the server.", required=False)
@lightbulb.option(name="member", description="The member you want to remove a timeout for.", type=hikari.Member, required=True)
@lightbulb.command(name="remove-timeout", description="Remove a timeout for a member in the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def untimeout_command(ctx: lightbulb.SlashContext):
    embed = Utils.embed(ctx)
    reason: str = "Unspecified"

    if ctx.options.reason:
        reason = str(ctx.options.reason)

    user: hikari.Member = ctx.options.member

    author_tag = f"{ctx.author.username}#{ctx.author.discriminator}"
    member_tag = f"{user.username}#{user.discriminator}"

    embed.title = "Member Timeout Removed!"
    embed.add_field(name="Whos timeout was removed", value=f"**`{member_tag}`**", inline=True)
    embed.add_field(name="Timeout removed by", value=f"**`{author_tag}`**", inline=True)
    embed.add_field(name="Reason", value=f"**`{reason}`**")

    await user.edit(reason=reason, communication_disabled_until=None)

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))
@lightbulb.option(name="amount", description="The amount of messages you want to clear.", required=True)
@lightbulb.command(name="purge", description="Purge a certain amount of messages.")
@lightbulb.implements(lightbulb.SlashCommand)
async def purge_command(ctx: lightbulb.SlashContext):
    amount = int(ctx.options.amount)

    if amount <= 1:
        return await ctx.respond(Utils.quick_embed(f"**You need to provide more than 1 message to delete.**", ctx))

    if amount > 100:
        return await ctx.respond(Utils.quick_embed(f"**You cannot provide more than 100 messages to delete.**", ctx))

    messages = list(await ctx.bot.rest.fetch_messages(ctx.get_channel().id))[slice(amount)]

    channel: hikari.TextableGuildChannel = ctx.get_channel()
    await channel.delete_messages(messages)

    msg = await ctx.respond(Utils.quick_embed(f"**I have deleted `{amount}` messages.**", ctx))

    await asyncio.sleep(5)
    await msg.delete()

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.MANAGE_GUILD))
@lightbulb.option(name="reason", description="The reason why you warned the member you provided.", required=False)
@lightbulb.option(name="member", description="The member you want to warn.", type=hikari.Member, required=True)
@lightbulb.command(name="warn", description="Warn a member in the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def warn_command(ctx: lightbulb.SlashContext):
    member: hikari.Member = ctx.options.member
    collection = Utils.get_database().load_collection("Users")

    if ctx.options.reason:
        reason = ctx.options.reason
    else:
        reason = "Unspecified"

    collection.push({
        "Guild": ctx.guild_id,
        "User": member.id
    }, "Warns", { "Moderator": ctx.author.id, "Reason": reason, })

    await ctx.respond(Utils.quick_embed(f"**`${member.username}#{member.discriminator}` has been warned with the reason of `{reason}`**", ctx))
    
    try:
        await member.send(Utils.quick_embed(f"**You were warned in `{ctx.get_guild().name}` for the following reason: `${reason}`**", ctx))
    except:
        pass

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.MANAGE_GUILD))
@lightbulb.option(name="member", description="The member you want the view the warnings for.", type=hikari.Member, required=True)
@lightbulb.command(name="warnings", description="Check the warnings a specific member has.")
@lightbulb.implements(lightbulb.SlashCommand)
async def warnings_command(ctx: lightbulb.SlashContext):
    desc = ""
    embed = Utils.embed(ctx)
    member: hikari.Member = ctx.options.member
    collection = Utils.get_database().load_collection("Users")

    warnings: list = collection.get_or_default({ "Guild": ctx.guild_id, "User": member.id }, "Warns", [])

    if warnings == []:
        embed.description = f"**`{member.username}#{member.discriminator}` has no warns in this server!**"
        return await ctx.respond(embed)

    count = 0
    for warning in warnings:
        reason = warning["Reason"]
        moderator = await ctx.bot.rest.fetch_user(warning['Moderator'])
        desc += f"**`{count + 1}.` Moderator: `{moderator.username}#{moderator.discriminator}` Reason: `{reason}`**\n"
        count += 1

    embed.title = f"**`${member.username}#{member.discriminator}` has `${count}` warns in `${ctx.get_guild().name}`.**"
    embed.description = desc

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.MANAGE_GUILD))
@lightbulb.option(name="member", description="The member you want the clear the warnings for.", type=hikari.Member, required=True)
@lightbulb.command(name="clearwarnings", description="Clear all the warnings a specific person has.")
@lightbulb.implements(lightbulb.SlashCommand)
async def clear_warnings_command(ctx: lightbulb.SlashContext):
    embed = Utils.embed(ctx)
    member: hikari.Member = ctx.options.member
    collection = Utils.get_database().load_collection("Users")

    warnings: list = collection.get_or_default({ "Guild": ctx.guild_id, "User": member.id }, "Warns", [])

    if warnings == []:
        embed.description = f"**`{member.username}#{member.discriminator}` has no warns in this server!**"
        return await ctx.respond(embed)

    collection.update({
        "Guild": ctx.guild_id,
        "User": member.id
    }, {
        "Warns": []
    })

    embed.description = f"**Cleared all of `{member.user.username}'s` warns!**"

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.MANAGE_GUILD))
@lightbulb.option(name="channel", description="The channel you would like to lock.", type=hikari.TextableGuildChannel, required=False)
@lightbulb.command(name="lock", description="Lock a channel.")
@lightbulb.implements(lightbulb.SlashCommand)
async def lock_command(ctx: lightbulb.SlashContext):
    embed = Utils.embed(ctx)
    channel: hikari.TextableGuildChannel = ctx.get_channel()

    if ctx.options.channel:
        channel = ctx.options.channel

    roles = ctx.get_guild().get_roles()
    everyone_role: hikari.Role = None

    for role in roles:
        fetched_role = ctx.get_guild().get_role(role)

        if fetched_role.name == "@everyone":
            everyone_role = fetched_role

    await channel.edit_overwrite(everyone_role, deny=hikari.Permissions.VIEW_CHANNEL)

    embed.description = f"**The channel `{channel.name}` has now been locked!**"

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.add_checks(checks.has_guild_permissions(hikari.Permissions.MANAGE_GUILD))
@lightbulb.option(name="channel", description="The channel you would like to unlock.", type=hikari.TextableGuildChannel, required=False)
@lightbulb.command(name="unlock", description="Unlock a channel.")
@lightbulb.implements(lightbulb.SlashCommand)
async def unlock_command(ctx: lightbulb.SlashContext):
    embed = Utils.embed(ctx)
    channel: hikari.TextableGuildChannel = ctx.get_channel()

    if ctx.options.channel:
        channel = ctx.options.channel

    roles = ctx.get_guild().get_roles()
    everyone_role: hikari.Role = None

    for role in roles:
        fetched_role = ctx.get_guild().get_role(role)

        if fetched_role.name == "@everyone":
            everyone_role = fetched_role

    await channel.edit_overwrite(everyone_role, allow=hikari.Permissions.VIEW_CHANNEL)

    embed.description = f"**The channel `{channel.name}` has now been unlocked!**"

    await ctx.respond(embed)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)