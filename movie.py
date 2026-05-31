class Movie:

    def __init__(self, title, movie_type, country, genre):
        self.title = title
        self.movie_type = movie_type
        self.country = country
        self.genre = genre

    def display(self):
        print("影片名稱:", self.title)
        print("類型:", self.movie_type)
        print("國家:", self.country)
        print("分類:", self.genre)