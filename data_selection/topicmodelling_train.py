import pyLDAvis.gensim
import gensim
from gensim import corpora
from database import Database
import preprocessing
import numpy as np
import pandas as pd
import random
from datetime import datetime
from gensim.models import CoherenceModel

"""
Get data from database
"""
db = Database()
source_data = db.get_all(collection="date")

"""
Do Some preprocessing
"""
text = [i["lda"] for i in source_data]
text_data = [t.split(" ") for t in text]
dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]

"""
Do small grid search with different topic numbers &
Storing the models for later evaluation
"""

for topic in [i for i in range(1, 50, 7)]:
        try:
            ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=topic, id2word=dictionary, passes=25)
            name = "lda_t"+str(topic)+"_"
            now = datetime.now()
            stringtime = now.strftime("%m%d%Y_%H%M%S")
            ldamodel.save("lda_models/"+name+stringtime+".model")

            print("done",topic)
        except Exception as e:
            with open("lda_log.txt","a") as file:
                file.write(e)


