import pyLDAvis.gensim
import gensim
from gensim import corpora
from database import Database
import preprocessing
import numpy as np
import random
from datetime import datetime

db = Database()

data = db.get_all(collection="date")
texts = [i["noun_lemma"] for i in data]
text_data = preprocessing.preprocessing_lda(texts)

dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=20, id2word=dictionary, passes=100)

now = datetime.now()
stringtime = now.strftime("%m%d%Y_%H%M%S")
ldamodel.save("lda_models/lda_"+stringtime+".model")

document_topics = [ldamodel.get_document_topics(item) for item in corpus]

for topic, art in zip(document_topics, data):
    art["topics"] = topic
    db.update_article(collection="date",data=art)