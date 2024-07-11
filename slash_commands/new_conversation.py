import discord
from discord.ext import commands
from discord import app_commands
from models.guild import Guild

class NewConversation(commands.Cog):
    def __init__(self, client, data_storage):
        self.client = client
        self.data_storage = data_storage

    @app_commands.command(name="newconversation", description="Start a new conversation with the bot")
    async def new_conversation(self, interaction: discord.Interaction):
        if not interaction.guild:
            await interaction.response.send_message("This command is only available in a server.")
            return

        await interaction.response.defer()
        if interaction.guild.id not in self.data_storage.guildDict:
            self.data_storage.guildDict[interaction.guild.id] = Guild(interaction.guild.id)

        guild = self.data_storage.guildDict[interaction.guild.id]
        guild.resetChatHistoy()

        self.data_storage.mongoClient.delete_many({"guildID": interaction.guild.id})

        await interaction.edit_original_response(content="Conversation started!. Ask me anything.")