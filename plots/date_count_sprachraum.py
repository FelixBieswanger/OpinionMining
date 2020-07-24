import matplotlib.pyplot as plt
import os
import sys
sys.path.append("./")
from database import Database
import pandas as pd
import numpy as np

db = Database()
filename = os.path.basename(__file__).split(".")[0]


all_articles = db.get_all(collection="date")
df = pd.DataFrame(all_articles)
dfg = df[["_id", "source", "language"]].groupby(["source", "language"], as_index=False).count()
sources = dfg["source"].unique()
languages = dfg["language"].unique()

store = dict()
for index, row in dfg.iterrows():
    if row["language"] == "en":
        store[row["source"]] = [row["_id"], 0]
    else:
        store[row["source"]] = [0, row["_id"]]

plot_hand = list()
width = 0.5
terms = list(store.keys())
plt.figure(figsize=(10, 5), dpi=200)
for term, arr in zip(terms, store.values()):
    indexterm = terms.index(term)
    if indexterm == 0:
        plot_hand.append(plt.bar(languages, store[term], width)[0])

    else:
        sum_arr = np.array((0, 0))
        for prevterm in terms[:indexterm]:
            sum_arr += np.array(store[prevterm])
        plot_hand.append(
            plt.bar(languages, store[term], width, bottom=sum_arr)[0])

plt.legend(plot_hand, list(store.keys()))
plt.savefig("plots/images/"+filename+".png")
