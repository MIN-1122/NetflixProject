import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from movie import Movie
from recommender import Recommender

#使圖表能顯示中文及負號
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False


#資料讀取
def load_data():

    try:
        df = pd.read_csv("netflix_titles.csv")

        print("資料讀取成功")

        return df

    except FileNotFoundError:

        print("找不到CSV檔")

        return None


def clean_data(df):

    df = df.drop_duplicates()            #去除重複資料

    #將df[欄位]欄位中的空值用"Unknown"填補
    df["country"] = df["country"].fillna("Unknown")
    df["director"] = df["director"].fillna("Unknown")

    return df


def show_basic_info(df):

    #取得長度:len(物件)
    print("\n資料筆數")
    print(len(df))

    #取得欄位名稱
    print("\n欄位")
    print(df.columns)


#哪十個國家影片最多，長條圖:
def analyze_country(df):

    top_country = (
        df["country"]        #取得country欄位
        .value_counts()      #統計每個值出現的次數
        .head(10)            #保留前十名
    )

    print("\n影片最多國家")
    print(top_country)

    plt.figure(figsize=(10, 5))            #圖表大小
    top_country.plot(kind="bar")           #繪製長條圖

    plt.title("Top 10 Countries")
    plt.xlabel("Country")
    plt.ylabel("Count")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


#熱門類型:圓餅圖
def analyze_type(df):

    #熱門類型
    movie_type = (df["type"].value_counts())

    print(movie_type)

    plt.figure(figsize=(6, 6))

    plt.pie(
        movie_type,
        labels=movie_type.index,       #文字為類別名稱
        autopct="%1.1f%%"              #取到小數點後一位
    )

    plt.title("Movie vs TV Show")

    plt.show()

#每個年份的作品數量:折線圖
def analyze_year(df):

    year_count = (
        df["release_year"]
        .value_counts()
        .sort_index()                    #改順序
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        year_count.index,          #年份參數
        year_count.values,               #數量參數
        #marker="o",                     #增加線條與標記點
        linewidth=2,
        color = "steelblue"
    )

    plt.title("Release Year Trend")
    plt.xlabel("Year")
    plt.ylabel("Count")

    #開啟網格線，alpha=>透明度
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()

#統計 Netflix中最熱門的影片類型（Genre），顯示前 10 名的長條圖
def analyze_genre(df):

    genres = {}             #建立空字典儲存類型計數

    #逐筆讀取listed_in欄位
    for item in df["listed_in"]:

        #判斷是否為空值，否則跳過這次迴圈
        if pd.isna(item):
            continue

        genre_list = item.split(",")        #將多類型拆開

        #去除空白然後統計累加
        for genre in genre_list:

            genre = genre.strip()           #去除空白

            #累加記數
            if genre in genres:
                genres[genre] += 1
            else:
                genres[genre] = 1

    #轉成DataFrame
    genre_df = (
        pd.DataFrame(
            genres.items(),
            columns=["Genre", "Count"]
        )
        #一大到小進行排序
        .sort_values(
            by="Count",
            ascending=False
        )
        .head(10)            #只保留前10筆
    )

    print("\n熱門類型")

    print(genre_df)

    plt.figure(figsize=(10, 5))

    plt.bar(
        genre_df["Genre"],
        genre_df["Count"]
    )

    plt.xticks(rotation=45)            #旋轉標籤

    plt.title(
        "Top 10 Genres"
    )

    plt.tight_layout()
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