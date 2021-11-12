import pandas as pd
import numpy as np
from user_based_recom import get_movie_recommendations
from user_based_recom import movies_data

def recommend_for_group(user_group):

    recommendations_list = pd.DataFrame()
    for user_id in user_group:
        user_movie_recommendations = get_movie_recommendations(user_id, 0)
        # print(user_movie_recommendations)
        recommendations_list = recommendations_list.append(user_movie_recommendations, ignore_index=True)

    # recommendations_list = recommendations_list[recommendations_list.groupby(['movie'])['movie'].transform('size') > 2]
    # print(recommendations_list)
    # TODO: Assumption to mention
    # Keep only duplicated ones (rated by more than 1 users in the similar users list)
    # recommendations_list = recommendations_list[recommendations_list.duplicated(subset=['movie'], keep=False)]
    recommendations_list = recommendations_list[recommendations_list.groupby('movie')['movie'].transform('size') == len(user_group)]

    # Calculating average
    recommendations_list = recommendations_list.groupby('movie')['score'].mean().reset_index()
    recommendations_list = recommendations_list.nlargest(20, 'score')

    for predicted_movie in recommendations_list.movie:
        print(movies_data[movies_data['movieId']==predicted_movie].title.values[0])


recommend_for_group([9,31,33])