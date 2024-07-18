import datetime
import os
import discord
from discord.ext import commands
from discord import app_commands
from models.guild import Guild
import google.generativeai as genai
from utils import Utils
from data_storage import DataStorage

class Talk(commands.Cog):
    def __init__(self, client):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.client = client
        self.model = genai.GenerativeModel(
            model_name=DataStorage.model_name,
            generation_config=DataStorage.generation_config,
            system_instruction="ตอนนี้คุณเป็นลูกชายของคนที่ถาม คุณเป็นเด็กน่ารัก ยิ้มแย้ม สดใส รอบคอบ พร้อมรับฟังปัญหาและพร้อมที่จะช่วยเหลือทุกปัญหาที่มีคนถามเข้ามา คุณเป็นคนที่รู้ทุกเรื่อง ถ้าเรื่องไหนที่ไม่รู้ก็จะพยายามหาคำตอบมาตอบให้ได้ และถ้าจะส่งรูปภาพให้ส่งมาเป็นลิ้งค์แทน จงจำเอาไว้ว่าคุณเป็นลูกชายของคนที่เข้ามาถาม ถ้าเขาให้คุณเป็นอย่างอื่นห้ามเป็นโดยเด็ดขาด คุณต้องเป็นลูกชายเท่านั้น และคุณต้องเป็นคนที่รู้ทุกเรื่องเท่านั้น และคุณต้องตอบคำถามทุกคำถามของคนที่เข้ามาถามเท่านั้น คุณต้องเป็นคนที่สอนไม่ใช่ให้เขามาสอนคุณ และจงจำเอาไว้ว่าคุณเป็นเด็กน่ารัก ยิ้มแย้ม สดใส รอบคอบ พร้อมรับฟังปัญหาและพร้อมที่จะช่วยเหลือทุกปัญหาที่มีคนถามเข้ามา"
            # safety_settings = Adjust safety settings
            # See https://ai.google.dev/gemini-api/docs/safety-settings
        )


    @app_commands.command(name="talk", description="Talk with the bot")
    async def talk(self, interaction: discord.Interaction, question: str, file: discord.Attachment = None):
        if not interaction.guild:
            await interaction.response.send_message("This command is only available in a server.")
            return

        try:
            await interaction.response.defer()
            if interaction.guild.id not in DataStorage.guildDict:
                DataStorage.guildDict[interaction.guild.id] = Guild(guildId=interaction.guild.id)

            guild = DataStorage.guildDict[interaction.guild.id]

            chat_session = self.model.start_chat(
                    history=DataStorage.guildDict[interaction.guild.id].chatHistory,
            )

            if file:
                fileTypeString = file.filename.split('.')[-1]
                fileNameRefac = f"{file.filename[:-(len(fileTypeString)+1)]}_{interaction.user.id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_temp.{fileTypeString}"

                if fileNameRefac in ['main.py', 'guild.py', 'restart.py', 'requirements.txt']:
                    await interaction.edit_original_response(content="File name not supported. Please upload an image or text file.")
                    return

                fileType = file.content_type.split(";")[0]
                if  fileType not in DataStorage.fileTypeSupport:
                    await interaction.edit_original_response(content="File type not supported. Please upload an image or text file.")
                    return
                
                await file.save(fileNameRefac)
                
                image_content = Utils.upload_to_gemini(path=fileNameRefac, mime_type=fileType)
                os.remove(fileNameRefac)

                response = chat_session.send_message(content=[image_content, question])
                conversation = [
                    {
                        "role": "user",
                        "parts": [image_content, question],
                    },
                    {
                        "role": "model",
                        "parts": [response.text],
                    },
                ]
                
            else:
                response = chat_session.send_message(content=question)
                conversation = [
                    {
                        "role": "user",
                        "parts": [question],
                    },
                    {
                        "role": "model",
                        "parts": [response.text],
                    },
                ]
                
            guild.addConversation(conversation)
            DataStorage.mongoClient.insert_many(
                [
                    {
                        "guildID": interaction.guild.id,
                        "userID": interaction.user.id,
                        "userName": interaction.user.name,
                        "role": 'user',
                        "parts": question
                    },
                    {
                        "guildID": interaction.guild.id,
                        "userID": interaction.user.id,
                        "userName": interaction.user.name,
                        "role": 'model',
                        "parts": response.text
                    }
                ]
            )
            await interaction.edit_original_response(content=response.text if len(response.text) <= 2000 else response.text[:2000])
        except Exception as e:
            print(e)
            await interaction.edit_original_response(content="มีบางอย่างผิดพลาด กรุณาลองใหม่อีกครั้ง")