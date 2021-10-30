import pandas as pd
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

ratings_data = pd.read_csv('ml-latest-small/ratings.csv')

movies_data = pd.read_csv('ml-latest-small/movies.csv')
ratings_with_name = pd.merge(ratings_data, movies_data).drop(['genres'], axis=1)

def pearson_correlation(a, b, rated_intersection):
    average_a = float(sum(a['rating'])/len(a['rating']))
    average_b = float(sum(b['rating'])/len(b['rating']))
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    sim_a_b = 0
    for common_movie_id in rated_intersection['movieId']:
        a_rating_for_movie = float(a[a['movieId'] == common_movie_id].rating)
        b_rating_for_movie = float(b[b['movieId'] == common_movie_id].rating)

        numerator += (a_rating_for_movie - average_a) * (b_rating_for_movie - average_b)

        denominator1 += (a_rating_for_movie - average_a) * (a_rating_for_movie - average_a)
        denominator2 += (b_rating_for_movie - average_b) * (b_rating_for_movie - average_b)
        if (denominator1 > 0 and denominator2 > 0):
            sim_a_b = numerator / ((np.sqrt(denominator1)) * (np.sqrt(denominator2)))

    return sim_a_b


def matching_users(input_user):
    rated_all_users = ratings_data['userId'].unique()
    input_user_ratings = ratings_data[ratings_data['userId']==input_user]

    correlations_list = list()
    similar_users = list()

    for iterative_user_id in rated_all_users:
        if iterative_user_id != input_user :
            iterative_user_ratings = ratings_data[ratings_data['userId'] == iterative_user_id]
            rated_intersection = pd.merge(input_user_ratings, iterative_user_ratings, on=['movieId', 'movieId'], how='inner')
            if not rated_intersection.empty:
                similarity_a_b = pearson_correlation(input_user_ratings, iterative_user_ratings, rated_intersection)
                correlations_list.append(similarity_a_b)
                similar_users.append(iterative_user_id)

    dataframe_with_similar_data = pd.DataFrame(list(zip(similar_users, correlations_list)), columns = ['userId', 'correlations'])
    most_similar_users_10 = dataframe_with_similar_data.nlargest(10, 'correlations')

    return most_similar_users_10




def user_based_recommendation():
    print("====== First 10 ratings data items ======")
    print(ratings_data.head(10))

    print("====== Length of data ======")
    print(len(ratings_data))

    user_id_input = 10
    most_similar_10 = matching_users(user_id_input)
    print("====== 10 most similar users ======")
    print(most_similar_10['userId'].values)















