import gensim
from gensim import corpora
from gensim.models import Word2Vec
import preprocessing as pre
from database import Database
import spacy

db = Database()

articles = db.get_all()

nlp = spacy.load("de_core_news_md")
doc1 = nlp(articles[0]["text"])
doc2 = nlp(articles[1]["text"])
doc3 = nlp(articles[2]["text"])

print(articles[0]["headline"],articles[1]["headline"])
print(doc1.similarity(doc2))












