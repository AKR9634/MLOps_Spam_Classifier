import os
import sys
import pymongo

import certifi

from src.logger import logging
from src.exception import MyException

MONGODB_PASSWORD = os.getenv("MONGO_PASS")
DATABASE_NAME = "Spam_Classifier"
MONGODB_URL_KEY = f"mongodb+srv://akhil6july2003_db_user:{MONGODB_PASSWORD}@cluster0.mpukhol.mongodb.net/?appName=Cluster0"

# Load the certificate authority file to avoid timeout error when connecting to MongoDB

ca = certifi.where()

class MongoDBClient:
    client = None

    def __init__(self, database_name:str = DATABASE_NAME) -> None:
        
        try:

            if MongoDBClient.client is None:
                mongo_db_url = MONGODB_URL_KEY
                if mongo_db_url is None:
                    raise Exception(f"Environment variable {MONGODB_URL_KEY} is not defined!!!")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlscafile=ca)

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successful!!!")
        
        except Exception as e:
            raise MyException(e, sys)