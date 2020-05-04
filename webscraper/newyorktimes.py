import sys
sys.path.append("./")
from logger import Logger
import requests as r
import json
import keys
from bs4 import BeautifulSoup
from database import Database


search_term = "digitization"
logger = Logger(site="NYT", search_term=search_term).getLogger()
db = Database(logger)
key = keys.get_key("newyorktimes")

response = r.get(
    "https://api.nytimes.com/svc/search/v2/articlesearch.json?q="+search_term+"&sort=newest&page=1&api-key="+key).content

result = json.loads(response)["response"]
hits = result["meta"]["hits"]
pages = int(hits/10)


for i in range(pages):
    response = r.get(
        "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=digitization&sort=newest&page="+str(i)+"&api-key="+key).content
    result = json.loads(response)["response"]

    for doc in result["docs"]:
        try:
            store = dict()

            url = doc["web_url"]
            store["article_url"] = url
            store["date"] = doc["pub_date"]
            store["doc_type"] = doc["document_type"]
            store["section"] = doc["section_name"]
            store["wordcount"] = doc["word_count"]

            article = BeautifulSoup(r.get(url).content, "html.parser")
            section = article.find("section", {"class": "meteredContent"})
            parts = section.find_all("div", {"class": "StoryBodyCompanionColumn"})

            text = ""
            for part in parts:
                text += part.text
            store["text"] = text
        except Exception as e:
            logger.warning(e)
            pass
        
        db.insert_data(collection="article", data=store)

        
