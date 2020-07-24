import sys
sys.path.append("./")
import pandas as pd
import resources.preprocessing as pre
from resources.database import Database
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
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
analyser = SentimentIntensityAnalyzer()


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
        
    sentiments["textblob_ansatz1"] = result_t/len(sentences)
    sentiments["vader_ansatz1"] = result_v/len(sentences)
    
    
    #calc sent with headline weighted stronger
    
    sent_t = sentiments["textblob_ansatz1"]
    sent_v = sentiments["vader_ansatz1"]
    
    headline = article["headline"]
    head_t = TextBlob(headline).sentiment.polarity
    head_v = analyser.polarity_scores(headline)["compound"]
    
    weight = 3
    sentiments["textblob_ansatz2"] = (sent_t + head_t*weight)/(weight+1)
    sentiments["vader_ansatz2"] = (sent_v + head_v*weight)/(weight+1)
      
    
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
        sentiments["textblob_ansatz3"] = section_sent/(weight*2+1)

        section_sent= section_result["first"]["v"] * weight + section_result["mid"]["v"] + section_result["first"]["v"] * weight
        sentiments["vader_ansatz3"] = section_sent/(weight*2+1)
    except Exception as e:
        print(e)
        sentiments["textblob_ansatz3"] = sentiments["textblob_ansatz1"]
        sentiments["vader_ansatz3"] = sentiments["vader_ansatz1"]

        
    sentiments["textblob_ansatz4"] = TextBlob(raw_text).sentiment.polarity
    sentiments["vader_ansatz4"] = analyser.polarity_scores(raw_text)["compound"]
    
    return sentiments



db = Database()
source_data = db.get_all(collection="selected2")

data = {"Anglo-Amerikanischer Sprachraum":list(),"Deutscher Sprachraum":list()}

for art in source_data:
    art["sentiment"] = calc_sent(art)["vader_ansatz3"]
    if art["language"] =="en":
        data["Anglo-Amerikanischer Sprachraum"].append(art)
    else:
        data["Deutscher Sprachraum"].append(art)

#plot en vs de
plt.figure(figsize=(10,10),dpi=222)
sent = dict()
for lang in data.keys():
    sent[lang] = [art["sentiment"] for art in data[lang]]
    sns.distplot(sent[lang],label=lang+", mean="+str(round(mean(sent[lang]),3)),kde=False)
    
plt.xlabel("Tonalität")
plt.ylabel("Häufigkeit")
plt.title("Verteilung des Sentiments je Sprachraum")
plt.legend()
plt.savefig("plots/images/verteilung_sentiment.png")


t, p = stats.ttest_ind(sent["Anglo-Amerikanischer Sprachraum"],sent["Deutscher Sprachraum"], equal_var=False,axis=0)
mean_en = np.array(sent["Anglo-Amerikanischer Sprachraum"]).mean()
mean_de = np.array(sent["Deutscher Sprachraum"]).mean()

print("t-statistic value",t)
print("p-value ttest",p/2)
print("mean en:",mean_en,"         mean de:",mean_de)



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


# In[13]:


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
    