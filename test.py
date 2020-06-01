from database import Database



db= Database()

deutsche = db.get_querry(collection="article", querry={
                     "$or": [{"source": "sueddeutsche"}, {"source": "zeit"}]})

print(deutsche[2500])