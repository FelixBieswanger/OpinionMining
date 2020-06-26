import matplotlib.pyplot as plt
import os
import sys
sys.path.append("./")
from database import Database
import pandas as pd
import numpy as np

db = Database()
filename = os.path.basename(__file__).split(".")[0]


all_articles = db.get_all(collection="article")
df = pd.DataFrame(all_articles)
dfg = df[["_id", "source", "search-term"]].groupby(["source", "search-term"], as_index=False).count()
sources = dfg["source"].unique()
terms = dfg["search-term"].unique()

store = dict()
for term in terms:
    result = list()
    for source in sources:
        if source in dfg.loc[dfg["search-term"] == term]["source"].to_list():
            count = int(dfg.loc[(dfg["source"] == source) &
                                (dfg["search-term"] == term)]["_id"])
            result.append(count)
        else:
            result.append(0)
    store[term] = result

new_store = dict()
new_store["digitalization/digitalisation"] = np.array((0, 0, 0, 0, 0, 0))
new_store["digitization/digitisation"] = np.array((0, 0, 0, 0, 0, 0))
for term in store.keys():
    if term == "digitalization" or term == "digitalisation":
        new_store["digitalization/digitalisation"] += np.array(store[term])
        continue
    if term == "digitization" or term == "digitisation":
        new_store["digitization/digitisation"] += np.array(store[term])
        continue
    new_store[term] = store[term]

store = new_store
plot_hand = list()
terms = list(store.keys())
width = 0.5
plt.figure(figsize=(10, 5), dpi=200)
for term, arr in zip(terms, store.values()):
    indexterm = terms.index(term)
    if indexterm == 0:
        plot_hand.append(plt.bar(sources, store[term], width)[0])

    else:
        sum_arr = np.array((0, 0, 0, 0, 0, 0))
        for prevterm in terms[:indexterm]:
            sum_arr += np.array(store[prevterm])
        plot_hand.append(
            plt.bar(sources, store[term], width, bottom=sum_arr)[0])

plt.legend(plot_hand, list(store.keys()))
plt.savefig("plots/images/"+filename+".png")
