import pyLDAvis.gensim
import gensim
from gensim import corpora
from pymongo import MongoClient
import numpy as np
import pandas as pd
import random
from datetime import datetime
from gensim.models import CoherenceModel
import os
import matplotlib.pyplot as plt
from database import Database

db = Database()

source_data = db.get_all(collection="date")
text = [i["lda"] for i in source_data]
text_data = [t.split(" ") for t in text]
dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]

result = dict()
path = "/Users/felixbieswanger/Desktop/Uni_Stuff/Bachelorarbeit/OpionionMining/lda_models/"
for file in os.listdir(path):
    split = file.split(".")
    split2 = file.split("_")
    if split[1] == "model" and len(split) == 2 and len(split2) == 4:
        print(file)
        para = split2[1]

        ldamodel = gensim.models.ldamodel.LdaModel.load(path+file)
        coherence_model_lda = CoherenceModel(
            model=ldamodel, texts=text_data, corpus=corpus, dictionary=dictionary, topn=15, coherence='c_v')
        coherence = coherence_model_lda.get_coherence()
        print(coherence)
        result[para] = coherence

pd.Series(result, index=result.keys()).to_csv("result_lda.csv")


y = list(result.values())
x = list(result.keys())
for i in range(len(x)):
    x[i] = int(x[i][1:])

x, y = zip(*sorted(zip(x, y)))

plt.figure(figsize=(15, 8), dpi=200)
plt.ylabel("c_v value")
plt.xlabel("Number of Topics")
plt.title("Coherence Score")
plt.plot(x, y)
plt.savefig("coherenceplt.png")
