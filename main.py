import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from movie import Movie
from recommender import Recommender

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False


def load_data():

    try:

        df = pd.read_csv(
            "netflix_titles.csv"
        )

        print("資料讀取成功")

        return df

    except FileNotFoundError:

        print("找不到CSV檔")

        return None


def clean_data(df):

    df = df.drop_duplicates()

    df["country"] = df["country"].fillna(
        "Unknown"
    )

    df["director"] = df["director"].fillna(
        "Unknown"
    )

    return df


def show_basic_info(df):

    print("\n資料筆數")

    print(len(df))

    print("\n欄位")

    print(df.columns)


def analyze_country(df):

    top_country = (
        df["country"]
        .value_counts()
        .head(10)
    )

    print("\n影片最多國家")

    print(top_country)

    plt.figure(figsize=(10, 5))

    top_country.plot(kind="bar")

    plt.title("Top 10 Countries")

    plt.xlabel("Country")

    plt.ylabel("Count")

    plt.show()


def analyze_type(df):

    movie_type = (
        df["type"]
        .value_counts()
    )

    print(movie_type)

    plt.figure(figsize=(6, 6))

    plt.pie(
        movie_type,
        labels=movie_type.index,
        autopct="%1.1f%%"
    )

    plt.title(
        "Movie vs TV Show"
    )

    plt.show()


def analyze_year(df):

    year_count = (
        df["release_year"]
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        year_count.index,
        year_count.values
    )

    plt.title(
        "Release Year Trend"
    )

    plt.xlabel("Year")

    plt.ylabel("Count")

    plt.show()


def analyze_genre(df):

    genres = {}

    for item in df["listed_in"]:

        if pd.isna(item):
            continue

        genre_list = item.split(",")

        for genre in genre_list:

            genre = genre.strip()

            if genre in genres:

                genres[genre] += 1

            else:

                genres[genre] = 1

    genre_df = (
        pd.DataFrame(
            genres.items(),
            columns=["Genre", "Count"]
        )
        .sort_values(
            by="Count",
            ascending=False
        )
        .head(10)
    )

    print("\n熱門類型")

    print(genre_df)

    plt.figure(figsize=(10, 5))

    plt.bar(
        genre_df["Genre"],
        genre_df["Count"]
    )

    plt.xticks(rotation=45)

    plt.title(
        "Top 10 Genres"
    )

    plt.show()


def create_movie_object(df):

    first = df.iloc[0]

    movie = Movie(
        first["title"],
        first["type"],
        first["country"],
        first["listed_in"]
    )

    print("\n物件導向展示")

    movie.display()


def recommendation_system(df):

    recommender = Recommender(df)

    movie_name = input(
        "\n請輸入電影名稱："
    )

    recommender.recommend(
        movie_name
    )


def main():

    df = load_data()

    if df is None:
        return

    df = clean_data(df)

    show_basic_info(df)

    analyze_country(df)

    analyze_type(df)

    analyze_year(df)

    analyze_genre(df)

    create_movie_object(df)

    recommendation_system(df)


if __name__ == "__main__":
    main()