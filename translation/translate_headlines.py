from google.cloud import translate_v2
from google.api_core.exceptions import Forbidden,ServiceUnavailable
from database import Database
import preprocessing
import time
from urllib.error import HTTPError
import traceback
import os

"""
The Headlines where forgotton the first time translated
(so here is an extra script, because needed for an sentiment calcualtion approach)
"""

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./resources/google_cloud_api.json"

"""
Get German Articles 
"""
db = Database()
german_articles = db.get_querry(collection="date", querry={"language": "de"})

index = 0
old_index = 0

"""
Translate Headline and store in database
"""

while index<len(german_articles):

    if index != old_index:
        start = time.time()

    old_index = index

    translate_client = translate_v2.Client()
    article = german_articles[index]
    
    raw_text = article["headline"]
    article["headline-de"] = raw_text

    clean_text = preprocessing.clean_string(raw_text)

    try:
        try:
            result = translate_client.translate(clean_text,target_language="en")
        except (Forbidden,ServiceUnavailable):
            print("Wait because of rate limit")
            time.sleep(10)
            continue

        translated_text = result["translatedText"]
        article["headline"] = translated_text
        db.update_article(collection="date", data=article)
        
        print("Translated ", german_articles.index(
                article)+1, "of", len(german_articles))

        index+=1

    except Exception as e:
        traceback.print_exc()
        print("Fail Index",german_articles.index(article))
        break
        
        
