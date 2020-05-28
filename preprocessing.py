import re
from nltk import tokenize
from nltk.corpus import stopwords
import spacy


def clean_string(string):
    string = re.sub('[^a-zA-Zäüöß.,]', ' ', string)
    string = string.strip()
    string = re.sub('[  ]+', ' ', string)
    return string

def get_sentences(string):
    sents = tokenize.sent_tokenize(string)
    for i in range(len(sents)):
        sents[i] = sents[i].replace(".","")
    return sents

def get_lemma(docs):
    nlp = spacy.load("de_core_news_sm")

    result = list()
    for doc in docs:
        temp = ""
        for token in nlp(doc):
            temp += token.lemma_ + " "
        result.append(temp)
        print("processed",docs.index(doc),"of",len(docs))
    return result


def remove_stopwords(tokens,lang="german"):
    all_tokens= tokens

    result = list()
    for sent in all_tokens:
        sent_result = list()
        for token in sent:
            if token not in stopwords.words(lang):
                sent_result.append(token)
        result.append(sent_result)

    return result

def pos_tag(text):
    nlp = load('de_core_news_md')
    result = list()
    for sent in text:
        doc= nlp(sent)
        asent = list()
        for token in doc:
            if token.pos_ == "NOUN":
                asent.append(token.text)
        result.append(asent)
    return result

def find_max(results):
    max = 0
    topic = 0
    for tupl in results:
        if tupl[1] > max:
            max = tupl[1]
            topic = tupl[0]

    return topic










        


