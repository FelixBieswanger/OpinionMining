import matplotlib.pyplot as plt
import sys
sys.path.append("./")
import pyLDAvis.gensim
import gensim
from gensim import corpora
from resources.database import Database
import resources.preprocessing as pre
import numpy as np
import pandas as pd
import random
from datetime import datetime
import resources.color_sheme as color_sheme

colors = color_sheme.get_colors_lang()


db = Database()
topic_names = pd.read_csv("resources/interpretation.csv")["Ergebnis"].to_list()
source_data = db.get_all(collection="date")
text = [i["lda"] for i in source_data]
text_data = [t.split(" ") for t in text]
dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]
ldamodel = gensim.models.ldamodel.LdaModel.load("data_selection/lda_models/lda_t22_07072020_103348.model")

selected_topics = [3, 18, 19, 20]
document_topics = [ldamodel.get_document_topics(item) for item in corpus]

suretopics = list()
for doc in document_topics:
    for topic in doc:
        if topic[1] > 0.3:
            suretopics.append(topic[0])

fig, ax = plt.subplots(figsize=(20, 8), dpi=222)
bins = np.arange(24) - 0.5
plt.xticks(range(22), topic_names)
plt.xticks(rotation=90)
plt.xlim([-1, 22])
plt.xlabel("Topicname", fontsize=14)
plt.title("Verteilung der Themen im Korpus vor der Auswahl", fontsize=18)
plt.ylabel("Anzahl an Artikeln", fontsize=14)
N, bins, patches = ax.hist(suretopics, bins, rwidth=0.69, color=colors[0])

for i in selected_topics:
    patches[i].set_facecolor(colors[1])

plt.savefig("plots/images/histogram_topics.png",bbox_inches='tight')
