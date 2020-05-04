import sys
sys.path.append(
    "/Users/felixbieswanger/Desktop/Uni_Stuff/Bachelorarbeit/OpionionMining")
from database import Database
from bs4 import BeautifulSoup
import requests as r
from useragent import get_random_useraget
from datetime import datetime
from logger import Logger

# defining search-word
search_term = "Fußball"

logger = Logger(site="FAZ",search_term=search_term).getLogger()

# initializing database class and passing logger
db = Database(logger)

# config of base url, which will be used to retrieve articles from FAZ. Specifying search-term, search-range
# and sorting methode


def build_url(i, search_term=search_term, sort="date", search_from="TT.MM.JJJJ", search_to=datetime.now().strftime("%d.%m.%Y")):
    return "https://www.faz.net/suche/s"+str(i)+".html?BTyp=redaktionelleInhalte&allboosted=&author=Vorname+Nachname&boostedresultsize=%24boostedresultsize&cid=&from="+search_from+"&index=&query="+search_term+"&resultsPerPage=80&sort=date&to="+search_to+"&username=Benutzername&BTyp=redaktionelleInhalte&chkBoxType_2=on"


# defining standard methode for scaping content on webpage
def scrape_content(article, name, html_tag, attribute_type, value):
    result = None
    try:
        result = article.find(html_tag, {attribute_type: value}).text.strip()
    except:
        logger.warning(name+" could not be scraped")
    return result


# finding how many root pages there are to scrape example for search term digitalisierung: 62 pages
url = build_url(1, search_term=search_term)
root_page = r.get(url, headers={"User-Agent": get_random_useraget()}).content
root_page = BeautifulSoup(root_page, "html.parser")

pagecount = root_page.find("span", {"class": "Seitenzahl"}).text
pagecount = int(pagecount.split(" ")[1])

#stop if no new articles are found
stop_counter = 0


# iterating over all root pages
for i in range(1, pagecount):
    logger.info("Start scrape of base page "+str(i))
    base_url = build_url(i, search_term=search_term)
    logger.info("Scrape URL"+base_url)
    root_page = r.get(base_url, headers={
                      "User-Agent": get_random_useraget()}).content
    root_page = BeautifulSoup(root_page, "html.parser")

    all_articles = root_page.find("div", {"class": "SuchergebnisListe"})
    all_articles = root_page.find_all("div",{"class":"Teaser620"})
    logger.info(str(len(all_articles))+" found on page")

    if len(all_articles) == 0:
        logger.critical("!!!!! Scrape Stopped because resources were exeeded !!!!!!")
        exit()

    for article in all_articles:
        """
        if stop_counter == 15:
            logger.critical("!!!!! Scrape Stopped because no new articles were found !!!!!!")
            exit()
        """

        # skip those articles, where access has to be bought (maybe added later for scraping)
        if article.find("span", {"class": "fazplusIcon"}) or article.find("div", {"class": "First"}):
            continue

        headline = scrape_content(article=article,name="headline", html_tag="span", attribute_type="class", value="Headline")
        info = scrape_content(article=article, name="info", html_tag="div",
                              attribute_type="class", value=["TeaserInfo"])
        author = scrape_content(article=article, name="autor",
                                html_tag="span", attribute_type="class", value="Autor")

        if not author:
            author = "dpa"

        if info:
            info = " ".join(info)
            info = info.split("|")
            category = info[1].strip()
            category = category.replace(" ", "")
            date = info[0].strip()+":00"
            date = date.replace(" ", "")
            try:
                date = datetime.strptime(date, "%d.%m.%y%H:%M:%S")
            except:
                logger.warning("Date could not be created. Source Date: "+date)
                date = None
        else:
            category = None
            date = None
            logger.info("Headline: "+headline)

        try:
            link = article.find("div", {"class": "MediaLink"})
            link = link.find("a")["href"]
            article_url = "https://faz.net"+link
            logger.info("Start scrape of article "+article_url)

            page = r.get(article_url, headers={
                "User-Agent": get_random_useraget()}).content
            art_page = BeautifulSoup(page, "html.parser")
        except:
            page = None
            logger.critical(
                "Article Page could not be loaded and therefore could not be scraped")

        if page:
            try:
                text = art_page.find(
                    "p", {"class": "atc-IntroText"}).text.strip()

                paragraphs = art_page.find_all(
                    "p", {"class": "atc-TextParagraph"})
                for p in paragraphs:
                    text += p.text.strip()
            except:
                text = None
                logger.critical("Article text could not be scraped")

            data = {
                "search-term": search_term,
                "source": "FAZ",
                "base_url": base_url,
                "article_url": article_url,
                "headline": headline,
                "date": date,
                "author": author,
                "category": category,
                "text": text
            }

            if db.insert_data(data=data, collection="article") == "already":
                stop_counter+=1
