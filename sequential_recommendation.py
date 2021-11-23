import numpy as np
import pandas as pd
from itertools import combinations

from group_recommendation import user_wise_recommendations
from user_based_recom import ratings_data, set_ratings_data, movies_data


# Finding average of item dz in the group G
def seq_recom_for_group(user_group):
    splitted_data_set = [ratings_data.sample(n=50000), ratings_data.sample(n=18000), ratings_data.sample(n=18000), ratings_data.sample(n=25000), ratings_data.sample(n=20000)]

    alpha = 0
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
        for movie in recommendations_list.movie.unique():
            min_score_dz_j = float(recommendations_list[recommendations_list['movie'] == movie].score.min())
            avg_score_dz_j = float(recommendations_list[recommendations_list['movie'] == movie].score.mean())

            score_dz_j = float((1 - alpha) * avg_score_dz_j + alpha * min_score_dz_j)
            dz_scores_j.append(score_dz_j)
            movie_iterations.append(iteration_count)

        overall_movies.extend(recommendations_list.movie.unique())
        overall_dz_scores.extend(dz_scores_j)
        # print(recommendations_list)
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

    print('\n ===== User-wise satisfaction on each iteration =====')
    print(satisfaction_output)

    round_wise_dissatisfaction = pd.DataFrame(columns=['iteration', 'dissatisfaction'])
    for counted_iteration in range(1, iteration_count):
        current_satisfactions = satisfaction_output[satisfaction_output['iteration'] == counted_iteration]
        # print(current_satisfactions)
        iteration_dissatisfaction = 0.0
        for combo in combinations(current_satisfactions.user, 2):
            dissatisfaction = abs(float((current_satisfactions[current_satisfactions['user'] == combo[0]]).satisfaction.values[0] - (current_satisfactions[current_satisfactions['user'] == combo[1]]).satisfaction.values[0]))
            iteration_dissatisfaction = iteration_dissatisfaction + dissatisfaction
        round_wise_dissatisfaction = round_wise_dissatisfaction.append({'iteration': counted_iteration, 'dissatisfaction': iteration_dissatisfaction}, ignore_index=True)

    print('\n ===== Overall dissatisfaction in each round =====')
    print(round_wise_dissatisfaction)

    least_dissatisfaction_round_df = round_wise_dissatisfaction.nsmallest(1, 'dissatisfaction')
    print('\n ===== least dissatisfaction iteration is =====')
    print(least_dissatisfaction_round_df)
    least_dissatisfaction_round = least_dissatisfaction_round_df.head(1).iteration.values[0]

    suggestable_movie_list = complete_cycles_output[complete_cycles_output['iteration'] == least_dissatisfaction_round].nlargest(20, 'dz_score')

    print('\n ===== Movies suggested from the round ', least_dissatisfaction_round, ' =====')
    print('==================================================')
    for predicted_movie in suggestable_movie_list.movie:
        print(movies_data[movies_data['movieId'] == predicted_movie].title.values[0])


print("\n ===== Sequential recommendation for the list of users [1,10,31] ===== ")
seq_recom_for_group([1,10,31])