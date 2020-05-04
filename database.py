from pymongo import MongoClient
from bson.objectid import ObjectId
import getpass
import keys

class Database:

    def __init__(self, logger=None):
        #connecting to mongodb running on default host and port
        user = getpass.getuser()
        pw = user+"!"
        print("mongodb://"+user+":"+pw +"@34.90.240.64:27017/data")
        
        client = MongoClient( 'mongodb://%s:%s@34.90.240.64:27017' % (user, pw))
        self.db = client.data

        self.logger = logger

    def insert_data(self,collection,data):
        #check if article has already bin insertet by date,title,author
        if self.db[collection].count_documents({"article_url": data["article_url"]}):
            self.logger.warn("Article already in db")
            return "already"
        
        #insert article information into db
        try:
            self.db.article.insert(data)
            self.logger.info("Article succsessfully stored")
        except:
            self.logger.critical("Article could not be stored")
            
    def get_all(self,collection):
        return [doc for doc in self.db[collection].find()]


    def update_article(self,data):
        try:
            article = self.db.article.find_one_and_replace({"_id": ObjectId(data["_id"])},data)
        except:
            print("Post with ID could not be found")
            pass


    def find_by_id(self,collection, id):
        try:
            return self.db[collection].find_one({"_id": ObjectId(id)})
        except:
            return None
        

    def getNewDoc(self):
        docs = self.db.article.find()
        trigger = True
        for i in range(docs.count()):
            found = self.find_by_id(id= docs[i]["_id"], collection="stich")
            if found is None:
                return docs[i]




