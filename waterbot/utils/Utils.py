import hikari
from datetime import datetime

import lightbulb
from waterbot.utils.Leveling import Leveling
from waterbot.utils.Database import Database

def get_bot_token() -> str:
    with open("./secrets/token.txt") as file:
        bot_token = file.read().strip()

    return bot_token

def get_mongo_uri() -> str:
    with open("./secrets/mongoURI.txt") as file:
        mongo_uri = file.read().strip()

    return mongo_uri

database = Database(get_mongo_uri(), "WaterBot")
leveling = Leveling(database)

def get_prefix() -> str:
    return "/"

def embed(message: lightbulb.SlashContext) -> hikari.Embed:
    embed = hikari.Embed(color="#1DA1F2")

    embed.timestamp = datetime.now().astimezone()
    embed.set_footer(text=f"{message.author.username}#{message.author.discriminator}", icon=message.author.avatar_url.url)

    return embed

def quick_embed(text: str, message: lightbulb.SlashContext | hikari.GuildMessageCreateEvent) -> hikari.Embed:
    embed = hikari.Embed(description=text, color="#1DA1F2")

    embed.timestamp = datetime.now().astimezone()
    embed.set_footer(text=f"{message.author.username}#{message.author.discriminator}", icon=message.author.avatar_url.url)

    return embed

def get_command_options(options):
    usage = ""

    for option in options:
        option_like = options.get(option)

        usage += " "

        if option_like.required:
            usage += f"<{option}>"
        else:
            usage += f"[{option}]"

    return usage

def get_permissions(perms: list[str]) -> str:
    permissions = []

    for perm in perms:
        string = f"`{str(perm).replace('_', ' ').title()}`"
        permissions.append(string)

    return ' '.join(permissions)

def get_database(): 
    return database

def get_leveling(): 
    return leveling