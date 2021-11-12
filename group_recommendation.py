import pandas as pd
import numpy as np
from user_based_recom import get_movie_recommendations
from user_based_recom import movies_data


def recommend_for_group(user_group):
    recommendations_list = pd.DataFrame()

    for user_id in user_group:
        # fetching movie recommendations for a given user
        user_movie_recommendations = get_movie_recommendations(user_id, 0)
        # building data frame with users all recommendations for movies
        recommendations_list = recommendations_list.append(user_movie_recommendations, ignore_index=True)

    # recommendations_list = recommendations_list[recommendations_list.groupby(['movie'])['movie'].transform('size') > 2]
    # TODO: Assumption to mention
    # Keep only duplicated ones (rated by more than 1 users in the similar users list)
    recommendations_list = recommendations_list[recommendations_list.groupby('movie')['movie'].transform('size') == len(user_group)]

    print('\n======= Movie list according to Average Aggregation =======')
    avg_aggregation_df = average_aggregation(recommendations_list)
    for predicted_movie in avg_aggregation_df.movie:
        print(movies_data[movies_data['movieId']==predicted_movie].title.values[0])

    print('\n\n======= Movie list according to Least Misery Aggregation =======')
    least_misery_aggregation_df = least_misery_aggregation(recommendations_list)
    for predicted_movie in least_misery_aggregation_df.movie:
        print(movies_data[movies_data['movieId']==predicted_movie].title.values[0])


# Function that does average aggregation of the given list
def average_aggregation(recommendations_list):
    # Calculating average rating of the given movie
    recommendations_list = recommendations_list.groupby('movie')['score'].mean().reset_index()
    recommendations_list = recommendations_list.nlargest(20, 'score')
    return recommendations_list


# Function that does least misery aggregation of the given list
def least_misery_aggregation(recommendations_list):
    # Calculating minimum rating of the given movie
    recommendations_list = recommendations_list.groupby('movie')['score'].min().reset_index()
    recommendations_list = recommendations_list.nlargest(20, 'score')
    return recommendations_list


recommend_for_group([9,31,33])