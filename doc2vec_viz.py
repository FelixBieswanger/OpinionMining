import plotly.graph_objects as go
import plotly.express as px
import pickle
import pandas as pd
import numpy
from datetime import datetime
import random
import numpy as np
import gensim
from sklearn import preprocessing as sk_pre
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.decomposition import PCA
from gensim.models import Doc2Vec
from database import Database
import preprocessing
from gensim.models.callbacks import CallbackAny2Vec


SEED = 42

db = Database()

data = db.get_querry(collection="article", querry={
                     "$or": [{"source": "sueddeutsche"}, {"source": "zeit"}]})

#1: Digitalisierung,    0 Kein Digitalisierung
actual_label = list()

digitalisierung = list()
for doc in data:
    if doc["text"].count("Digitalisierung") >= 6:
        digitalisierung.append(doc)
        actual_label.append(1)

kein_digitalisierung = list()
for doc in data:
    if doc["text"].count("Digitalisierung") == 1:
        kein_digitalisierung.append(doc)
        actual_label.append(0)

    if len(digitalisierung)*5 == len(kein_digitalisierung):
        break

print("len digi",len(digitalisierung))
print("len not digi",len(kein_digitalisierung))

data = digitalisierung+kein_digitalisierung

hovertext = list()
for doc,label in zip(data,actual_label):
    if label == 1:
        hovertext.append(doc["headline"]+"<br>"+"<b>Label</b>: Digi")
    else:
        hovertext.append(doc["headline"]+"<br>"+"<b>Label</b>: Not Digi")

train = [preprocessing.clean_string(i["text"]) for i in data]
#train = preprocessing.get_lemma(train)

LabeledSentence1 = gensim.models.doc2vec.TaggedDocument
all_content_train = list()
for doc in train:
    all_content_train.append(LabeledSentence1(doc, ["doc"+str(train.index(doc))]))

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

d2v_model = Doc2Vec(all_content_train, vector_size=400, window=9,
                    min_count=2, workers=4, dm=1, alpha=0.025, min_alpha=0.001, callbacks=[epochlogger],seed=SEED)
d2v_model.train(all_content_train, total_examples=d2v_model.corpus_count,
                epochs=200, start_alpha=0.002)

vecs = sk_pre.StandardScaler().fit_transform(d2v_model.docvecs.vectors_docs)
vecs = PCA(n_components=3).fit_transform(vecs)



digi = list()
notdigi = list()
hovertext0 = list()
hovertext1 = list()

for label,vec,hover in zip(actual_label,vecs,hovertext):
    if label == 1:
        digi.append(vec)
        hovertext0.append(hover)
    else:
        notdigi.append(vec)
        hovertext1.append(hover)

print("after len digi",len(digi))
print("after len notdigi", len(notdigi))


digi = np.array(digi)
notdigi = np.array(notdigi)


fig = go.Figure(data=[
    go.Scatter3d(x=digi[:, 0], y=digi[:, 1], z=digi[:, 2],
                 mode='markers',name="Digi", hovertext=hovertext0, marker={"size": 3}),
    go.Scatter3d(x=notdigi[:, 0], name="Not Digi", y=notdigi[:, 1], z=notdigi[:, 2],
                 mode='markers', hovertext=hovertext1, marker={"size": 3})
    ])


fig.write_html("/Users/felixbieswanger/Downloads/result" +
               datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")+".html")
fig.show()
