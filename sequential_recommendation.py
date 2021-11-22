import numpy as np
import pandas as pd

from group_recommendation import user_wise_recommendations
from user_based_recom import ratings_data, set_ratings_data


# Finding average of item dz in the group G
def seq_recom_for_group(user_group):
    splitted_data_set = [ratings_data.sample(n=50000), ratings_data.sample(n=18000), ratings_data.sample(n=18000), ratings_data.sample(n=25000), ratings_data.sample(n=20000)]

    alpha = 0
    overall_iterations = []
    iteration_count = 1
    overall_movies = []
    overall_dz_scores = []
    overall_satisfactions = []
    overall_users = []
    movie_iterations = []
    user_iterations = []

    for data_set_itr in splitted_data_set:
        dz_scores_j = []
        satisfactions = []
        users_gp = []
        set_ratings_data(data_set_itr)
        recommendations_list = user_wise_recommendations(user_group)
        # average_aggregation = recommendations_list.groupby('movie')['score'].mean().reset_index()
        # least_mis_aggregation = recommendations_list = recommendations_list.groupby('movie')['score'].min().reset_index()
        print(iteration_count)
        for movie in recommendations_list.movie.unique():
            min_score_dz_j = float(recommendations_list[recommendations_list['movie'] == movie].score.min())
            avg_score_dz_j = float(recommendations_list[recommendations_list['movie'] == movie].score.mean())

            score_dz_j = float((1 - alpha) * avg_score_dz_j + alpha * min_score_dz_j)
            dz_scores_j.append(score_dz_j)
            movie_iterations.append(iteration_count)

        overall_movies.extend(recommendations_list.movie.unique())
        overall_dz_scores.extend(dz_scores_j)
        print(recommendations_list)
        # calculating alpha
        for user in user_group:
            user_list_sat = sum((recommendations_list[recommendations_list['user'] == user]).score)
            group_list_sat = sum(dz_scores_j)
            satisfaction = np.float64(user_list_sat/group_list_sat)
            satisfactions.append(satisfaction)
            users_gp.append(user)
            user_iterations.append(iteration_count)

        # calculate and set alpha for next round
        alpha = float(max(satisfactions) - min(satisfactions))
        overall_satisfactions.extend(satisfactions)
        overall_users.extend(users_gp)
        iteration_count = iteration_count + 1

    complete_cycles_output = pd.DataFrame(list(zip(overall_movies, overall_dz_scores, movie_iterations)), columns=['movie', 'dz_score', 'iteration'])
    satisfaction_output = pd.DataFrame(list(zip(overall_users, overall_satisfactions, user_iterations)), columns=['user', 'satisfaction', 'iteration'])

    print(complete_cycles_output)
    print('=================================')
    print(satisfaction_output)

print("\n ===== Seq. recommendation list [9,31,33] ===== ")
seq_recom_for_group([1,10,31])