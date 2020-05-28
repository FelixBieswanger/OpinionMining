import pyLDAvis.gensim
import gensim
from gensim import corpora
import spacy
from database import Database
import preprocessing as pre
import numpy as np

db = Database()
nlp = spacy.load("de_core_news_sm")


data = db.get_querry(collection="article", querry={
                     "$or": [{"source": "NYT"}]})

clean = list()
for doc in data:
    if doc["text"].count("digital") >= 3:
        clean.append(doc)

data = clean

labels = [i["search-term"] for i in data]
text = [i["text"] for i in data]
text = [pre.clean_string(i) for i in text]
sent = [pre.get_sentences(i) for i in text]

text_data = list()
for doc in sent:
    nounsprodoc = list()
    for s in doc:
        nounsprodoc += [token.lemma_ for token in nlp(
            s) if token.pos_ == "NOUN" and len(token) > 3 and token.lemma_ != "Jahr"]
    text_data.append(nounsprodoc)
    print("processed ",sent.index(doc)+1,"of",len(sent))



dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=100)
topics = ldamodel.print_topics(num_words=10)
for topic in topics:
    print(topic)


topics = list()
for doc in text_data:
    topics.append(pre.find_max(ldamodel.get_document_topics(dictionary.doc2bow(doc))))

for topic, label in zip(topics, labels):
    print(topic, label)


lda_display = pyLDAvis.gensim.prepare(
    ldamodel, corpus, dictionary, sort_topics=True)
pyLDAvis.show(lda_display)


    






