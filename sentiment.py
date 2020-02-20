import gensim
from gensim import corpora
from gensim.models import Word2Vec
import preprocessing as pre

text=""
with open("data/article1.txt","r") as file:
    text = file.readline()

pos = pre.pos_tag(text)

tokens=list()
for sent in pos:
    s=list()
    for tup in sent:
        if tup["pos"] == "NOUN":
            s.append(tup["word"])
    tokens.append(s)
    
dictionary = corpora.Dictionary(tokens)
corpus = [dictionary.doc2bow(text) for text in tokens]

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=1, id2word=dictionary, passes=20)
topics = ldamodel.print_topics(num_words=2)
for topic in topics:
    print(topic)












