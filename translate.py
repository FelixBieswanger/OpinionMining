from googletrans import Translator
from database import Database
import preprocessing


db = Database()
trans = Translator(service_urls=["translate.google.com"])

german_articles = db.get_querry(collection="article", querry={
    "$or": [{"source": "sueddeutsche"}, {"source": "zeit"}]})

for article in german_articles:
    if "text-de" not in article:
        #save original text
        article["text-de"] = article["text"]

        clean_text = preprocessing.clean_string(article["text"])
        trans_text = trans.translate(clean_text,dest="en").text

        article["text"] = trans_text
        
        db.update_article(collection="article",data=article)

    print(german_articles.index(article),"of",len(german_articles),"translated")


