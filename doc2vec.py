import matplotlib.pyplot as plt
import pickle
import pandas as pd
import numpy
import random
import re
import os
import numpy as np
import gensim
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from gensim.models import Doc2Vec
from database import Database
import preprocessing
import spacy
from matplotlib.colors import ListedColormap



db = Database()

data = db.get_all(collection="article")
search_terms = [i["search-term"] for i in data]
train = [preprocessing.clean_string(i["text"]) for i in data]
train = preprocessing.get_lemma(train)

LabeledSentence1 = gensim.models.doc2vec.TaggedDocument
all_content_train = list()
for doc in train:
    all_content_train.append(LabeledSentence1(doc,[train.index(doc)]))


d2v_model = Doc2Vec(all_content_train, size=300, window=10,
                    min_count=2, workers=4, dm=1, alpha=0.025, min_alpha=0.001)
d2v_model.train(all_content_train, total_examples=d2v_model.corpus_count,
                epochs=300, start_alpha=0.002, end_alpha=-0.016)


cluster_num = 1

kmeans_model = KMeans(n_clusters=cluster_num,max_iter=50)
X = kmeans_model.fit(d2v_model.docvecs.doctag_syn0)
labels = kmeans_model.labels_.tolist()
l = kmeans_model.fit_predict(d2v_model.docvecs.doctag_syn0)
pca = PCA(n_components=2).fit(d2v_model.docvecs.doctag_syn0)
datapoint = pca.transform(d2v_model.docvecs.doctag_syn0)

plt.figure
label1 = list()
for i in range(cluster_num):
    random_number = random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    hex_number = '#' + hex_number[2:]
    label1.append(hex_number)

colors = [label1[i] for i in labels]

fig = plt.figure()
colours = ListedColormap(['r', 'b', 'g'])
scatter=plt.scatter(datapoint[:, 0], datapoint[:, 1], c=labels, cmap=colours)
plt.legend(handles=scatter.legend_elements()[0],labels=["Digitalisierung","Coronoa","Fußball"])
centroids = kmeans_model.cluster_centers_
centroidpoint = pca.transform(centroids)
plt.scatter(centroidpoint[:, 0], centroidpoint[:, 1], marker="^", s=150, c="#000000")
plt.show()





