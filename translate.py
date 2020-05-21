from google.cloud import translate_v2
from database import Database
import preprocessing

db = Database()
translate_client = translate_v2.Client()

german_articles = db.get_querry(collection="article", querry={
    "$or": [{"source": "sueddeutsche"}, {"source": "zeit"}]})

for article in german_articles[:10]:
    if "text-de" in article:
        #case falls bereits übersetzt wurde
        raw_text = article["text-de"]
    else:
        #case falls noch nicht übersetzt wurde
        #orginaltext in text-de abspeichern
        raw_text = article["text"]
        article["text-de"] = raw_text

    clean_text = preprocessing.clean_string(raw_text)

    try:
        result = translate_client.translate(clean_text, target_language="en")
        translated_text = result["translatedText"]
        article["text"] = translated_text
        db.update_article(collection="article", data=article)

        print("Translated ", german_articles.index(article)+1,"of",len(german_articles))
    except Exception as e:
        print(e.with_traceback())
        print("Fail Index",german_articles.index(article))
        break

    print(article)
    print()
    print()
    print()
    print()
    
     
