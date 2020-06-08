from pymongo import MongoClient
from bson.objectid import ObjectId
import getpass
import keys

class Database:

    def __init__(self, logger=None):
        #connecting to mongodb running on default host and port
        user = getpass.getuser()
        pw = user+"!"

        ip = keys.get_key("mongoip")
        print("mongodb://"+user+":"+pw +"@"+ip)
        
        client = MongoClient(
            'mongodb://%s:%s@35.204.216.175:27017' % (user, pw))
        self.db = client.data

        self.logger = logger

    def insert_data(self,collection,data):
        #check if article has already bin insertet by date,title,author
        if self.db[collection].count_documents({"article_url": data["article_url"]}):
            self.logger.warn("Article already in db")
            return
        
        #insert article information into db
        try:
            self.db.article.insert(data)
            self.logger.info("Article succsessfully stored, URL:"+data["article_url"])
        except:
            self.logger.critical("Article could not be stored")
            
    def get_all(self,collection):
        return [doc for doc in self.db[collection].find()]


    def get_querry(self,collection,querry):
        return [doc for doc in self.db[collection].find(querry)]


    def update_article(self,collection,data):
        try:
            self.db[collection].find_one_and_replace({"_id": ObjectId(data["_id"])},data)
        except:
            print("No Article was found with givin ID")
            pass


    def find_by_id(self,collection, id):
        try:
            return self.db[collection].find_one({"_id": ObjectId(id)})
        except:
            return None
        




