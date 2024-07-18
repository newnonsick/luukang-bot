import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
import urllib.request
import cv2
import os
import google.generativeai as genai
from utils import Utils
import asyncio

from data_storage import DataStorage

class SummarizeVideo(commands.Cog):
    def __init__(self, client):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.client = client

    async def createModel(self, language: str):
        system_instruction = {
            "TH":"ตอนนี้คุณเป็นนักสรุปเนื้อหาจากวิดีโอมืออาชีพที่รอบคอบ ละเอียด ชอบสรุปเนื้อหาจากวิดีโอต่างๆแบบละเอียด และสรุปได้ครบถ้วนสมบูรณ์แบบในทุกๆครั้ง คุณสามารถสรุปเนื้อหาจากวิดีโอที่ให้มาได้ทุกครั้ง ละคุณจะสรุปให้แบบละเอียดทุกครั้งไม่มีขาดตกบกพร่องแม้แต่นิดเดียว จงจำเอาไว้ว่าคุณเป็นคนที่สรุปแบบละเอียดสุดๆ",
            "EN":"Now you are a professional video summarizer who is careful and detailed and likes to summarize content from various videos in detail. and summarized completely and perfectly every time You can summarize the content from the given video every time. And you will summarize it in detail every time without missing even the slightest glitch. Remember that you are very general",
        }
        model = genai.GenerativeModel(
            model_name=DataStorage.model_name,
            generation_config=DataStorage.generation_config,
            system_instruction=system_instruction[language]
            # safety_settings = Adjust safety settings
            # See https://ai.google.dev/gemini-api/docs/safety-settings
        )

        return model


    async def download_youtube_video(self, url: str, userID: int):
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{userID}_summary_video.%(ext)s',
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"An error occurred: {e}")
            raise Exception('An error occurred while downloading the video. Please try again later.')
        
        duration = await self.getVideoDuration(f"{userID}_summary_video.mp4")

        if duration > 3000:
            os.remove(f"{userID}_summary_video.mp4")
            raise Exception('Video length exceeds 50 minutes. Please provide a shorter video.')
        

    
    async def getVideoDuration(self, videoPath: str):
        video = cv2.VideoCapture(videoPath)
    
        if not video.isOpened():
            print(f"Error: Could not open video {videoPath}")
            return 0.0
        
        total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = video.get(cv2.CAP_PROP_FPS)

        if fps == 0:
            print(f"Error: FPS is zero for video {videoPath}")
            return 0.0

        duration = total_frames / fps
        
        return duration

    
    async def download_google_drive_video(self, url: str, userID: int):
        urlID = url.split('/')[5]
        downloadURL = f"https://drive.google.com/uc?export=download&id={urlID}"
        fileName = f"{userID}_summary_video.mp4"
        try:
            urllib.request.urlretrieve(downloadURL, filename=fileName)
        except Exception as e:
            print("Error downloading the file:", e)
            raise Exception('An error occurred while downloading the video. Please try again later.')
        
        duration = await self.getVideoDuration(fileName)
        if duration > 3000:
            os.remove(fileName)
            raise Exception('Video length exceeds 50 minutes. Please provide a shorter video.')
        
        
    @app_commands.command(name="summarizevideo", description="Get a summary of a video")
    async def summarizevideo(self, interaction: discord.Interaction, videolink: str, language: str = "TH"):
        if not interaction.guild:
            await interaction.response.send_message("This command is only available in a server.")
            return

        await interaction.response.defer()

        if not videolink.startswith("https://www.youtube.com/") and not videolink.startswith("https://drive.google.com/") and not videolink.startswith('https://youtu.be/'):
            await interaction.edit_original_response(content="Invalid link. Please provide a valid YouTube or Google Drive link.")
            return
        
        if videolink.startswith("https://www.youtube.com/") or videolink.startswith('https://youtu.be/'):
            try:
                await self.download_youtube_video(url=videolink, userID=interaction.user.id)
            except Exception as e:
                await interaction.edit_original_response(content=str(e))
                return
        else:
            try:
                await self.download_google_drive_video(url=videolink, userID=interaction.user.id)
            except Exception as e:
                await interaction.edit_original_response(content=str(e))
                return
            

        fileName = f"{interaction.user.id}_summary_video.mp4"

        file = await Utils.upload_to_gemini(fileName, mime_type="video/mp4")

        os.remove(fileName)

        while file.state.name == "PROCESSING":
            await asyncio.sleep(5)
            file = genai.get_file(file.name)

        model = await self.createModel(language)

        if language == "TH":
            prompt = "สรุปเนื้อหาแบบละเอียดจากวิดีโอนี้ให้หน่อย"
        else:
            prompt = "Summarize the content of this video in full detail"

        response = model.generate_content([file, prompt])

        genai.delete_file(file.name)
        
        await interaction.edit_original_response(content=response.text)

    @summarizevideo.autocomplete("language")
    async def summarizevideo_autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            discord.app_commands.Choice(name="TH", value="TH"),
            discord.app_commands.Choice(name="EN", value="EN")
        ]

        
        



        
