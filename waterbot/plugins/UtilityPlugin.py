import lightbulb
from waterbot.utils import Utils

plugin = lightbulb.Plugin("Utility")

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.command(name="ping", description="Checks the bots latency.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping_command(ctx: lightbulb.SlashContext):
    embed = Utils.quick_embed(text=f"**API Latency: `{round(ctx.bot.heartbeat_latency * 1000)} MS!`**", message=ctx)
    embed.title = "🏓 Pong!"
    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.option(name="command", description="A command name.", required=False)
@lightbulb.command(name="help", description="Shows a list of commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def help_command(ctx: lightbulb.SlashContext):
    embed = Utils.embed(ctx)
    guild = ctx.get_guild()
    embed.set_thumbnail(guild.get_member(881566888897957909).avatar_url.url)

    if ctx.options.command:
        command_name: str = str(ctx.options.command).title()
        command = ctx.bot.slash_commands.get(ctx.options.command)

        embed.title = f"{command_name} Command"
        usage: str = f"/{command.name}{Utils.get_command_options(command.options)}"

        embed.description = f"**Name: `{command_name}`\nDescription: `{command.description}`\nUsage: `{usage}`**"
    else:
        embed.description = f"**The prefix for this bot is `{Utils.get_prefix()}`**"
        
        if guild.icon_url != None:
            embed.set_author(name=f"Help Commands | {guild.name}", icon=guild.icon_url.url)
        else:
            embed.set_author(name=f"Help Commands | {guild.name}")

        for plugin in ctx.bot.plugins:
            if plugin in ["Events"]:
                continue

            commands_type = f"{plugin} Commands"
            commands = ""

            for command in ctx.bot.get_plugin(plugin).all_commands:
                commands += f"**`{command.name}`** "

            embed.add_field(commands_type, commands)

    await ctx.respond(embed)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)