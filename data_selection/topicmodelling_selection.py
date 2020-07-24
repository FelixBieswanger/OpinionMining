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

"""
Get data from database
"""
db = Database()
source_data = db.get_all(collection="date")

"""
Do some preprocessing
"""
text = [i["lda"] for i in source_data]
text_data = [t.split(" ") for t in text]
dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]
#load optimal model
ldamodel = gensim.models.ldamodel.LdaModel.load("./data_selection/lda_models/lda_t22_07072020_103348.model")

#enter all selected topics from survey
selected_topics = [3, 18, 19, 20]
document_topics = [ldamodel.get_document_topics(item) for item in corpus]

"""
Take all articles assigend to selected topics with certain reliability (0.3) & 
Store topic-mix in article
"""
result = list()
for topics, art in zip(document_topics, source_data):
    trigger = False
    for topic in topics:
        if topic[0] in selected_topics and topic[1] > 0.3:
            trigger = True
    if trigger:
        art["topics"] = [t[0] for t in topics if t[1] > 0.1]
        result.append(art)

"""
Insert updated Artikel in sperate collection in database
"""
counter = 0
for art in result:
    db.insert_one(collection="selected2",data=art)
    counter +=1 
    print(counter,"/",len(result))


