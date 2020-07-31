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

analyser = SentimentIntensityAnalyzer()


"""
Calc Sentiment
"""
def calc_sent(article):

    count_ex = 0
    sentiments = dict()
    raw_text = pre.clean_string(article["text"])
    sentences = pre.get_sentences(raw_text)

    #calc sent without any further weighting
    result_t = 0
    result_v = 0
    for sent in sentences:
        result_v += analyser.polarity_scores(sent)["compound"]

    sentiments["vader_ansatz1"] = result_v/len(sentences)

    #calc sentiment with stronger weigth of first and last forth of article
    try:
        text = raw_text
        fifth = int(len(text)*0.2)
        first_index = text[:fifth].rfind(".")+1
        first = text[:first_index]
        last_index = len(text)-fifth+text[len(text)-fifth:].find(".")+1
        last = text[last_index:]
        mid = text[first_index:last_index]

        text = {"first": first, "mid": mid, "last": last}
        section_result = dict()
        for sec in text.keys():
            section_result[sec] = {"t": list(), "v": list()}

        for section in section_result.keys():
            sentences = pre.get_sentences(text[section])
            for sent in sentences:
                section_result[section]["t"].append(
                    TextBlob(sent).sentiment.polarity)
                section_result[section]["v"].append(
                    analyser.polarity_scores(sent)["compound"])

        for section in section_result.keys():
            for tool in section_result[section].keys():
                rlist = section_result[section][tool]
                section_result[section][tool] = sum(rlist)/len(rlist)

        weight = 2
        section_sent = section_result["first"]["t"] * weight + \
            section_result["mid"]["t"] + section_result["first"]["t"] * weight
        sentiments["textblob_ansatz3"] = section_sent/(weight*2+1)

        section_sent = section_result["first"]["v"] * weight + \
            section_result["mid"]["v"] + section_result["first"]["v"] * weight
        sentiments["vader_ansatz3"] = section_sent/(weight*2+1)
    except Exception as e:
        sentiments["vader_ansatz3"] = sentiments["vader_ansatz1"]

    return sentiments

"""
Get relevant Data from database
"""

db = Database()
source_data = db.get_all(collection="selected2")

"""
Calculate Sentiment and store values
"""

data = {"Anglo-Amerikanischer Sprachraum": list(), "Deutscher Sprachraum": list()}

for art in source_data:
    art["sentiment"] = calc_sent(art)["vader_ansatz3"]
    db.update_article(collection="selected2",data=art)
    if art["language"] == "en":
        data["Anglo-Amerikanischer Sprachraum"].append(art)
    else:
        data["Deutscher Sprachraum"].append(art)

"""
Calculate t-Test and mean
"""

t, p = stats.ttest_ind(data["Anglo-Amerikanischer Sprachraum"],
                       data["Deutscher Sprachraum"], equal_var=False, axis=0)
mean_en = np.array(data["Anglo-Amerikanischer Sprachraum"]).mean()
mean_de = np.array(data["Deutscher Sprachraum"]).mean()

print("t-statistic value", t)
print("p-value ttest", p/2)
print("mean en:", mean_en, "         mean de:", mean_de)
