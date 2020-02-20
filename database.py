from pymongo import MongoClient

#connecting to mongodb running on default host and port
client = MongoClient('mongodb://localhost:27017/')
db = client.data

def insert_article(data):
    #check if article has already bin insertet by date,title,author
    db.article.insert(data)

def get_all(data):
    pass
