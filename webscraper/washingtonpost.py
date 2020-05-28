import sys
sys.path.append("./")
from logger import Logger
from database import Database
from bs4 import BeautifulSoup
import requests
import json
import keys
import re
import pandas as pd



cookies = dict()
with open("webscraper/cookie.txt","r") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        line = line.split(";")
        cookies[line[0]]= line[1]

response = requests.get("https://www.washingtonpost.com/health/whats-shopping-in-a-pandemic-like-drive-to-your-local-mall/2020/05/04/f7a94712-8e3f-11ea-9322-a29e75effc93_story.html", cookies=cookies)
soup = BeautifulSoup(response.content,"html.parser")
name = soup.find("span", {"class": "dn dib-ns sign-in-text truncate mr-xxs"})
print(name.text)
