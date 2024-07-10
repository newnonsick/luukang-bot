import discord
from discord.ext import commands

class GatewayEvents(commands.Cog):

    def __init__(self, client, dataStorage):
        self.client = client
        self.dataStorage = dataStorage

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"to some questions!")) 
        print(f'We have logged in as {self.client.user.name}')  
