from googletrans import Translator
from database import Database
import preprocessing


db = Database()

german_articles = db.get_querry(collection="article", querry={
    "$or": [{"source": "sueddeutsche"}, {"source": "zeit"}]})

for article in german_articles[530:]:
    if "text-de" not in article:
        trans = Translator(service_urls=["translate.google.com"])
        try:
            #save original text
            article["text-de"] = article["text"]
            clean_text = preprocessing.clean_string(article["text"])

            translated_text = ""
            rest = clean_text
            while len(rest) != 0:
                if len(rest) > 9999:
                    cutoff = rest[:9999].rfind(".")
                    part = rest[:cutoff]
                    rest = rest[cutoff:]
                else:
                    part = rest
                    rest = []
            
                translated_text += trans.translate(part, dest="en").text

            article["text"] = translated_text
            db.update_article(collection="article",data=article)


            print(german_articles.index(article), "of",
                  len(german_articles), "translated")
        except Exception as e:
            print(e.with_traceback())
            print("index", german_articles.index(article))
            break
    else:
        print("Already Translated")




