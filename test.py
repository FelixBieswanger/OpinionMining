from textblob import TextBlob

blob = TextBlob("I think this was the best movie ever!")


print(blob.sentiment)


score = (blob.sentiment.polarity + blob.sentiment.subjectivity)/2
print(score)
