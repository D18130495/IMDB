import pandas as pd
from math import *
import numpy as np

movies = pd.read_csv("./ml-latest-small/movies.csv")
ratings = pd.read_csv("./ml-latest-small/ratings.csv")
data = pd.merge(movies, ratings, on='movieId')
data = data[['userId', 'rating', 'movieId', 'title']].sort_values(by="userId", ascending=True)

for line in range(len(data)):
    if data["title"][line][-12:-7] == ", The":
        data.loc[line, "title"] = "The " + data["title"][line].replace(", The", "")

data.to_csv('./ml-latest-small/data.csv', index=False)
