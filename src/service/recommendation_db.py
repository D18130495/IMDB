import pandas as pd
from math import *

import os

from src.mapping import mysql_connection

starMatrix = {}


# put all the data in 2D-array
# def matrix():
#     for line in file.readlines():
#         line = line.strip().split(',')
#         if not line[0] in starMatrix.keys():
#             starMatrix[line[0]] = {line[3]: line[1]}
#         else:
#             starMatrix[line[0]][line[3]] = line[1]


if __name__ == '__main__':
    matrix()
    # Recommendations = recommend("1")
    #
    # for video in Recommendations:
    #     print(video)
