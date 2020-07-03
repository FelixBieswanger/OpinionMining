import re
from nltk import tokenize
from nltk.corpus import stopwords
import spacy


def clean_string(string):
    #keep ! because a lot of meaning in sentiment 
    string = re.sub("[^a-zA-Z.!,[^']]", ' ', string)
    string = string.replace('“', "")
    string = string.replace('”', "")
    string = string.replace('"', "")
    string = string.strip()
    string = re.sub('[  ]+', ' ', string)
    string = string.lower()
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


def remove_stopwords_sent(texts):
    print("loading model..")
    nlp = spacy.load("en_core_web_md")
    print("model loaded!")

    result = list()
    #pipe = list(nlp.pipe(texts, disable=["parser", "ner", "textcat"]))
    for doc in texts:
        processed = nlp(doc)
        result.append([str(token).lower() for token in processed if token.pos_ == "NOUN" and len(token) > 1])
        print("processed", pipe.index(doc), "of", len(texts))
    return result

def preprocessing_doc2vec(list_of_texts):
    print("loading model..")
    nlp = spacy.load("en_core_web_md")
    print("model loaded!")

    result = list()
    #pipe = list(nlp.pipe(texts, disable=["parser", "ner", "textcat"]))
    for doc in list_of_texts:
        processed = nlp(doc)
        processed = [str(token).lower() for token in processed if token.pos_ in ["NOUN", "ADJ"] and len(token) > 1]
        joined = " ".join(processed)
        result.append(joined)
        print("processed", list_of_texts.index(doc), "of", len(list_of_texts))
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


def preprocessing_lda(texts):
    result = list()
    for text in texts:
        text = text.replace("digital transformation", "digital_transformation")
        tokens = text.split(" ")
        tokens = [token for token in tokens if len(token) > 2 and token not in ["p.m.", "a.m", "p.m", "a.m."]]
        result.append(tokens)
    return result










        


