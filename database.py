from pymongo import MongoClient

#connecting to mongodb running on default host and port
client = MongoClient('mongodb://localhost:27017/')
db = client.data

print(db.list_collection_names())

def insert_data(data):
    #check if article has already bin insertet by date,title,author
    pass

def get_all(data):
    pass
