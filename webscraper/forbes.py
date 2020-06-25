import sys
sys.path.append("./")
from datetime import datetime
from useragent import get_random_useraget
from logger import Logger
from database import Database
from bs4 import BeautifulSoup
import requests
import time
import keys
import cookie_maker

search_terms = ["digital+transformation","digitization"]
cookies = keys.get_key("forbes-cookies")
header = {
    "Cookie": cookie_maker.create_cookie_string(cookies)
}


for search_term in search_terms:
    logger = Logger(site="forbes", search_term=search_term).getLogger()
    db = Database(logger)


    for i in range(900,10000,20):

        response = requests.get("https://www.forbes.com/simple-data/search/more/?start="+str(i)+"&q="+search_term, headers=header)
        base = BeautifulSoup(response.content,"html.parser")
        articles = base.find_all("article")

        for article in articles:
            try:

                store = dict()

                store["search-term"]=search_term
                store["source"] = "forbes"
                store["date"] = datetime.fromtimestamp(int(article["data-date"])/1000)
                head_link = article.find("a", {"class": "stream-item__title"})
                link = head_link["href"]
                store["headline"] = head_link.text.strip()
                store["article_url"] = link

                page = BeautifulSoup(requests.get(link, headers=header).content,"html.parser")

                text = ""
                for p in page.find("div", {"class": "article-body"}).find_all("p", recursive=False):
                    text+=p.text

                store["text"] = text
                
                db.insert_data(collection="article", data=store)

            except Exception as e:
                logger.warning(e)
                logger.warning(str(i))
                pass

        time.sleep(3)
