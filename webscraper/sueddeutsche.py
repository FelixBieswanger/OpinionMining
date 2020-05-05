import sys
sys.path.append("./")
from logger import Logger
from database import Database
from bs4 import BeautifulSoup
import requests
import keys


search_term = "Digitalisierung"
logger = Logger(site="sueddeutsche", search_term=search_term).getLogger()
db = Database(logger)


for i in range(1,101):
    response = requests.get(
        "https://www.sueddeutsche.de/news/page/"+str(i)+"?search="+search_term+"&sort=date&type=article")

    main = BeautifulSoup(response.content,"html.parser")
    articles = main.find_all("div", {"class": "entrylist__entry"})
    
    for article in articles:
        try:
            store = dict()
            url = article.find("a", {"class": "entrylist__link"})["href"]
            page = BeautifulSoup(requests.get(url).content,"html.parser")
            store["article_url"] = url
            store["headline"] = page.find("span", {"class": "css-1kuo4az"}).text
            store["date"] = page.find("time", {"class": "css-11lvjqt"})["datetime"]
            store["source"] = "sueddeutsche"
            store["search-term"] = search_term
            text = ""
            for paragraph in page.find_all("p", {"class": "css-0"}):
                text += paragraph.text
            store["text"] = text
 
            if text != "":
                db.insert_data(collection="artilce",data=store)
            
        except Exception as e:
            logger.warning(e)
            pass
