import numpy as np
import pandas as pd
from itertools import combinations

from group_recommendation import user_wise_recommendations
from user_based_recom import ratings_data, set_ratings_data, movies_data


def seq_recom_for_group(user_group):
    # Splitting data set into 5 parts
    splitted_data_set = [ratings_data.sample(n=50000), ratings_data.sample(n=30000), ratings_data.sample(n=18000), ratings_data.sample(n=20000), ratings_data.sample(n=25000)]

    alpha = 0
    iteration_count = 1
    overall_movies = []
    overall_dz_scores = []
    overall_satisfactions = []
    overall_users = []
    movie_iterations = []
    user_iterations = []

    # Iterations are done based on splitted data sets, consider 1 by 1 on each iteration
    for data_set_itr in splitted_data_set:
        dz_scores_j = []
        satisfactions = []
        users_gp = []
        iteration_movies = []
        iteration_scores = []
        set_ratings_data(data_set_itr)
        recommendations_list = user_wise_recommendations(user_group)

        # Iterate through the movies list and calculate score against every movie
        for movie in recommendations_list.movie.unique():
            min_score_dz_j = float(recommendations_list[recommendations_list['movie'] == movie].score.min())
            avg_score_dz_j = float(recommendations_list[recommendations_list['movie'] == movie].score.mean())

            score_dz_j = float((1 - alpha) * avg_score_dz_j + alpha * min_score_dz_j)
            dz_scores_j.append(score_dz_j)
            movie_iterations.append(iteration_count)

        iteration_movies.extend(recommendations_list.movie.unique())
        iteration_scores.extend(dz_scores_j)
        iteration_suggestions = pd.DataFrame(list(zip(iteration_movies, iteration_scores)), columns=['movie', 'dz_score'])
        iteration_suggestions = iteration_suggestions.nlargest(20, 'dz_score')

        print('\n ===== Movies list prediction at iteration ', iteration_count, ' =====')
        for predicted_movie in iteration_suggestions.movie:
            print(movies_data[movies_data['movieId'] == predicted_movie].title.values[0])

        overall_movies.extend(recommendations_list.movie.unique())
        overall_dz_scores.extend(dz_scores_j)

        # Calculating satisfaction to calculate alpha
        for user in user_group:
            user_list_sat = sum((recommendations_list[recommendations_list['user'] == user]).score)
            group_list_sat = sum(dz_scores_j)
            satisfaction = np.float64(group_list_sat/user_list_sat)
            satisfactions.append(satisfaction)
            users_gp.append(user)
            user_iterations.append(iteration_count)

        # calculate and set alpha for next round
        alpha = float(max(satisfactions) - min(satisfactions))
        overall_satisfactions.extend(satisfactions)
        overall_users.extend(users_gp)
        iteration_count = iteration_count + 1

    # DataFrame that consists the dz score and iterations against every movie that considered
    complete_cycles_output = pd.DataFrame(list(zip(overall_movies, overall_dz_scores, movie_iterations)), columns=['movie', 'dz_score', 'iteration'])

    # Dataframe that contains the user user wise satisfaction in every iteration
    satisfaction_output = pd.DataFrame(list(zip(overall_users, overall_satisfactions, user_iterations)), columns=['user', 'satisfaction', 'iteration'])

    print('\n ===== User-wise satisfaction on each iteration =====')
    print(satisfaction_output)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # Finding the best iteration to consider for recommender  # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Finding the dissatisfaction of the outputs
    round_wise_dissatisfaction = pd.DataFrame(columns=['iteration', 'dissatisfaction'])
    for counted_iteration in range(1, iteration_count):
        current_satisfactions = satisfaction_output[satisfaction_output['iteration'] == counted_iteration]
        iteration_dissatisfaction = 0.0
        # Logic is to identify the satisfaction gap between each users
        # And adding them together to identify the magnitude of the dissatisfaction among users in a particular iteration
        for combo in combinations(current_satisfactions.user, 2):
            dissatisfaction = abs(float((current_satisfactions[current_satisfactions['user'] == combo[0]]).satisfaction.values[0] - (current_satisfactions[current_satisfactions['user'] == combo[1]]).satisfaction.values[0]))
            iteration_dissatisfaction = iteration_dissatisfaction + dissatisfaction
        round_wise_dissatisfaction = round_wise_dissatisfaction.append({'iteration': counted_iteration, 'dissatisfaction': iteration_dissatisfaction}, ignore_index=True)

    print('\n ===== Overall dissatisfaction in each round =====')
    print(round_wise_dissatisfaction)

    # Get the round with lowest dissatisfaction
    least_dissatisfaction_round_df = round_wise_dissatisfaction.nsmallest(1, 'dissatisfaction')
    print('\n ===== least dissatisfaction iteration is =====')
    print(least_dissatisfaction_round_df)
    least_dissatisfaction_round = least_dissatisfaction_round_df.head(1).iteration.values[0]

    # Movies list of the iteration that has the least dissatisfaction
    suggestable_movie_list = complete_cycles_output[complete_cycles_output['iteration'] == least_dissatisfaction_round].nlargest(20, 'dz_score')

    print('\n ===== Movies suggested from the round ', least_dissatisfaction_round, ' =====')
    print('==================================================')
    for predicted_movie in suggestable_movie_list.movie:
        print(movies_data[movies_data['movieId'] == predicted_movie].title.values[0])


print("\n ===== Sequential recommendation for the list of users [1,10,31] ===== ")
seq_recom_for_group([1,10,31])