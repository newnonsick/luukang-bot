import json
from models.guild import Guild
from models.mongodb_client import MongoDBClient
import os

class DataStorage:
    def __init__(self):
        self.guildDict = {}
        self.generation_config = {}
        self.model_name = ""
        self.fileTypeSupport = []
        self.mongoClient = None

        self.mongoClient = MongoDBClient(os.getenv('MONGO_URI'), os.getenv('MONGO_DB'), os.getenv('MONGO_COLLECTION'))
        guildList = self.mongoClient.find_all_guildID()
        for guildID in guildList:
            chatHistory = self.mongoClient.find({"guildID": guildID})
            chatHistory = [{'role':chat['role'], 'parts':[chat['parts']]} for chat in chatHistory]
            self.guildDict[guildID] = Guild(guildId=guildID, chatHistoryExtend=chatHistory)

        with open("config.json", "r") as file:
            data = json.load(file)
            self.generation_config = data["generation_config"]
            self.model_name = data["model_name"]
            self.fileTypeSupport = data["fileTypeSupport"]

        print("DataStorage initialized")