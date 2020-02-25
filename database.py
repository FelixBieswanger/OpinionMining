from pymongo import MongoClient

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





def test():
    pass




