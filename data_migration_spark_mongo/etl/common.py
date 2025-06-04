from pymongo import MongoClient

def clean_collection(collection_name: str):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["challenge"]
    db[collection_name].delete_many({})