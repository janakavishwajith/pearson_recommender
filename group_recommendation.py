import pandas as pd
import numpy as np
from user_based_recom import get_movie_recommendations

def recommend_for_group(user_group):

    recommendations_list = list()
    for user_id in user_group:
        user_movie_recommendations = get_movie_recommendations(user_id)
        # print(user_movie_recommendations)
        recommendations_list.append(user_movie_recommendations)

    recommendations_list = pd.concat(recommendations_list)
    recommendations_list = recommendations_list[recommendations_list.groupby(['movie'])['movie'].transform('size') > 2]
    print(recommendations_list.nlargest(60, 'score'))
    recommendations_list.groupby(['movie']).mean()
    print(recommendations_list.nlargest(50, 'score'))

recommend_for_group([9, 31, 11])