from database import Database
import preprocessing

db = Database()

date_articles = db.get_all(collection="date")
article_texts = [art["text"] for art in date_articles]

preprocessed_text = preprocessing.preprocessing_doc2vec(article_texts)


for art in date_articles:
    art["noun_lemma"] = preprocessed_text[date_articles.index(art)]
    db.update_article(collection="date",data=art)
    print(date_articles.index(art),"/",len(date_articles))

