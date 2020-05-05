from database import Database

db = Database()

counter = 0

for doc in db.get_all(collection="article"):
    try:
        if doc["text"].count("digitization") >= 2:
            print(doc[""])
            counter+=1
    except:
        pass
   
adsd
print(counter)


