
import sys
sys.path.append("./")
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import cookie_maker
import keys
import time
import requests
from bs4 import BeautifulSoup
from database import Database
from logger import Logger
from useragent import get_random_useraget
from datetime import datetime


search_terms =["digitalisation"]#,"digitisation","digital+transformation"]

for search_term in search_terms:
    
    logger = Logger(site="financialtimes", search_term=search_term).getLogger()
    db = Database(logger)

    cookies = keys.get_key("ft-cookies")

    header = {
        "Cookie": cookie_maker.create_cookie_string(cookies)
    }

    for i in range(1,26):
        response = requests.get(
            "https://www.ft.com/search?q="+search_term+"&page="+str(i)+"&sort=date", headers=header)

        base = BeautifulSoup(response.content,"html.parser")
        articles = base.find_all("li", {"class": "search-results__list-item"})

        for article in articles:
            try:
                if article.find("span", {"class": "o-labels o-labels--premium o-labels--content-premium"}) is None:
                    store = {}
                    store["source"] = "financialtimes"
                    store["search-term"] = search_term

                    headline = article.find("a", {"class": "js-teaser-heading-link"})
                    store["headline"] = headline.text
                    store["article_url"] = "https://www.ft.com"+headline["href"]

                    page = BeautifulSoup(requests.get(store["article_url"],headers=header).content,"html.parser")


                    store["section"] = page.find("div",{"class":"topper__primary-theme"}).find("a").text
                    date_str = page.find("time", {"class": "article-info__timestamp o-date"})["datetime"]
                    datetime = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                    store["date"] = datetime

                    paragraph_container = page.find("div",{"class":"article__content-body n-content-body js-article__content-body"})
                    text = ""
                    for p in paragraph_container.find_all("p"):
                        text += p.text.strip()

                    store["text"] = text

                    db.insert_data(collection="article", data=store)

            except Exception as e:
                logger.warning(e)
                logger.warning(str(i))


        time.sleep(3)


