from database import Database
from random import randint

db = Database()
"""
Get Data from Database
"""
data = db.get_all("selected")
selected = list()

"""
Randomly select 50 unique Articles
"""

while(len(selected) < 50):
    randindex = randint(0, len(data))
    if randindex not in selected:
        db.insert_one(collection="sample",data=data[randindex])
        selected.append(randindex)


