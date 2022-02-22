import random
import hikari
import lightbulb
from waterbot.utils import Utils
from hikari.messages import MessageFlag

plugin = lightbulb.Plugin("Events")

@plugin.listener(hikari.GuildMessageCreateEvent)
async def message_create_event(event: hikari.GuildMessageCreateEvent):
    if event.author.is_bot:
        pass
    else:
        xp_to_add = random.randint(5, 10)
        await Utils.get_leveling().add_xp(int(xp_to_add), event)

@plugin.listener(hikari.GuildJoinEvent)
async def guild_join_event(event: hikari.GuildJoinEvent):
    guilds = await event.app.rest.fetch_my_guilds()

    if len(guilds) == 1:
        await plugin.bot.update_presence(activity=hikari.Activity(name=f"/help || {len(guilds)} server", type=hikari.ActivityType.PLAYING), status=hikari.Status.DO_NOT_DISTURB)
    else:
        await plugin.bot.update_presence(activity=hikari.Activity(name=f"/help || {len(guilds)} servers", type=hikari.ActivityType.PLAYING), status=hikari.Status.DO_NOT_DISTURB)

@plugin.listener(hikari.StartedEvent)
async def on_started_event(event: hikari.StartedEvent):
    guilds = await event.app.rest.fetch_my_guilds()
    
    if len(guilds) == 1:
        await plugin.bot.update_presence(activity=hikari.Activity(name=f"/help || {len(guilds)} server", type=hikari.ActivityType.PLAYING), status=hikari.Status.DO_NOT_DISTURB)
    else:
        await plugin.bot.update_presence(activity=hikari.Activity(name=f"/help || {len(guilds)} servers", type=hikari.ActivityType.PLAYING), status=hikari.Status.DO_NOT_DISTURB)

@plugin.listener(lightbulb.CommandErrorEvent)
async def on_command_err(event: lightbulb.CommandErrorEvent):

    if isinstance(event.exception, lightbulb.CommandNotFound):
        return None

    if isinstance(event.exception, lightbulb.CommandIsOnCooldown):
        embed = Utils.quick_embed(text=f"**Command is on cooldown. Try again in `{event.exception.retry_after:.1f}` seconds.**", message=event.context)
        return await event.context.respond(embed, flags=MessageFlag.EPHEMERAL)

    if isinstance(event.exception, lightbulb.NotOwner):
        embed = Utils.quick_embed(text=f"**You cannot use this command because you are not the owner of the bot.**", message=event.context)
        return await event.context.respond(embed, flags=MessageFlag.EPHEMERAL)

    if isinstance(event.exception, lightbulb.BotMissingRequiredPermission):
        embed = Utils.quick_embed(text=f"**I am missing the following permissions: {Utils.get_permissions(event.exception.missing_perms)}.**", message=event.context)
        return await event.context.respond(embed, flags=MessageFlag.EPHEMERAL)

    if isinstance(event.exception, lightbulb.MissingRequiredPermission):
        embed = Utils.quick_embed(text=f"**You are missing the following permissions: {Utils.get_permissions(event.exception.missing_perms)}.**", message=event.context)
        return await event.context.respond(embed, flags=MessageFlag.EPHEMERAL)

    print(event.exception)
    return await event.context.respond(Utils.quick_embed(text=f"**An error has occured when executing this command.**", message=event.context), flags=MessageFlag.EPHEMERAL)

@plugin.listener(hikari.GuildReactionAddEvent)
async def on_reaction_add(event: hikari.GuildReactionAddEvent):
    collection = Utils.get_database().load_collection("ReactionRoles")
    
    emoji = None

    if event.emoji_id != None:
        emoji = ":" + event.emoji_name + ":"
    else:
        emoji = event.emoji_name

    data = collection.get({
        "Guild": int(event.guild_id),
        "Message": int(event.message_id),
        "Emoji": emoji,
    })

    if not data:
        return

    try:
        await event.member.add_role(data["Role"])
    except:
        pass

@plugin.listener(hikari.GuildReactionDeleteEvent)
async def on_reaction_remove(event: hikari.GuildReactionDeleteEvent):
    collection = Utils.get_database().load_collection("ReactionRoles")
    
    emoji = None

    if event.emoji_id != None:
        emoji = ":" + event.emoji_name + ":"
    else:
        emoji = event.emoji_name

    data = collection.get({
        "Guild": int(event.guild_id),
        "Message": int(event.message_id),
        "Emoji": emoji,
    })

    if not data:
        return

    try:
        await event.app.rest.remove_role_from_member(data["Guild"], event.user_id, data["Role"])
    except:
        pass

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)