from database import Database
from datetime import datetime

"""
Get all data from Database
"""
db = Database()
all_article = db.get_all(collection="article")

"""
Insert all articles newer than january 2019 into sperate collection in database
"""
for article in all_article:
    if article["date"] > datetime(2019,1,1):
        db.insert_data(collection="date",data=article)
