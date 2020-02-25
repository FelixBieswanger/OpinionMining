from pymongo import MongoClient
from bson.objectid import ObjectId

class Database:

    def __init__(self, logger=None):
        #connecting to mongodb running on default host and port
        client = MongoClient('mongodb://localhost:27017/')
        self.db = db = client.data

        self.logger = logger

    def insert_article(self, data):
        #check if article has already bin insertet by date,title,author
        if self.db.article.count_documents({"article_url": data["article_url"]}):
            self.logger.warn("Article already in db")
            return
        
        #insert article information into db
        try:
            self.db.article.insert(data)
            self.logger.info("Article succsessfully stored")
        except:
            self.logger.critical("Article could not be stored")
            
    def get_all(self):
        return self.db.article.find()


    def update_article(self,data):
        try:
            article = self.db.article.find_one_and_replace({"_id": ObjectId(data["_id"])},data)
        except:
            print("Post with ID could not be found")
            pass


    def find_by_id(self, id):
        try:
            return self.db.article.find_one({"_id": ObjectId(id)})
        except:
            print("Post with ID could not be found")
            return
        



