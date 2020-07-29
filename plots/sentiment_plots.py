import sys
sys.path.append("./")
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import seaborn as sns
from nltk import tokenize
import datetime
from statistics import mean
import re
from textblob import TextBlob
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
from resources.database import Database
import resources.preprocessing as pre
import pandas as pd


"""
Get Data
"""

db = Database()
source_data = db.get_all(collection="selected2")

data = {
    "Anglo-Amerikanischer Sprachraum": [art for art in source_data if art["language"]=="en"],
    "Deutscher Sprachraum": [art for art in source_data if art["language"] == "de"]
    }

"""
Plot Histogram
"""

#plot en vs de
plt.figure(figsize=(10, 10), dpi=222)
sent = dict()
for lang in data.keys():
    sent[lang] = [art["sentiment"] for art in data[lang]]
    sns.distplot(sent[lang], label=lang+", mean=" +
                 str(round(mean(sent[lang]), 3)), kde=False)

plt.xlabel("Tonalität")
plt.ylabel("Häufigkeit")
plt.title("Verteilung des Sentiments je Sprachraum")
plt.legend()
plt.savefig("plots/images/verteilung_sentiment.png")


"""
Plot TimeSeries
"""

plt.figure(figsize=(15,8))
for lang in data.keys():
    x = list()
    y = list()
    for art in data[lang]:
        x.append(art["date"])
        y.append(art["sentiment"])
    x, y = zip(*sorted(zip(x, y)))
    y = SimpleExpSmoothing(y).fit(smoothing_level=0.075).fittedvalues
    plt.plot(x,y,label=lang)
    
    # calc the trendline
    x1 = [i.timestamp() for i in x]
    z = np.polyfit(x1, y, 1)
    p = np.poly1d(z)
    trendline_function="y="+str(z[0])+"x +("+str(z[1])+")"
    plt.plot(x,p(x1),label=lang+" trendline: "+trendline_function)  
plt.title("Tonalität im Zeitverlauf",fontsize=15)
plt.ylabel("Tonalität",fontsize=12)
plt.legend()
plt.savefig("plots/images/zeitreihen.png",bbox_inches='tight')


"""
Plot Correlation with meta-data
"""

topic_names = pd.read_csv("resources/interpretation.csv")["Ergebnis"].to_list()

topics = list()
for art in source_data:
    topics.append([topic_names[t] for t in art["topics"]])


from mlxtend.preprocessing import TransactionEncoder

te = TransactionEncoder()
te_ary = te.fit(topics).transform(topics)
df = pd.DataFrame(te_ary, columns=te.columns_)

sources= [[art["source"]] for art in source_data]
te_ary = te.fit(sources).transform(sources)
df2 = pd.DataFrame(te_ary, columns=te.columns_)

lang = [[art["language"]] for art in source_data]
te_ary = te.fit(lang).transform(lang)
df3 = pd.DataFrame(te_ary, columns=te.columns_)

df["Datum"] = [art["date"].timestamp() for art in source_data]
df["Quelle"] = [art["source"] for art in source_data]
df["Artikellänge"] = [len(art["text"]) for art in source_data]
df["Sentiment"] = [art["sentiment"] for art in source_data]
df = df.join(df2)
df = df.join(df3)
corr = df.corr()
corrdict = corr["Sentiment"].to_dict()


del corrdict["Sentiment"]
for key in list(corrdict.keys()):
    v = corrdict[key]
    cuttof = 0.1
    if (v < 0 and v > -cuttof):
        del corrdict[key]
    if (v > 0 and v < cuttof):
        del corrdict[key]

x = list(corrdict.keys())
y = list(corrdict.values())

plt.figure(figsize=(10,5),dpi=222)
plt.xticks(rotation=90)
plt.ylabel("Korrelation",fontsize=12)
plt.title("Korrelation mit Sentiment",fontsize=15)
plt.bar(x,y)
plt.savefig("plots/images/correlation.png", bbox_inches='tight')


"""
Plot Boxplot of Sources
"""

fig, ax = plt.subplots(figsize=(5,7),dpi=222)

s_data = dict()
sources = list(pd.DataFrame(source_data)["source"].unique())
for source in sources:
    s_data[source] = [art["sentiment"] for art in source_data if art["source"] == source]
ax.boxplot(s_data.values(),showmeans=True,showfliers=False)
ax.set_xticklabels(s_data.keys())

for source in sources:
    mea = round(mean(s_data[source]),3)
    plt.text(sources.index(source)+0.77,mea+0.02, str(mea), fontsize=8)


plt.xticks(rotation=90)
plt.ylabel("Tonalität")
plt.title("Durchschnittliche Tonalität je Quelle",fontsize=10)
plt.savefig("plots/images/barchart_source.png",bbox_inches = 'tight')



"""
Plot Boxplot mean sentiment regarding topics and source language
"""

sentiments = dict()
srange = [i for i in range(22)]
for topic in srange:
    sentiments[topic_names[topic]] = dict()
    for lang in ["de", "en"]:
        sentiments[topic_names[topic]][lang] = list()

for art in source_data:
    for topic in art["topics"]:
        sentiments[topic_names[topic]][art["language"]].append(
            art["sentiment"])


de_means = list()
en_means = list()
for topic in sentiments.keys():
    de_means.append(mean(sentiments[topic]["de"]))
    en_means.append(mean(sentiments[topic]["en"]))


labels = list(sentiments.keys())
x = np.arange(len(labels))  # the label locations
width = 0.3  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
rects1 = ax.bar(x - width/2, de_means, width, label='de')
rects2 = ax.bar(x + width/2, en_means, width, label='en')

ax.set_ylabel('Tonalität')
ax.set_title('Durchschnittliche Tonalität je Topic')
ax.set_xticks(x)
ax.set_xticklabels(labels)
plt.legend()
plt.xticks(rotation=90)
plt.savefig("plots/images/mean_sentiment_topic.png")
    
