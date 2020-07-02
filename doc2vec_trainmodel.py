import pandas as pd
import numpy
from datetime import datetime
import random
import numpy as np
import gensim
from gensim.models import Doc2Vec
from database import Database
import preprocessing
from gensim.models.callbacks import CallbackAny2Vec

SEED = 42

db = Database()

data = db.get_all(collection="date")
train = [doc["noun_lemma"] for doc in data]

LabeledSentence1 = gensim.models.doc2vec.TaggedDocument
all_content_train = list()
for doc in train:
    all_content_train.append(LabeledSentence1(doc, [data[train.index(doc)]["article_url"]]))

class EpochLogger(CallbackAny2Vec):
    '''Callback to log information about training'''
    def __init__(self):
        self.epoch = 0

    def on_epoch_begin(self, model):
        print("Epoch #{} start".format(self.epoch))
    
    def on_epoch_end(self, model): 
        print("Epoch #{} end".format(self.epoch))
        self.epoch += 1

epochlogger = EpochLogger()

d2v_model = Doc2Vec(all_content_train, vector_size=100, window=6,
                    min_count=2, workers=4, dm=1, alpha=0.025, min_alpha=0.001, callbacks=[epochlogger],seed=SEED)
d2v_model.train(all_content_train, total_examples=d2v_model.corpus_count, epochs=100)

now = datetime.now()
stringtime = now.strftime("%m%d%Y_%H%M%S")

d2v_model.save("doc2vec_models/doc2vec_"+stringtime+".model")
