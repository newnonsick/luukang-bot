from discord.ext import commands
from models.mongodb_client import MongoDBClient
from models.guild import Guild

class GuildsEvents(commands.Cog):

    def __init__(self, client, dataStorage):
        self.client = client
        self.dataStorage = dataStorage

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.dataStorage.guildDict.pop(guild.id, None)
        self.dataStorage.mongoClient.delete_many({"guildID": guild.id})
