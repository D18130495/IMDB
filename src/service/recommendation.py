import time

import pandas as pd
from math import *
import numpy as np


def merge_data():
    movies = pd.read_csv("../../ml-latest-small/movies.csv")
    ratings = pd.read_csv("../../ml-latest-small/ratings.csv")
    data = pd.merge(movies, ratings, on='movieId')
    data = data[['userId', 'rating', 'movieId', 'title']].sort_values(by="userId", ascending=True)

    for line in range(len(data)):
        if data["title"][line][-12:-7] == ", The":
            data.loc[line, "title"] = "The " + data["title"][line].replace(", The", "")

    data.to_csv('../../ml-latest-small/data.csv', index=False)


def matrix():
    file = open('../../ml-latest-small/data.csv', 'r', encoding='UTF-8')
    data = {}

    for line in file.readlines():
        line = line.strip().split(',')
        if not line[0] in data.keys():
            data[line[0]] = {line[3]: line[1]}
        else:
            data[line[0]][line[3]] = line[1]


if __name__ == '__main__':
    # merge_data()
    matrix()
