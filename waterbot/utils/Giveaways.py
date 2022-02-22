import asyncio
import hikari
import lightbulb
from waterbot.utils import Utils

async def schedule_giveaway(bot: lightbulb.BotApp, msg_id: int):
    collection = Utils.get_database().load_collection("Giveaways")
    data = collection.get({ "Message": msg_id })

    channel: hikari.GuildTextChannel = await bot.rest.fetch_channel(data["Channel"])
    message = await channel.fetch_message(msg_id)

    await asyncio.sleep(data["Duration"])

async def start_giveaway(bot: lightbulb.BotApp, channel: int, prize: str, duration: int, winners: int, hosted_by: int, ctx: lightbulb.SlashContext):
    collection = Utils.get_database().load_collection("Giveaways")
    text_channel: hikari.TextableGuildChannel = ctx.get_guild().get_channel(channel)
    member_hosting_giveaway = ctx.get_guild().get_member(hosted_by)                                                                                                                              
    
    msg = await channel.send(Utils.quick_embed(f"**🎖️ Winners: `{options.Winners} Winners`\n🥳 Hosted By: `{member_hosting_giveaway.username}#{member_hosting_giveaway.discriminator}`**", ctx))
    await msg.add_reaction('🎉')

    collection.create({
        "Message": msg.id,
        "HasEnded": False,
        "Channel": text_channel.id,
        "Guild": ctx.guild_id,
        "Duration": duration,
        "HostedBy": member_hosting_giveaway.id,
        "Prize": prize,
        "Winners": winners
    })

    await ctx.respond(Utils.quick_embed("**🎉 Created the giveaway.**", ctx))
    await schedule_giveaway(msg.id)
