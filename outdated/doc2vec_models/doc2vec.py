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
    if doc["text"].count("Digitalisierung") >= 5:
        digitalisierung.append(doc)
        actual_label.append(1)

kein_digitalisierung = list()
for doc in data:
    if doc["text"].count("Digitalisierung") == 1:
        kein_digitalisierung.append(doc)
        actual_label.append(0)

    if len(digitalisierung) == len(kein_digitalisierung):
        break

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

d2v_model = Doc2Vec(all_content_train, vector_size=200, window=5,
                    min_count=2, workers=4, dm=0, alpha=0.025, min_alpha=0.001, callbacks=[epochlogger],seed=SEED)
d2v_model.train(all_content_train, total_examples=d2v_model.corpus_count,
                epochs=100, start_alpha=0.002)


model = KMeans(max_iter=300,random_state=SEED)
#model = DBSCAN(eps=0.001,min_samples=40)
vecs = sk_pre.StandardScaler().fit_transform(d2v_model.docvecs.vectors_docs)
pca = PCA(n_components=200).fit(vecs)

sum_pca_variance = 0.0
pca_variance_threshold = 0
for variance in pca.explained_variance_ratio_:
    sum_pca_variance += variance

    if sum_pca_variance >= 0.90:
        pca_variance_threshold = pca.explained_variance_ratio_.tolist().index(variance)
        break


print(pca_variance_threshold)
vecs = pca.transform(vecs)
vecs = vecs[:,:pca_variance_threshold]

km = model.fit(vecs)
labels = model.labels_.tolist()
datapoint = vecs[:,:3]

closest, _ = pairwise_distances_argmin_min(km.cluster_centers_, vecs)
index_clostest_0 = closest[0]
index_clostest_1 = closest[1]

cluster0 = list()
hovertext0 = list()

cluster1 = list()
hovertext1 = list()

for label,hover,data in zip(labels,hovertext,datapoint):
    if label == 0:
        cluster0.append(data)
        hovertext0.append(hover)
    else:
        cluster1.append(data)
        hovertext1.append(hover)

cluster0 = np.array(cluster0)
cluster1 = np.array(cluster1)

fig = go.Figure(data=[
    go.Scatter3d(x=cluster0[:, 0], y=cluster0[:, 1], z=cluster0[:, 2],
                 mode='markers',name="Cluster 0", hovertext=hovertext0, marker={"size": 3}),
    go.Scatter3d(x=cluster1[:, 0],name="Cluster 1", y=cluster1[:, 1], z=cluster1[:, 2],
                 mode='markers', hovertext=hovertext1, marker={"size": 3})
    ])

"""
fig.update_layout({
    "scene":{
        "annotations":[
            {
                "x":datapoint[index_clostest_0, 0],
                "y":datapoint[index_clostest_0, 1],
                "z":datapoint[index_clostest_0, 2],
                "text":"Most Typical Article Cluster 0 <br>"+hovertext[index_clostest_0],
                "ax": 0,
                "ay":-300
            },
            {
                "x": datapoint[index_clostest_1, 0],
                "y":datapoint[index_clostest_1, 1],
                "z":datapoint[index_clostest_1, 2],
                "text":"Most Typical Article Cluster 1 <br>"+hovertext[index_clostest_1],
                "ax": 0,
                "ay":-300
            }
        ]
    }
})

"""


fig.write_html("/Users/felixbieswanger/Downloads/result" +
               datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")+".html")
fig.show()
