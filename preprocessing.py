import re
from nltk import tokenize
from nltk.corpus import stopwords
from spacy import load


def clean_string(string):
    string = string.lower()
    string = re.sub('[^a-zA-Zäüö.ß]', ' ', string)
    return string

def get_sentences(string):
    sents = tokenize.sent_tokenize(string)
    for i in range(len(sents)):
        sents[i] = sents[i].replace(".","")
    return sents


def doc2token(string):
    string = clean_string(string)
    sent = get_sentences(string)
    result = list()
    for s in sent:
        s = s.replace(".","")
        if len(s) < 1:
            continue
        result.append(tokenize.word_tokenize(s))
 
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








        


