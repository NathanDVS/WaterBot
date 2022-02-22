import hikari
from waterbot.utils import Utils
from waterbot.utils.Database import Database

class Leveling:

    _database: Database = None

    def __init__(self, database) -> None:
        self._database = database

    async def add_xp(self, xp: int, event: hikari.GuildMessageCreateEvent):
        guild_collection = self._database.load_collection("Users")
        collection = self._database.load_collection("Users")
        
        temp_xp = collection.get_or_default({ "Guild": event.get_guild().id, "User": event.author_id }, "Xp", 0)
        temp_level = collection.get_or_default({ "Guild": event.get_guild().id, "User": event.author_id }, "Level", 1)

        updated_level = temp_level
        updated_xp = int(temp_xp + xp)

        needed_xp = temp_level * temp_level * 100

        if temp_xp >= needed_xp:
            updated_xp = updated_xp - needed_xp
            updated_level = temp_level + 1

            auto_roles = guild_collection.get_or_default({ "Guild": event.guild_id }, "LevelingAutoRoles", [])

            if auto_roles != []:
                for auto_role in auto_roles:
                    level = auto_role['Level']
                    role = event.get_guild().get_role(auto_role['Role'])

                    if updated_level == level:
                        event.member.add_role(role.id)

            try:
                data = guild_collection.get({ "Guild": event.guild_id })
                leveling_channel: hikari.TextableGuildChannel = event.get_guild().get_channel(data["LevelingChannel"])

                if data["LevelingChannel"] == None:
                    leveling_channel: hikari.TextableGuildChannel = event.get_channel()
                    await leveling_channel.send(Utils.quick_embed(f"**🎉 {event.author.username}#{event.author.discriminator}, congratulations! You have leveled up to `{updated_level}`.**", event))
                else:
                    await leveling_channel.send(Utils.quick_embed(f"**🎉 {event.author.username}#{event.author.discriminator}, congratulations! You have leveled up to `{updated_level}`.**", event))
            except:
                leveling_channel: hikari.TextableGuildChannel = event.get_channel()
                await leveling_channel.send(Utils.quick_embed(f"**🎉 {event.author.username}#{event.author.discriminator}, congratulations! You have leveled up to `{updated_level}`.**", event))

        collection.update({
            "Guild": event.get_guild().id,
            "User": event.author_id 
        }, {
            "Guild": event.get_guild().id,
            "User": event.author_id,
            "Level": updated_level,
            "Xp": updated_xp
        })