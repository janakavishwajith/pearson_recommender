import pandas as pd
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

ratings_data = pd.read_csv('../ml-latest-small/ratings.csv')
print(ratings_data.head(10))
print('Length of data', len(ratings_data))

movies_data = pd.read_csv('../ml-latest-small/movies.csv')
ratings_with_name = pd.merge(ratings_data, movies_data).drop(['genres'], axis=1)


def get_similar_users(user_id):
    user_ids_list = ratings_data['userId'].unique()

    for itr_user_id in user_ids_list:
        u2 = ratings_with_name[ratings_data["userId"] == itr_user_id]
        print(u2)

def recommendation():
    user_id_input = 10
    most_similar_10 = get_similar_users(user_id_input)



recommendation()










