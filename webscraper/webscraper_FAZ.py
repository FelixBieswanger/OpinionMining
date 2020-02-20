import sys
sys.path.append(
    "/Users/felixbieswanger/Desktop/Uni_Stuff/Bachelorarbeit/OpionionMining")

from bs4 import BeautifulSoup
import requests as r
from useragent import get_random_useraget
from datetime import datetime
import database as db



key_word="Digitalisierung"

#config of base url, which will be used to retrieve articles from FAZ. Specifying search-term, search-range
#and sorting methode
def build_url(i, search_term="digitalisierung", sort="date", search_from="TT.MM.JJJJ", search_to="20.02.2020"):
    return "https://www.faz.net/suche/s"+str(i)+".html?BTyp=redaktionelleInhalte&allboosted=&author=Vorname+Nachname&boostedresultsize=%24boostedresultsize&cid=&from="+search_from+"&index=&query="+search_term+"&resultsPerPage=80&sort=date&to="+search_to+"&username=Benutzername&BTyp=redaktionelleInhalte&chkBoxType_2=on"

#finding how many root pages there are to scrape example for search term digitalisierung: 62 pages
url = build_url(1,search_term=key_word)
root_page = r.get(url, headers={"User-Agent": get_random_useraget()}).content
root_page = BeautifulSoup(root_page,"html.parser")

pagecount = root_page.find("span",{"class":"Seitenzahl"}).text
pagecount = int(pagecount.split(" ")[1])

pagecount = 1

#iterating over all root pages
for i in range(1,pagecount+1):
    base_url = build_url(i,search_term=key_word)

    root_page = r.get(base_url,headers={"User-Agent":get_random_useraget()}).content
    root_page = BeautifulSoup(root_page, "html.parser")

    all_articles = root_page.find("div", {"class": "SuchergebnisListe"})
    all_articles = all_articles.find_all("div", {"class": "Teaser620"})
    
    for article in all_articles[0:1]:

        #skip those articles, where access has to be bought (maybe added later for scraping)
        fplus = article.find("span", {"class": "fazplusIcon"})
        if fplus:
            continue

        article_url = "https://faz.net"+article.find("a", {"class": "TeaserHeadLink"})["href"]
        headline = article.find("span", {"class": "Headline"}).text.strip()

        info = article.find("div", {"class": "TeaserInfo"}).text.split()
        info = " ".join(info)
        info = info.split("|")

        date = info[0].strip()+":00"
        date = datetime.strptime(date,"%d.%m.%y %H:%M:%S")
        category = info[1].strip()

        page = r.get(article_url, headers={
                     "User-Agent": get_random_useraget()}).content
        art_page = BeautifulSoup(page,"html.parser")

        author = art_page.find("a", {"class": "atc-MetaAuthorLink"}).text.strip()
        location = art_page.find_all("span", {"class": "atc-MetaAuthor"})[1].text.strip()

        text = art_page.find("p", {"class": "atc-IntroText"}).text.strip()

        paragraphs = art_page.find_all("p", {"class": "atc-TextParagraph"})
        for p in paragraphs:
            text += p.text.strip()


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

        



            



       

    

    


    
    


