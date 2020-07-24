from database import Database
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random
from nltk.corpus import stopwords
import preprocessing
import matplotlib.pyplot as plt

analyser = SentimentIntensityAnalyzer()


def calc_sent_vader(article):
    return sentiment


def calc_sent_textblob(article):
    text = preprocessing.clean_string(article["text"])
    sentences = preprocessing.get_sentences(text)


    result = 0
    for sent in sentences:
        result += TextBlob(sent).sentiment.polarity

    return round(result/len(sentences), 3)


en_articles = db.get_querry(collection="selected",querry={"language":"en"})
print("en_articles",len(en_articles))
de_articles = db.get_querry(collection="selected",querry={"language":"de"})
print("de_articles", len(de_articles))


data = [en_articles,de_articles]


results_en = list()
results_de = list()

for stichprobe in data:
    for art in stichprobe:
        if data.index(stichprobe) == 0:
            #en
            results_en.append(calc_sent_textblob(art))
        else:
            #de
            results_de.append(calc_sent_textblob(art))
        

plt.hist(results_en)
plt.show()
plt.hist(results_de)
plt.show()


