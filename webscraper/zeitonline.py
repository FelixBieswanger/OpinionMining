import sys
sys.path.append("./")
import keys
import requests
from bs4 import BeautifulSoup
from database import Database
from logger import Logger

search_term = "digitale+transformation"
logger = Logger(site="zeit", search_term=search_term).getLogger()
db = Database(logger)


# Fill in your details here to be posted to the login form.
user = keys.get_key("zeituser")
pw = keys.get_key("zeitpw")

for i in range(277):
    payload = {
        'email': user,
        'pass': pw,
        "return_url": "https://www.zeit.de/suche/index?q="+search_term+"&sort=aktuell&p="+str(i)
    }
    # create Session to login and send login information with every further request
    with requests.Session() as s:
        p = s.post('https://meine.zeit.de/anmelden', data=payload)

        # Check if login worked
        soup = BeautifulSoup(p.content, "html.parser")
        name = soup.find("span", {"class": "nav__user-name"}).text

        articles = soup.findAll("article", {"class": "zon-teaser-standard"})

        for article in articles:
            try:
                url = article.find(
                    "a", {"class", "zon-teaser-standard__combined-link"})["href"]

                page = BeautifulSoup(s.get(url).content, "html.parser")

                store = dict()
                store["headline"] = page.find(
                    "span", {"class": "article-heading__title"}).text
                store["section"] = page.find(
                    "span", {"class": "article-heading__kicker"}).text
                store["date"] = page.find("time", {"class": "metadata__date"})["datetime"]
                store["article_url"] = url
                store["search-term"] = search_term
                store["source"] = "zeit"

                text = ""
                for paragraph in page.find_all("p", {"class": "paragraph article__item"}):
                    text += paragraph.text
                store["text"] = text
                
                if text != "":
                    db.insert_data(collection="article",data=store)
            except Exception as e:
                logger.warning(e)
                pass
