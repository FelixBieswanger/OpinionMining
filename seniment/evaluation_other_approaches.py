import sys
sys.path.append("./")
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from textblob import TextBlob
import re
from statistics import mean
import datetime
import pandas as pd
from nltk import tokenize
import seaborn as sns
from resources.database import Database
import resources.preprocessing as pre
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import resources.color_sheme as color_sheme


analyser = SentimentIntensityAnalyzer()
colors = color_sheme.get_colors_lang()

"""
Method that defines all sentiment calculation approaches
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
        result_t += TextBlob(sent).sentiment.polarity
        result_v += analyser.polarity_scores(sent)["compound"]
        
    sentiments["textblob_Ansatz 1"] = result_t/len(sentences)
    sentiments["vader_Ansatz 1"] = result_v/len(sentences)
    
    
    #calc sent with headline weighted stronger
    
    sent_t = sentiments["textblob_Ansatz 1"]
    sent_v = sentiments["vader_Ansatz 1"]
    
    headline = article["headline"]
    head_t = TextBlob(headline).sentiment.polarity
    head_v = analyser.polarity_scores(headline)["compound"]
    
    weight = 3
    sentiments["textblob_Ansatz 2"] = (sent_t + head_t*weight)/(weight+1)
    sentiments["vader_Ansatz 2"] = (sent_v + head_v*weight)/(weight+1)
      
    
    #calc sentiment with stronger weigth of first and last forth of article
    try:
        text = raw_text
        fifth = int(len(text)*0.2)
        first_index = text[:fifth].rfind(".")+1
        first = text[:first_index]
        last_index =len(text)-fifth+text[len(text)-fifth:].find(".")+1
        last = text[last_index:]
        mid = text[first_index:last_index]

        text = {"first":first,"mid":mid,"last":last}
        section_result = dict()
        for sec in text.keys():
            section_result[sec] = {"t":list(),"v":list()}

        for section in section_result.keys():
            sentences = pre.get_sentences(text[section])
            for sent in sentences:
                section_result[section]["t"].append(TextBlob(sent).sentiment.polarity)
                section_result[section]["v"].append(analyser.polarity_scores(sent)["compound"])


        for section in section_result.keys():
            for tool in section_result[section].keys():
                rlist = section_result[section][tool]
                section_result[section][tool] = sum(rlist)/len(rlist)


        weight = 2
        section_sent= section_result["first"]["t"] * weight + section_result["mid"]["t"] + section_result["first"]["t"] * weight
        sentiments["textblob_Ansatz 3"] = section_sent/(weight*2+1)

        section_sent= section_result["first"]["v"] * weight + section_result["mid"]["v"] + section_result["first"]["v"] * weight
        sentiments["vader_Ansatz 3"] = section_sent/(weight*2+1)
    except Exception as e:
        print(e)
        sentiments["textblob_Ansatz 3"] = sentiments["textblob_Ansatz 1"]
        sentiments["vader_Ansatz 3"] = sentiments["vader_Ansatz 1"]

    sentiments["textblob_Ansatz 4"] = TextBlob(raw_text).sentiment.polarity
    sentiments["vader_Ansatz 4"] = analyser.polarity_scores(raw_text)["compound"]
    
    return sentiments

"""
Get relevant data from database
"""

db = Database()
source_data = db.get_all(collection="selected2")

data = {"de": list(), "en": list()}

for art in source_data:
    if art["language"] =="en":
        data["en"].append(art)
    else:
        data["de"].append(art)

"""
Calc sentiment for all approaches and store properly
"""

tools = list(calc_sent(source_data[0]).keys())

store = dict()
for tool in tools:
    store[tool] = list()

for lang in data.keys():
    for art in data[lang]:
        result = calc_sent(art)
        for tool in result.keys():
            art[tool] = result[tool]


results ={"de":dict(),"en":dict()}
for lang in data.keys():
    for tool in tools:
        results[lang][tool] = [art[tool] for art in data[lang]]

tools_plot = tools.copy()

"""
Plot all Histograms in one plot
"""

fig, ax = plt.subplots(4,2,figsize=(15,14),dpi=222)
for tool,a in zip(tools_plot,ax.flat):   
    
    data=list()
    for lang in results.keys():
        data.append(results[lang][tool])
        mean = np.array(results[lang][tool]).mean()
        sns.distplot(results[lang][tool], label=lang+", mean: " +
                     str(round(mean, 3)), ax=a, color=colors[list(results.keys()).index(lang)])
    a.legend()
    
    t, p = stats.ttest_ind(data[0], data[1], equal_var=False,axis=0)
    p = str(p/2)
    p_e = p.find("e")
    e = p[p_e:]
    p_d = p.find(".")
    d = p[:p_d+3]
    p = d+e
    tool_s = tool.split("_")
    tool_str = tool_s[0]

    if tool_str == "vader":
        tool_str = "vaderSentiment"

    a.title.set_text(tool_str+" "+tool_s[1]+", p-Wert: "+p)
fig.tight_layout(pad=3.0)
fig.suptitle("Sentimentverteilung aller Ansätze",fontsize=15)
try:
    fig.grid(False)
except:
    pass
fig.savefig("plots/images/verteilungenderalternativenansätze.png", bbox_inches='tight')

