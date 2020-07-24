import sys
sys.path.append("./")

from resources.database import Database

db = Database

source_data = db.get_all(collection="date")

text = [i["lda"] for i in source_data]
text_data = [t.split(" ") for t in text]
dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]
ldamodel = gensim.models.ldamodel.LdaModel.load("./data_selection/lda_models/lda_t22_07072020_103348.model")


def color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    return "hsl(0, 100%, 0%)"


with open("topics.txt","a") as file:
    for topic in ldamodel.print_topics(22, 15):
        file.append("=======")
        file.append("TOPIC", topic[0])
        file.append(topic[1])
        split = topic[1].split("+")
        d = dict()
        for el in split:
            split2 = el.split("*")
            weight = float(split2[0])
            word = split2[1].replace('"', '')
            d[word] = weight
        wc = WordCloud(background_color='white',
                    max_font_size=100, color_func=color_func)
        wc.generate_from_frequencies(d)

        # Display the generated image:
        plt.figure(figsize=(15, 15))
        plt.imshow(wc, interpolation='blackman')
        plt.axis("off")
        plt.savefig("wordclouds/cloud_t"+str(topic[0])+".png")

        file.append("\n")
        file.append("\n")
