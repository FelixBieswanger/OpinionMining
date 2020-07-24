import sys
sys.path.append("./")
from textblob import TextBlob
from statistics import mean
from nltk import tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from resources.database import Database
from resources.preprocessing import *
analyser = SentimentIntensityAnalyzer()

"""
Get Data
"""

db = Database()
source_data = db.get_all(collection="sample")


"""
Method, that calculates different sentiment approaches
"""

def calc_sent(article):

    sentiments = dict()
    raw_text = clean_string(article["text"])
    sentences = get_sentences(raw_text)

    #calc sent without any further weighting
    result_t = 0
    result_v = 0
    for sent in sentences:
        result_t += TextBlob(sent).sentiment.polarity
        result_v += analyser.polarity_scores(sent)["compound"]

    sentiments["textblob"] = result_t/len(sentences)
    sentiments["vader"] = result_v/len(sentences)

    #calc sent with headline weighted stronger

    sent_t = sentiments["textblob"]
    sent_v = sentiments["vader"]

    headline = article["headline"]
    head_t = TextBlob(headline).sentiment.polarity
    head_v = analyser.polarity_scores(headline)["compound"]

    weight = 3
    sentiments["textblob_headline"] = (sent_t + head_t*weight)/(weight+1)
    sentiments["vader_headline"] = (sent_v + head_v*weight)/(weight+1)

    #calc sentiment with stronger weigth of first and last forth of article
    try:
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
            sentences = get_sentences(text[section])
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
        sentiments["textblob_section"] = section_sent/(weight*2+1)

        section_sent = section_result["first"]["v"] * weight + \
            section_result["mid"]["v"] + section_result["first"]["v"] * weight
        sentiments["vader_section"] = section_sent/(weight*2+1)
    except:
        sentiments["textblob_section"] = sentiments["textblob"]
        sentiments["vader_section"] = sentiments["vader"]

    sentiments["textblob_whole"] = TextBlob(raw_text).sentiment.polarity
    sentiments["vader_whole"] = analyser.polarity_scores(raw_text)["compound"]

    return sentiments


"""
Calculate Sentiment for every approach and store value
"""
store = dict()
tools = list(calc_sent(source_data[0]).keys())
tools.append("manual_sentiment")

for tool in tools:
    store[tool] = list()


for doc in source_data:
    result = calc_sent(doc)
    for key in result:
        store[key].append(result[key])

    store["manual_sentiment"].append(doc["manual_sentiment"])


"""
Calculate Mean Absoulte Error
"""

evaluation = dict()

tools = calc_sent(source_data[0]).keys()
for tool in tools:
    evaluation[tool] = [abs(score_m-score_t) for score_t,
                        score_m in zip(store[tool], store["manual_sentiment"])]

for tool in evaluation.keys():
    print(tool, mean(evaluation[tool]))
