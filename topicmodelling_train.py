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

db = Database()

source_data = db.get_all(collection="date")
text = [i["lda"] for i in source_data]
text_data = [t.split(" ") for t in text]

dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]

num_topics = [15,20,25,30]
passes = [50,100,150]

results = dict()

for topic in num_topics:
    for passnum in passes:

        if (topic == 15 and passnum == 50) or (topic == 15 and passnum == 100):
            print("continue")
            continue

        try:
            ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=topic, id2word=dictionary, passes=passnum)
            name = "lda_t"+str(topic)+"_p"+str(passnum)+"_"

            now = datetime.now()
            stringtime = now.strftime("%m%d%Y_%H%M%S")

            ldamodel.save("lda_models/"+name+stringtime+".model")

            coherence_model_lda = CoherenceModel(model=ldamodel, texts=text_data, dictionary=dictionary, coherence='c_v')
            results[name] = coherence_model_lda.get_coherence()

            print("done",topic,passnum)
        except Exception as e:
            with open("lda_log.txt","a") as file:
                file.write(e)

pd.Series(result, index=result.keys()).to_csv("result_lda.csv")


