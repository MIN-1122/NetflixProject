import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Recommender:

    def __init__(self, dataframe):
        self.df = dataframe

    def recommend(self, movie_title):

        self.df["listed_in"] = self.df["listed_in"].fillna("")

        vectorizer = CountVectorizer()

        matrix = vectorizer.fit_transform(
            self.df["listed_in"]
        )

        similarity = cosine_similarity(matrix)

        movie_index = self.df[
            self.df["title"] == movie_title
        ].index

        if len(movie_index) == 0:
            print("找不到此電影")
            return

        movie_index = movie_index[0]

        scores = list(
            enumerate(similarity[movie_index])
        )

        scores = sorted(
            scores,
            key=lambda x: x[1],
            reverse=True
        )

        print("\n推薦電影：")

        count = 0

        for i in scores[1:6]:

            idx = i[0]

            print(
                self.df.iloc[idx]["title"]
            )

            count += 1

            if count == 5:
                break