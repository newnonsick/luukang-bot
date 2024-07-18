import asyncio
import os
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import discord
from discord.ext import commands
from client_events.gateway_events import GatewayEvents
from client_events.guilds_events import GuildsEvents
from slash_commands.new_conversation import NewConversation
from slash_commands.talk import Talk
from slash_commands.summarize_video import SummarizeVideo
from data_storage import DataStorage
from dotenv import load_dotenv

intents = discord.Intents.default() 
# intents.messages = True 
# intents.voice_states = True 
# intents.message_content = True 
# intents.members = True  

client = commands.Bot(command_prefix='!', intents=intents)

async def main():
    async with client:
        load_dotenv()
        DataStorage.initialize()
        await client.add_cog(SummarizeVideo(client=client))  
        await client.add_cog(GatewayEvents(client=client))
        await client.add_cog(GuildsEvents(client=client))
        await client.add_cog(NewConversation(client=client))
        await client.add_cog(Talk(client=client))
        await client.start(os.getenv("BOT_TOKEN"))


if __name__ == "__main__":
    try:     
        asyncio.run(main())
    except discord.HTTPException as e:     
        if e.status == 429:         
            print("The Discord servers denied the connection for making too many requests.")         
            print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")         
            os.system("python restart.py")         
            os.system('kill 1')     
        else:         
            raise e