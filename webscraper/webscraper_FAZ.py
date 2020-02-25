import sys
sys.path.append(
    "/Users/felixbieswanger/Desktop/Uni_Stuff/Bachelorarbeit/OpionionMining")

import logging as logger
from database import Database
from datetime import datetime
from useragent import get_random_useraget
import requests as r
from bs4 import BeautifulSoup

# defining search-word
key_word = "Digitale+Transformation"

# setting date to starttime of script
now = datetime.now()
string_time = now.strftime("%d%m%y_%H%M%S")
# setup logger
logger.basicConfig(filename=("./logs/webscrape_FAZ_"+string_time+".log"), level=logger.INFO,
                   format="%(levelname)s;%(asctime)s;%(filename)s;%(lineno)s;%(message)s")
logger.getLogger("requests").setLevel(logger.NOTSET)

# initializing database class and passing logger
db = Database(logger)

# config of base url, which will be used to retrieve articles from FAZ. Specifying search-term, search-range
# and sorting methode


def build_url(i, search_term="digitalisierung", sort="date", search_from="TT.MM.JJJJ", search_to="20.02.2020"):
    return "https://www.faz.net/suche/s"+str(i)+".html?BTyp=redaktionelleInhalte&allboosted=&author=Vorname+Nachname&boostedresultsize=%24boostedresultsize&cid=&from="+search_from+"&index=&query="+search_term+"&resultsPerPage=80&sort=date&to="+search_to+"&username=Benutzername&BTyp=redaktionelleInhalte&chkBoxType_2=on"


#defining standard methode for scaping content on webpage
def scrape_content(name, html_tag, attribute_type, value):
    result = None
    try:
        result = article.find(html_tag, {attribute_type: value}).text.strip()
    except:
        logger.warning(name+" could not be scraped")
    return result


# finding how many root pages there are to scrape example for search term digitalisierung: 62 pages
url = build_url(1, search_term=key_word)
root_page = r.get(url, headers={"User-Agent": get_random_useraget()}).content
root_page = BeautifulSoup(root_page, "html.parser")

pagecount = root_page.find("span", {"class": "Seitenzahl"}).text
pagecount = int(pagecount.split(" ")[1])

frompage = 1
topage = 4

if topage > pagecount:
    print("To many pages were specifyed.",pagecount,"is the maximum.")
    exit()

# iterating over all root pages
for i in range(frompage, topage+1):
    logger.info("Start scrape of base page "+str(i)+"/"+str(topage))
    logger.info("=====================================")
    base_url = build_url(i, search_term=key_word)
    root_page = r.get(base_url, headers={
                      "User-Agent": get_random_useraget()}).content
    root_page = BeautifulSoup(root_page, "html.parser")

    all_articles = root_page.find("div", {"class": "SuchergebnisListe"})
    all_articles = all_articles.find_all("div", {"class": "Teaser620"})

    for article in all_articles:

        # skip those articles, where access has to be bought (maybe added later for scraping)
        fplus = article.find("span", {"class": "fazplusIcon"})
        if fplus:
            continue

        link = article.find("div", {"class": "MediaLink"})
        link = link.find("a")["href"]
        article_url = "https://faz.net"+link
        logger.info("Start scrape of article "+article_url)

        headline = scrape_content(
            "headline", html_tag="span", attribute_type="class", value="Headline")
        info = scrape_content("info", "div", "class", ["TeaserInfo"])
        if info:
            info = " ".join(info)
            info = info.split("|")
            category = info[1].strip()
            category = category.replace(" ","")
            date = info[0].strip()+":00"
            date = date.replace(" ","")
            try:
                date = datetime.strptime(date, "%d.%m.%y%H:%M:%S")
            except:
                logger.warning("Date could not be created. Source Date: "+date)
                date = None
        else:
            category = None
            date = None

        try:
            page = r.get(article_url, headers={
                        "User-Agent": get_random_useraget()}).content
            art_page = BeautifulSoup(page, "html.parser")
        except:
            page = None
            logger.critical(
                "Article Page could not be loaded and therefore could not be scraped")

        if page:
            try:
                author = art_page.find_all(
                    "span", {"class": "atc-MetaAuthor"})[0].text.strip()
                location = art_page.find_all(
                    "span", {"class": "atc-MetaAuthor"})[1].text.strip()
            except:
                author = None
                location = None
                logger.warning("Author & Location could not be scraped")

            if not author:
                author_span = art_page.find(
                    "span", {"class", "atc-MetaAuthor"})
                author = author_span.find("a").text

            if not author:
                author = scrape_content(
                    "Author_Qulle", "span", "class", "atc-Footer_Quelle")

            try:
                text = art_page.find("p", {"class": "atc-IntroText"}).text.strip()

                paragraphs = art_page.find_all("p", {"class": "atc-TextParagraph"})
                for p in paragraphs:
                    text += p.text.strip()
            except:
                text=None
                logger.critical("Article text could not be scraped")


            data = {
                 "key-word":key_word, 
                 "source":"FAZ", 
                 "base_url":base_url, 
                 "article_url":article_url,
                 "headline":headline,
                 "date":date,
                 "author":author,
                 "category":category,
                 "text":text 
                }

            db.insert_article(data)

        



            



       

    

    


    
    


