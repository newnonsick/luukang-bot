import discord
from discord.ext import commands
from discord import app_commands
from models.guild import Guild
from data_storage import DataStorage

class NewConversation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="newconversation", description="Start a new conversation with the bot")
    async def new_conversation(self, interaction: discord.Interaction):
        if not interaction.guild:
            await interaction.response.send_message("This command is only available in a server.")
            return

        await interaction.response.defer()
        if interaction.guild.id not in DataStorage.guildDict:
            DataStorage.guildDict[interaction.guild.id] = Guild(interaction.guild.id)

        guild = DataStorage.guildDict[interaction.guild.id]
        guild.resetChatHistoy()

        DataStorage.mongoClient.delete_many({"guildID": interaction.guild.id})

        await interaction.edit_original_response(content="Conversation started!. Ask me anything.")