import plotly.graph_objects as go
import plotly.express as px
import pickle
import pandas as pd
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

source_data = db.get_all(collection="date")
source_urls = [ i["article_url"] for i in source_data]

class EpochLogger(CallbackAny2Vec):
    '''Callback to log information about training'''

    def __init__(self):
        self.epoch = 0

    def on_epoch_begin(self, model):
        print("Epoch #{} start".format(self.epoch))

    def on_epoch_end(self, model):
        print("Epoch #{} end".format(self.epoch))
        self.epoch += 1


d2v_model = Doc2Vec.load("doc2vec_models/doc2vec_07032020_110834.model")

original_vecs = sk_pre.StandardScaler().fit_transform(d2v_model.docvecs.vectors_docs)
vecs = PCA(n_components=3).fit_transform(original_vecs)


d_true=list()
d_false=list()

model_urls = d2v_model.docvecs.index2entity
for url,vec in zip(model_urls,vecs):
    index = source_urls.index(url)

    if source_data[index]["marker"] == True:
        d_true.append(vec)
    else:
        d_false.append(vec)


d_true = np.array(d_true)
d_false = np.array(d_false)

size= 3

figdata = [
    go.Scatter3d(x=d_true[:, 0], y=d_true[:, 1], z=d_true[:, 2], mode="markers",
                 marker=dict(size=size),name="Contains Digital*"),
    go.Scatter3d(x=d_false[:, 0], y=d_false[:, 1], z=d_false[:, 2], mode="markers",
                 marker=dict(size=size), name="Not Containing")
]

layout = dict(title='Doc2Vec Vizual', showlegend=True)
fig = go.Figure(data=figdata, layout=layout)
fig.show()





