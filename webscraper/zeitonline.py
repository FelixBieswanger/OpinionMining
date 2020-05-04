import requests
from bs4 import BeautifulSoup as BS

# Fill in your details here to be posted to the login form.
payload = {
    'email': 'accounts@philliprundel.net',
    'pass': 'safhaq-rosri3-cyVwib',
    "return_url":"https://www.zeit.de/suche/index?q=Digitalisierung&sort=aktuell&p=1"
}

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    p = s.post('https://meine.zeit.de/anmelden',data=payload)
    # print the html returned or something more intelligent to see if it's a successful login page.
    soup = BS(p.content,"html.parser")
    name = soup.find("span", {"class": "nav__user-name"}).text
    print("Logged in",name)

    articles = soup.findAll("article", {"class":"zon-teaser-standard"})
    print(len(articles))
    for article in articles:
        head = article.find("span", {"class", "zon-teaser-standard__title"}).text
        print(head)
