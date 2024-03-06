from dotenv import load_dotenv
import os
from pymongo import MongoClient
from bson import ObjectId

load_dotenv()

USER_DB = os.getenv("MONGO_INITDB_ROOT_USERNAME")
USER_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
DB_NAME = os.getenv("MONGO_INITDB_DATABASE")
DB_URL = "mongodb://{username}:{password}@mongodb_wibo:27017/".format(
    username=USER_DB,
    password=USER_PASS,  
)
def get_mongo_client(model : str = DB_NAME):
        client = MongoClient(DB_URL)
        db = client[model]
        return db

