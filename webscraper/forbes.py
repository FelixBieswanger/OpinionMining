import sys
sys.path.append("./")
from datetime import datetime
from useragent import get_random_useraget
from logger import Logger
from database import Database
from bs4 import BeautifulSoup
import requests
import keys
from datetime import datetime

search_term = "digitalization"
logger = Logger(site="forbes", search_term=search_term).getLogger()
db = Database(logger)


cookies = {
    "notice_preferences": "2:1a8b5228dd7ff0717196863a5d28ce6c",
    "notice_gdpr_prefs": "0,1,2:1a8b5228dd7ff0717196863a5d28ce6c"
}

cookie_string = ""
for name in cookies.keys():
    cookie_string+=name
    cookie_string+="="
    cookie_string+=cookies[name]
    cookie_string+=";"

cookie_string = cookie_string[:-2]
header = {
    "Cookie": cookie_string
}



for i in range(0,10000,20):

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
            pass
