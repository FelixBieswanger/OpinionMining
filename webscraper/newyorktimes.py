import sys
sys.path.append("./")
from logger import Logger
import requests as r
import json
import keys
from bs4 import BeautifulSoup
from database import Database
import time
from useragent import get_random_useraget

search_term = "digitalization"
logger = Logger(site="NYT", search_term=search_term).getLogger()
db = Database(logger)
key = keys.get_key("newyorktimes")

response = r.get(
    "https://api.nytimes.com/svc/search/v2/articlesearch.json?q="+search_term+"&sort=newest&page=1&api-key="+key).content


result = json.loads(response)["response"]

hits = result["meta"]["hits"]
pages = int(hits/10)


for i in range(1,pages):
    response = r.get(
        "https://api.nytimes.com/svc/search/v2/articlesearch.json?q="+search_term+"&sort=newest&page="+str(i)+"&api-key="+key).content
    try:
        result = json.loads(response)["response"]
    except Exception as e:
        logger.warning(e)
        pass

    for doc in result["docs"]:
        try:
            store = dict()

            url = doc["web_url"]
            store["article_url"] = url
            store["date"] = doc["pub_date"]
            store["doc_type"] = doc["document_type"]
            store["section"] = doc["section_name"]
            store["wordcount"] = doc["word_count"]
            store["headline"] = doc["headline"]
            store["search-term"] = search_term
            store["source"] = "NYT"

            article = BeautifulSoup(
                r.get(url, headers={"User-Agent": get_random_useraget()}).content, "html.parser")
            section = article.find("section", {"class": "meteredContent"})
            parts = section.find_all("div", {"class": "StoryBodyCompanionColumn"})

            text = ""
            for part in parts:
                text += part.text
            store["text"] = text

            db.insert_data(collection="article", data=store)
        except Exception as e:
            logger.warning(e)
            pass
        
    time.sleep(3)


