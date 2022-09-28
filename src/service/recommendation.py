import pandas as pd
from math import *

import os

starMatrix = {}


def merge_data():
    movies = pd.read_csv("../../ml-latest-small/movies.csv")
    ratings = pd.read_csv("../../ml-latest-small/ratings.csv")
    data = pd.merge(movies, ratings, on='movieId')
    data = data[['userId', 'rating', 'movieId', 'title']].sort_values(by="userId", ascending=True)

    for line in range(len(data)):
        if data["title"][line][-12:-7] == ", The":
            data.loc[line, "title"] = "The " + data["title"][line].replace(", The", "")

    data.to_csv('../../ml-latest-small/data.csv', index=False)


# put all the data in 2D-array
def matrix():
    file = open('../../ml-latest-small/data.csv', 'r', encoding='UTF-8')

    for line in file.readlines():
        line = line.strip().split(',')
        if not line[0] in starMatrix.keys():
            starMatrix[line[0]] = {line[3]: line[1]}
        else:
            starMatrix[line[0]][line[3]] = line[1]


# find the highest similarity user in the record, and recommend the movie he/she hasn't watched
def recommend(user_id):
    similar_user = similar(user_id)[0][0]
    items = starMatrix[similar_user]
    recommendations = []

    for item in items.keys():
        if item not in starMatrix[user_id].keys():
            recommendations.append((item, items[item]))
    recommendations.sort(key=lambda val: val[1], reverse=True)
    return recommendations[:20]


# find the similar user
def similar(user_id):
    res = []

    for userid in starMatrix.keys():
        if not userid == user_id:
            similar_rate = euclidean(user_id, userid)
            res.append((userid, similar_rate))
    res.sort(key=lambda val: val[1])
    return res[:4]


# euclidean algorithm use to calculate the distance between two users
def euclidean(user1, user2):
    user1_data = starMatrix[user1]
    user2_data = starMatrix[user2]
    distance = 0

    for key in user1_data.keys():
        if key in user2_data.keys():
            distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)

    return 1 / (1 + sqrt(distance))


if __name__ == '__main__':
    if not os.path.exists('../../ml-latest-small/data.csv'):
        merge_data()

    matrix()
    Recommendations = recommend("1")

    for video in Recommendations:
        print(video)

