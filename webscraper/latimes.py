import sys
sys.path.append("./")
import keys
import requests
from bs4 import BeautifulSoup
from database import Database
from logger import Logger
from useragent import get_random_useraget
from datetime import datetime

search_term = "digitalization+digital"
logger = Logger(site="latimes", search_term=search_term).getLogger()
db = Database(logger)


for i in range(500):
    base_page = requests.get(
        "https://www.latimes.com/search?q="+search_term+"&s=0&p="+str(i), headers=get_random_useraget())
    base_soup = BeautifulSoup(base_page.content,"html.parser")

    articles = base_soup.find_all(
        "li", {"class": "SearchResultsModule-results-item"})

    for article in articles:
        try:
            media = article.find("div", {"class": "PromoMedium-title"})
            link = media.find("a")["href"]

            store = dict()
            store["source"] = "latimes"
            store["article_url"] = link
            store["search-term"] = search_term

            response = requests.get(link, headers=get_random_useraget())
            page = BeautifulSoup(response.content,"html.parser")

            store["headline"] = page.find("h1", {"class": "ArticlePage-headline"}).text.strip()
            store["section"] = page.find(
                "div", {"class": "ArticlePage-breadcrumbs"}).find("a").text
            day = page.find("div", {"class":"ArticlePage-datePublished-day"}).text
            day = day.replace(".","")
            day = day.replace(",", "")

            try:
                store["date"] = datetime.strptime(day, "%b %d %Y")
            except Exception as e:
                store["date"] = datetime.strptime(day, "%B %d %Y")
            except Exception as e:
                logger.warning("Date could not be converted, stored as string")
                store["date"] = day

            container = page.find("div", {"class": "RichTextArticleBody"})

            text = ""
            for p in container.find_all("p"):
                text += p.text.strip()
            
            store["text"] = text

            db.insert_data(collection="article", data=store)
        except Exception as e:
            logger.warning(e)
            pass
        
