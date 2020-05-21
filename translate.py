from google.cloud import translate
from google.api_core.exceptions import Forbidden
from database import Database
import preprocessing
import time
from urllib.error import HTTPError
import traceback

db = Database()


german_articles = db.get_querry(collection="article", querry={
    "$or": [{"source": "sueddeutsche"}, {"source": "zeit"}]})

index = 112
old_index = 0

while index<len(german_articles):

    if index != old_index:
        start = time.time()

    old_index = index

    translate_client = translate.TranslationServiceClient()
    article = german_articles[index]

    

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
        try:
            result = translate_client.translate_text()
        except Forbidden:
            print("Wait because of rate limit")
            time.sleep(10)
            continue

        translated_text = result["translatedText"]
        article["text"] = translated_text
        db.update_article(collection="article", data=article)
        end = time.time()
        #sec
        duration = end - start
    
        remaining_time = (len(german_articles)-german_articles.index(article))*duration
        #min
        remaining_time = int(remaining_time/60)

        print("Translated ", german_articles.index(
                article)+1, "of", len(german_articles), "| est. remaining duration", remaining_time, "min")

        index+=1

    except Exception as e:
        traceback.print_exc()
        print("Fail Index",german_articles.index(article))
        break
    
     
