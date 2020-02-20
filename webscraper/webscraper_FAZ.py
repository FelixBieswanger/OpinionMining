from bs4 import BeautifulSoup
import requests as r
from datetime import datetime

#config of base url, which will be used to retrieve articles from FAZ. Specifying search-term, search-range
#and sorting methode
def build_url(i, search_term="digitalisierung", sort="date", search_from="TT.MM.JJJJ", search_to="20.02.2020"):
    return "https://www.faz.net/suche/s"+str(i)+".html?BTyp=redaktionelleInhalte&allboosted=&author=Vorname+Nachname&boostedresultsize=%24boostedresultsize&cid=&from="+search_from+"&index=&query="+search_term+"&resultsPerPage=80&sort=date&to="+search_to+"&username=Benutzername&BTyp=redaktionelleInhalte&chkBoxType_2=on"

#finding how many root pages there are to scrape example for search term digitalisierung: 62 pages
base_url = build_url(1)
root_page = r.get(base_url).content
root_page = BeautifulSoup(root_page,"html.parser")

pagecount = root_page.find("span",{"class":"Seitenzahl"}).text
pagecount = int(pagecount.split(" ")[1])

pagecount = 1

#iterating over all root pages
for i in range(1,pagecount+1):
    url = build_url(i)

    root_page = r.get(base_url).content
    root_page = BeautifulSoup(root_page, "html.parser")

    all_articles = root_page.find("div", {"class": "SuchergebnisListe"})
    all_articles = all_articles.find_all("div", {"class": "Teaser620"})
    
    for article in all_articles:

        #skip those articles, where access has to be bought (maybe added later for scraping)
        fplus = article.find("span", {"class": "fazplusIcon"})
        if fplus:
            continue

        url = article.find("a", {"class": "TeaserHeadLink"})["href"]
        headline = article.find("span", {"class": "Headline"}).text.strip()

        info = article.find("div", {"class": "TeaserInfo"}).text.split()
        info = " ".join(info)
        info = info.split("|")

        date = info[0].strip()+":00"
        date = datetime.strptime(date,"%d.%m.%y %H:%M:%S")
        category = info[1].strip()

       

    

    


    
    


