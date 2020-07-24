import matplotlib.pyplot as plt
import os
import sys
sys.path.append("./")
from resources.database import Database
import pandas as pd
import numpy as np

db = Database()
filename = os.path.basename(__file__).split(".")[0]

df1 = pd.DataFrame(db.get_all(collection="article"))
dfg1 = df1[["_id", "source", "language"]].groupby(
    ["source", "language"], as_index=False).count()

df2 = pd.DataFrame(db.get_all(collection="date"))
dfg2 = df2[["_id", "source", "language"]].groupby(
    ["source", "language"], as_index=False).count()

df3 = pd.DataFrame(db.get_all(collection="selected2"))
dfg3 = df3[["_id", "source", "language"]].groupby(
    ["source", "language"], as_index=False).count()

xlabel = ["en - roh","en - zeitlich", "en - inhaltlich","de - roh","de - zeitlich", "de - inhaltlich"]

store = dict()
for index, row in dfg1.iterrows():
    if row["language"] == "en":
        store[row["source"]] = [row["_id"], dfg2.loc[index]["_id"], dfg3.loc[index]["_id"],0,0,0]
    else:
        store[row["source"]] = [0, 0, 0, row["_id"],dfg2.loc[index]["_id"], dfg3.loc[index]["_id"]]

plot_hand = list()
fig, ax = plt.subplots(figsize=(17, 10), dpi=222)
width = 0.5
terms = list(store.keys())
for term, arr in zip(terms, store.values()):
    indexterm = terms.index(term)
    if indexterm == 0:
        plot_hand.append(plt.bar(xlabel, store[term], width)[0])

    else:
        sum_arr = np.array((0, 0, 0, 0,0,0))
        for prevterm in terms[:indexterm]:
            sum_arr += np.array(store[prevterm])
        plot_hand.append(
            plt.bar(xlabel, store[term], width, bottom=sum_arr)[0])


plt.ylabel("Artikelanzahl",fontsize=12)
plt.title("Verschiedene Artikelselektionen je Quelle",fontsize=18)
plt.legend(plot_hand, ["Financial Times", "Forbes",
                       "Los Angeles Times", "New York Times", "Süddeutsche Zeitung", "Zeit Online"])
plt.savefig("plots/images/"+filename+".png")
