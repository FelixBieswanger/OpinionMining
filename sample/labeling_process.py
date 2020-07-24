from database import Database
from random import randint

db = Database()

sample_data = db.get_querry(collection="sample",querry={"manual_sentiment":{"$exists":False}})
sample = sample_data[randint(0,len(sample_data)-1)]
print()
print(len(sample_data),"übrig!")
print("======================")
print("Bitte lesen Sie sich den Artikel genau durch und achte auf die darin vorkommende Stimmlage.")
print("Sie können anschließend den Artikel Bewerten. Die Skala geht von -1 bis 1.")
print("-1 bedeutet, dass hauptsächlich mit einer negativen Tonalität gesprochen wird.")
print("1 visa versa.")
print("=======================")
print("Headline",sample["headline"])
print()
print(sample["text"])

bewertung = input("Bitte gib deine Bewertung ein: ")
try:
    bewertung = float(bewertung)
    sample["manual_sentiment"] = bewertung
    db.update_article(collection="sample",data=sample)
    print("Bewertung erfolgreich gespeicher!")
except:
    print("keine gültige Bewertung abgegegen.")




