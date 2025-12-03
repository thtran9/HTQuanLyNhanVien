import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("mongodb+srv://tvthuwork_db_user:7B9JRb6YJErpNNKd@cluster.mongodb.net/")
db_name = os.getenv("test")

def get_database():
    try:
        client = MongoClient(mongo_uri)
        return client[db_name]
    except Exception as e:
        print("Kết nối không thành công!")
        print(e)