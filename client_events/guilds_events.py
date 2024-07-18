from discord.ext import commands
from data_storage import DataStorage

class GuildsEvents(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        DataStorage.guildDict.pop(guild.id, None)
        DataStorage.mongoClient.delete_many({"guildID": guild.id})
