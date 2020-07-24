from database import Database
from datetime import datetime

db = Database()

all_article = db.get_all(collection="article")

for article in all_article:
    if article["date"] > datetime(2018,1,1):
        db.insert_data(collection="date",data=article)
