import json
from models.guild import Guild
from models.mongodb_client import MongoDBClient
import os

class DataStorage:
    # Class variables to store data
    guildDict  = {}
    generation_config = {}
    model_name = ""
    fileTypeSupport  = []
    mongoClient = None

    @classmethod
    def initialize(cls):
        # Initialize the MongoDB client using environment variables
        mongo_uri = os.getenv('MONGO_URI')
        mongo_db = os.getenv('MONGO_DB')
        mongo_collection = os.getenv('MONGO_COLLECTION')

        if not (mongo_uri and mongo_db and mongo_collection):
            raise ValueError("MongoDB environment variables are not set properly.")

        cls.mongoClient = MongoDBClient(mongo_uri, mongo_db, mongo_collection)
        
        # Retrieve all guild IDs
        guild_list = cls.mongoClient.find_all_guildID()

        # Initialize guild dictionary with chat history
        for guild_id in guild_list:
            chat_history = cls.mongoClient.find({"guildID": guild_id})
            chat_history = [{'role': chat['role'], 'parts': [chat['parts']]} for chat in chat_history]
            cls.guildDict[guild_id] = Guild(guildId=guild_id, chatHistoryExtend=chat_history)

        # Load configuration from a JSON file
        try:
            with open("config.json", "r") as file:
                data = json.load(file)
                cls.generation_config = data.get("generation_config", {})
                cls.model_name = data.get("model_name", "")
                cls.fileTypeSupport = data.get("fileTypeSupport", [])
        except FileNotFoundError:
            print("Config file not found. Please ensure 'config.json' is present.")
        except json.JSONDecodeError:
            print("Config file is not a valid JSON.")

        print("DataStorage initialized")