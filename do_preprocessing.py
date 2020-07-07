from database import Database
import preprocessing

db = Database()

def do_preprocessing_lda():
    data = db.get_all(collection="date")
    texts = [art["text"] for art in data]

    count = 0
    for art, pre_processedtext in zip(data,preprocessing.preprocessing_lda(texts)):
        art["lda"] = pre_processedtext
        db.update_article(collection="date",data=art)
        count += 1
        print(count,"/",len(texts))


do_preprocessing_lda()
    