import pandas as pd
from user_based_recom import get_movie_recommendations
from user_based_recom import movies_data
from itertools import combinations
import scipy.stats as stats


def user_wise_recommendations(user_group, keep_only_everyone_ranked=True):
    recommendations_list = pd.DataFrame()

    for user_id in user_group:
        # fetching movie recommendations for a given user
        user_movie_recommendations = get_movie_recommendations(user_id, 0)
        user_movie_recommendations = user_movie_recommendations.assign(user=user_id)
        # building data frame with users all recommendations for movies
        recommendations_list = recommendations_list.append(user_movie_recommendations, ignore_index=True)

    if keep_only_everyone_ranked:
        # Keep only duplicated ones (rated by more than 1 users in the similar users list)
        recommendations_list = recommendations_list[recommendations_list.groupby('movie')['movie'].transform('size') == len(user_group)]

    return recommendations_list


def recommend_for_group(user_group):
    recommendations_list = user_wise_recommendations(user_group)

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


# print("\n ===== Running group recommendation on user group [9,31,33] ===== ")
# recommend_for_group([9,31,33])


# Part B
def recommendation_with_distance(input_users):
    user_wise_recoms = user_wise_recommendations(input_users)
    kendall_tau_output = get_kendall_tau_disagreements(input_users, user_wise_recoms)
    print('\n======= Kendal tau calculation output =======')
    print(kendall_tau_output)
    for user in input_users:
        fair_points = kendall_tau_output[kendall_tau_output['user1'] == user].disagreement.sum()
        fair_points += kendall_tau_output[kendall_tau_output['user2'] == user].disagreement.sum()
        cond = user_wise_recoms['user']==user
        user_wise_recoms.loc[cond,'score'] -= fair_points

    print('\n======= Average aggregation after considering distances =======')
    avg_aggregation_df = average_aggregation(user_wise_recoms)
    for predicted_movie in avg_aggregation_df.movie:
        print(movies_data[movies_data['movieId'] == predicted_movie].title.values[0])


def get_kendall_tau_disagreements(input_users, user_wise_recoms):
    kendall_tau_output = pd.DataFrame(columns=['user1', 'user2', 'disagreement'])
    for combo in combinations(input_users, 2):
        user1_data = user_wise_recoms[user_wise_recoms['user'] == combo[0]]
        user2_data = user_wise_recoms[user_wise_recoms['user'] == combo[1]]
        user1_data = user1_data.sort_values(by=['score']).movie
        user2_data = user2_data.sort_values(by=['score']).movie

        # Shortening dataframes to match common length
        if user1_data.size > user2_data.size:
            user1_data = user1_data[:user2_data.size]
        elif user2_data.size > user1_data.size:
            user2_data = user2_data[:user1_data.size]

        kendall_distance = stats.kendalltau(user1_data, user2_data).correlation
        kendall_tau_output = kendall_tau_output.append({'user1': combo[0], 'user2': combo[1], 'disagreement': kendall_distance}, ignore_index=True)
    return kendall_tau_output


# print("\n ===== Running group recommendation with disagreement on user group [9,31,33] ===== ")
# recommendation_with_distance([9,31,33])
