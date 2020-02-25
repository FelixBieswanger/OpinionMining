from database import Database
import pandas as pd

db = Database()

articles = db.get_all()

l = list()
for i in articles:
    l.append(i)

df = pd.DataFrame(l)
print(df.count())
print(df.groupby("category").count()["_id"])