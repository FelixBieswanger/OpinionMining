import re
from nltk import tokenize
from nltk.corpus import stopwords
from spacy import load


def clean_string(string):
    string = string.lower()
    string = re.sub(r'\d+', " ", string)
    string = string.replace("–", "")
    string = string.replace(":", "")
    string = string.replace("'", "")
    string = string.replace(",", "")
    return string

def get_sentences(string):
    return tokenize.sent_tokenize(string)


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
    string = clean_string(text)
    sent = get_sentences(string)
    nlp = load('de_core_news_md')
    result = list()
    for s in sent:
        doc= nlp(s)
        asent = list()
        for token in doc:
            d=dict()
            d["word"] = token.text
            d["pos"] = token.pos_
            asent.append(d)
        result.append(asent)
    return result








        


