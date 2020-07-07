from database import Database
from random import randint

db = Database()

data = db.get_all("selected")
indieces = [i for i in range(len(data))]

for i in range(50):
    randindex = randint(0, len(indieces))
    db.insert_one(collection="sample",data=data[randindex])
    indieces.remove(randindex)


