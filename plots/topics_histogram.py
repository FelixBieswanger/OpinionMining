import matplotlib.pyplot as plt
import sys
sys.path.append("./")
import pyLDAvis.gensim
import gensim
from gensim import corpora
from database import Database
import preprocessing as pre
import numpy as np
import random
from datetime import datetime


db = Database()

source_data = db.get_all(collection="date")
text = [i["lda"] for i in source_data]
text_data = [t.split(" ") for t in text]
dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]
ldamodel = gensim.models.ldamodel.LdaModel.load("data_selection/lda_models/lda_t22_07072020_103348.model")

selected_topics = [3, 7, 18, 19, 20]
document_topics = [ldamodel.get_document_topics(item) for item in corpus]

cleantopics = list()
for doc in document_topics:
    for topic in doc:
        if topic[1] > 0.1:
            cleantopics.append(topic[0])

fig, ax = plt.subplots(figsize=(20, 8), dpi=222)
bins = np.arange(24) - 0.5
plt.xticks(range(22))
plt.xlim([-1, 22])
plt.title("Verteilung der Themen im Korpus")
plt.xlabel("Topic Number")
plt.ylabel("Count")
N, bins, patches = ax.hist(cleantopics, bins, rwidth=0.69)

for i in selected_topics:
    patches[i].set_facecolor('r')

plt.savefig("plots/images/histogram_topics.png")
