import hikari
import random
import lightbulb
from waterbot.utils import Utils

plugin = lightbulb.Plugin("Economy")

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.option(name="member", description="A member in the server.", required=False, type=hikari.Member)
@lightbulb.command(name="balance", description="Check yours or someones balance.")
@lightbulb.implements(lightbulb.SlashCommand)
async def balance_command(ctx: lightbulb.SlashContext):
    guild = ctx.get_guild()
    user: hikari.Member = ctx.member
    collection = Utils.get_database().load_collection("Users")

    if ctx.options.member:
        user = ctx.options.member

    wallet = collection.get_or_default({ "Guild": guild.id, "User": user.id }, "Wallet", 0)
    bank = collection.get_or_default({ "Guild": guild.id, "User": user.id }, "Bank", 0)

    embed = Utils.embed(ctx)

    if guild.icon_url != None:
        embed.set_author(name=f"{user.username}#{user.discriminator} Balance | {guild.name}", icon=guild.icon_url.url)
    else:
        embed.set_author(name=f"{user.username}#{user.discriminator} Balance | {guild.name}")

    embed.description = f"**Wallet: `{wallet} Coins`**\n**Bank: `{bank} Coins`**"

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(30, 1, lightbulb.UserBucket)
@lightbulb.command(name="beg", description="\"Beg\" people for \"money\".")
@lightbulb.implements(lightbulb.SlashCommand)
async def beg_command(ctx: lightbulb.SlashContext):
    user = ctx.author
    amount = random.randint(1, 1000)

    collection = Utils.get_database().load_collection("Users")

    collection.increment({ "Guild": ctx.guild_id, "User": user.id }, "Wallet", amount)

    embed = Utils.quick_embed(f"**You have earned `{amount} coins`!**", ctx)
    embed.title = "Beg Command | Economy"

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3600, 1, lightbulb.UserBucket)
@lightbulb.command(name="work", description="Every hour you can run this command to earn \"money\".")
@lightbulb.implements(lightbulb.SlashCommand)
async def work_command(ctx: lightbulb.SlashContext):
    user = ctx.author
    amount = random.randint(1000, 5000)

    collection = Utils.get_database().load_collection("Users")

    collection.increment({ "Guild": ctx.guild_id, "User": user.id }, "Wallet", amount)

    jobs = ['Developer', 'Scientist', 'Doctor', 'Shopkeeper']
    job = jobs[random.randint(0, 3)]

    embed = Utils.quick_embed(f"**You have earned `{amount} coins` as a `{job}`!**", ctx)
    embed.title = "Work Command | Economy"

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(86400, 1, lightbulb.UserBucket)
@lightbulb.command(name="daily", description="Each day you can run this command to earn \"money\".")
@lightbulb.implements(lightbulb.SlashCommand)
async def daily_command(ctx: lightbulb.SlashContext):
    user = ctx.author
    amount = random.randint(1000, 5000)

    collection = Utils.get_database().load_collection("Users")

    collection.increment({ "Guild": ctx.guild_id, "User": user.id }, "Wallet", amount)

    embed = Utils.quick_embed(f"**You have earned `{amount} coins`!**", ctx)
    embed.title = "Daily Command | Economy"

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(604800, 1, lightbulb.UserBucket)
@lightbulb.command(name="weekly", description="Each week you can run this command to earn \"money\".")
@lightbulb.implements(lightbulb.SlashCommand)
async def weekly_command(ctx: lightbulb.SlashContext):
    user = ctx.author
    amount = random.randint(5000, 10000)

    collection = Utils.get_database().load_collection("Users")

    collection.increment({ "Guild": ctx.guild_id, "User": user.id }, "Wallet", amount)

    embed = Utils.quick_embed(f"**You have earned `{amount} coins`!**", ctx)
    embed.title = "Weekly Command | Economy"

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(300, 1, lightbulb.UserBucket)
@lightbulb.command(name="slots", description="You can use this command to use the slots machine. (earn \"money\")")
@lightbulb.implements(lightbulb.SlashCommand)
async def slots_command(ctx: lightbulb.SlashContext):
    user = ctx.author
    amount = random.randint(0, 2000) - 1000

    collection = Utils.get_database().load_collection("Users")

    embed = Utils.quick_embed(f"**You have earned `{amount} coins`!**", ctx)
    embed.title = "Slots Command | Economy"

    top = ['🍇 🍇 🍇', '🍎 🍎 🍎'][random.randint(0, 1)]
    mid = ['🍇 🍇 🍎', '🍎 🍎 🍇'][random.randint(0, 1)]
    bottom = ['🍊 🍎 🍇', '🍇 🍎 🍊'][random.randint(0, 1)]

    if amount < 0:
        embed.color = "#FF1919"
    elif 0 < amount:
        embed.color = "#00FF00"

    if amount > 500:
        emojis = top
    if amount < 501 and amount > 0:
        emojis = mid
    if (amount < 1):
        emojis = bottom

    collection.increment({ "Guild": ctx.guild_id, "User": user.id }, "Wallet", amount)
    embed.add_field(name="You spun:", value=emojis, inline=True)

    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3600, 1, lightbulb.UserBucket)
@lightbulb.option(name="amount", description="The amount of you want to withdraw.", required=True)
@lightbulb.command(name="withdraw", description="Withdraw money to the bank.")
@lightbulb.implements(lightbulb.SlashCommand)
async def withdraw_command(ctx: lightbulb.SlashContext):
    embed = Utils.embed(ctx)

    amount = str(ctx.options.amount)
    collection = Utils.get_database().load_collection("Users")

    bank = collection.get_or_default({
		"User": ctx.author.id,
		"Guild": ctx.guild_id,
	}, "Bank", 0)

    if amount == "max" or amount == "all":
        collection.increment({ "User": ctx.author.id, "Guild": ctx.guild_id }, "Wallet", bank)
        collection.decrement({ "User": ctx.author.id, "Guild": ctx.guild_id }, "Bank", bank)

        embed.description = f"**Withdrawed `{bank} coins!`**"
        return await ctx.respond(embed)

    if bank < amount:
        embed.description = "**You do not have that much money in your bank!**"
        return await ctx.respond(embed)

    collection.increment({ "User": ctx.author.id, "Guild": ctx.guild_id }, "Wallet", int(amount))
    collection.decrement({ "User": ctx.author.id, "Guild": ctx.guild_id }, "Bank", int(amount))

    embed.description = f"**Withdrawed `{int(amount)} coins!`**"
    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3600, 1, lightbulb.UserBucket)
@lightbulb.option(name="amount", description="The amount of you want to deposit.", required=True)
@lightbulb.command(name="deposit", description="Deposit money to the bank.")
@lightbulb.implements(lightbulb.SlashCommand)
async def deposit_command(ctx: lightbulb.SlashContext):
    embed = Utils.embed(ctx)

    amount = str(ctx.options.amount)
    collection = Utils.get_database().load_collection("Users")

    wallet = collection.get_or_default({
		"User": ctx.author.id,
		"Guild": ctx.guild_id,
	}, "Wallet", 0)

    if amount == "max" or amount == "all":
        collection.decrement({ "User": ctx.author.id, "Guild": ctx.guild_id }, "Wallet", wallet)
        collection.increment({ "User": ctx.author.id, "Guild": ctx.guild_id }, "Bank", wallet)

        embed.description = f"**Deposited `{wallet} coins!`**"
        return await ctx.respond(embed)

    if wallet < amount:
        embed.description = "**You do not have that much money in your wallet!**"
        return await ctx.respond(embed)

    collection.decrement({ "User": ctx.author.id, "Guild": ctx.guild_id }, "Wallet", int(amount))
    collection.increment({ "User": ctx.author.id, "Guild": ctx.guild_id }, "Bank", int(amount))

    embed.description = f"**Deposited `{int(amount)} coins!`**"
    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(10000, 1, lightbulb.UserBucket)
@lightbulb.option(name="amount", description="The amount of you want to give.", required=True)
@lightbulb.option(name="member", description="A member in the server.", required=True, type=hikari.Member)
@lightbulb.command(name="give-money", description="Give money to another member in the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def give_money_command(ctx: lightbulb.SlashContext):
    embed = Utils.embed(ctx)

    amount = str(ctx.options.amount)
    member: hikari.Member = ctx.options.member
    collection = Utils.get_database().load_collection("Users")

    if member.id == ctx.author.id:
        embed.description = "**You cannot pay yourself!**"
        return await ctx.respond(embed)

    if amount.__contains__("-"):
        embed.description = "**You cannot provide a negitive number!**"
        return await ctx.respond(embed)

    wallet = collection.get_or_default({
		"User": ctx.author.id,
		"Guild": ctx.guild_id,
	}, "Wallet", 0)

    if wallet < amount:
        embed.description = f"**You do not have {amount} in your wallet!**"
        return await ctx.respond(embed)

    collection.increment({ "User": member.id, "Guild": ctx.guild_id }, "Wallet", int(amount))
    collection.decrement({ "User": ctx.author.id, "Guild": ctx.guild_id }, "Wallet", int(amount))

    embed.description = f"**You have given `{amount} coins` to `{member.username}#{member.discriminator}`!**"
    await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3600, 1, lightbulb.UserBucket)
@lightbulb.option(name="member", description="A member in the server.", required=True, type=hikari.Member)
@lightbulb.command(name="rob", description="Rob a member in the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def rob_command(ctx: lightbulb.SlashContext):
    embed = Utils.embed(ctx)

    member: hikari.Member = ctx.options.member
    collection = Utils.get_database().load_collection("Users")

    if member.id == ctx.author.id:
        embed.description = "**You cannot rob yourself!**"
        return await ctx.respond(embed)

    arr = [True, False]
    should_rob = arr[random.randint(0, 1)]

    wallet = collection.get_or_default({
        "User": ctx.author.id,
        "Guild": ctx.guild_id,
    }, "Wallet", 0)

    if wallet < 200:
        embed.description = f"**Does not have `200 coins` so its not worth it.**"
        return await ctx.respond(embed)

    if should_rob == True:
        amount = random.randint(200, wallet)

        collection.increment({ "User": member.id, "Guild": ctx.guild_id }, "Wallet", int(amount))
        collection.decrement({ "User": ctx.author.id, "Guild": ctx.guild_id }, "Wallet", int(amount))

        embed.description = f"**You have robbed `{member.username}#{member.discriminator}` and earned `{amount} coins`!**"
        return await ctx.respond(embed)
    else:
        embed.description = f"**You have failed to rob `{member.username}#{member.discriminator}`!**"
        return await ctx.respond(embed)

@plugin.command
@lightbulb.add_cooldown(3, 1, lightbulb.UserBucket)
@lightbulb.command(name="leaderboard", description="Check the leaderboard for the economy.")
@lightbulb.implements(lightbulb.SlashCommand)
async def leaderboard_command(ctx: lightbulb.SlashContext):
    guild = ctx.get_guild()

    text = ""
    embed = Utils.embed(ctx)

    collection = Utils.get_database().load_collection("Users")
    raw_lb = collection.leaderboard({ "Guild": guild.id }, [("Wallet", -1)], 10)

    embed.set_author(name=f"Economy Leaderboard", icon=guild.get_member(881566888897957909).avatar_url.url)
    
    count = 0

    for entry in raw_lb:
        user = ctx.bot.cache.get_user(entry['User'])

        try:
            text += f"**`{count + 1}.` {user.username}#{user.discriminator} - {entry['Wallet']} Coins**\n"
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
@lightbulb.command(name="global-leaderboard", description="Check the global leaderboard for the economy.")
@lightbulb.implements(lightbulb.SlashCommand)
async def global_leaderboard_command(ctx: lightbulb.SlashContext):
    guild = ctx.get_guild()

    text = ""
    embed = Utils.embed(ctx)

    collection = Utils.get_database().load_collection("Users")
    raw_lb = collection.leaderboard({}, [("Wallet", -1)], 10)

    embed.set_author(name=f"Economy Leaderboard", icon=guild.get_member(881566888897957909).avatar_url.url)
    
    count = 0

    for entry in raw_lb:
        user = ctx.bot.cache.get_user(entry['User'])

        try:
            text += f"**`{count + 1}.` {user.username}#{user.discriminator} - {entry['Wallet']} Coins**\n"
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
