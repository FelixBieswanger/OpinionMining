from database import Database
from random import randint

db = Database()

data = db.get_all("selected")
selected = list()

while(len(selected) < 50):
    randindex = randint(0, len(data))
    if randindex not in selected:
        db.insert_one(collection="sample",data=data[randindex])
        selected.append(randindex)


