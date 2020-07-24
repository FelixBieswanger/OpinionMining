import sys
sys.path.append("./")
import pyLDAvis.gensim
import gensim
from gensim import corpora
from resources.database import Database
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
ldamodel = gensim.models.ldamodel.LdaModel.load("./data_selection/lda_models/lda_t22_07072020_103348.model")

selected_topics = [3, 18, 19, 20]
document_topics = [ldamodel.get_document_topics(item) for item in corpus]

result = list()
for topics, art in zip(document_topics, source_data):
    trigger = False
    for topic in topics:
        if topic[0] in selected_topics and topic[1] > 0.3:
            trigger = True
    if trigger:
        art["topics"] = [t[0] for t in topics if t[1] > 0.1]
        result.append(art)

counter = 0
for art in result:
    db.insert_one(collection="selected2",data=art)
    counter +=1 
    print(counter,"/",len(result))


