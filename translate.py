from google.cloud import translate_v2
from google.api_core.exceptions import Forbidden,ServiceUnavailable
from database import Database
import preprocessing
import time
from urllib.error import HTTPError
import traceback
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./resources/opinionmininghdm-f5403fd25fa4.json"

db = Database()


german_articles = db.get_querry(collection="article", querry={
    "$or": [{"source": "sueddeutsche"}, {"source": "zeit"}]})

index = 755
old_index = 0

while index<len(german_articles):

    if index != old_index:
        start = time.time()

    old_index = index

    translate_client = translate_v2.Client()
    article = german_articles[index]

    if "text-de" not in article:
       
        raw_text = article["text"]
        article["text-de"] = raw_text

        clean_text = preprocessing.clean_string(raw_text)

        try:
            try:
                result = translate_client.translate(clean_text,target_language="en")
            except (Forbidden,ServiceUnavailable):
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
    else:
        index+=1
        print("already translated")
        
        
