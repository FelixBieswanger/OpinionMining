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


db = Database()

source_data = db.get_all(collection="article")


class EpochLogger(CallbackAny2Vec):
    '''Callback to log information about training'''

    def __init__(self):
        self.epoch = 0

    def on_epoch_begin(self, model):
        print("Epoch #{} start".format(self.epoch))

    def on_epoch_end(self, model):
        print("Epoch #{} end".format(self.epoch))
        self.epoch += 1


d2v_model = Doc2Vec.load("doc2vec_models/doc2vec_07022020_105155.model")

original_vecs = sk_pre.StandardScaler().fit_transform(d2v_model.docvecs.vectors_docs)
pca = PCA(n_components=100).fit(original_vecs)

sum_pca_variance = 0.0
pca_variance_threshold = 0
for variance in pca.explained_variance_ratio_:
    sum_pca_variance += variance

    if sum_pca_variance >= 0.90:
        pca_variance_threshold = pca.explained_variance_ratio_.tolist().index(variance)
        break

print(pca_variance_threshold)
train_vecs = pca.transform(original_vecs)
train_vecs = train_vecs[:, :pca_variance_threshold]

model = KMeans(n_clusters=10)
dbscan_model = model.fit(train_vecs)
labels = model.labels_.tolist()
model_urls = d2v_model.docvecs.index2entity


for label, url in zip(labels, model_urls):
    index = 0
    for sdata in source_data:
        if sdata["article_url"] == url:
            index = source_data.index(sdata)
            break
    
    source_data[index]["label"] = label


#TO DO COUNT DIGITALISIERUNG PRO CLUSTER




