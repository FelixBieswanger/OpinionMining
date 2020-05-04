from database import Database
import preprocessing
from textblob_de import TextBlobDE


print("Add Sentiment manually to Sentence:")
print("2 = Really Positive")
print("1 = Positive")
print("0 = Neutral")
print("-1 = Negative")
print("-2 = Really Negative")


db = Database()
doc = db.getNewDoc()
text = doc["text"]
id = doc["_id"]


sents = preprocessing.get_sentences(text)

for sent in sents:
    sent = sent.strip()
    print('"',sent,'"')
    data = {
        "doc_id": id,
        "text": sent
    }
    data["sentiment_human"]=input("Add Sentiment Value ")
    data["sentiment_textblib"] = TextBlobDE(sent).sentiment
    print(data)

