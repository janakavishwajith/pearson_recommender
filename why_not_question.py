import numpy as np
import pandas as pd
from itertools import combinations

from group_recommendation import user_wise_recommendations, average_aggregation
from user_based_recom import ratings_data, set_ratings_data, movies_data, matching_users_dataframe


def why_not_movie(user_group, movie):
    recommendations_list = user_wise_recommendations(user_group, False)

    existing_in_suggestion = recommendations_list[recommendations_list['movie'] == movie]
    print(existing_in_suggestion.user.tolist())
    suggestion_not_exists = pd.DataFrame(columns=['user'])
    for group_user in user_group:
        if group_user not in existing_in_suggestion.user.tolist():
            suggestion_not_exists = suggestion_not_exists.append({'user': group_user}, ignore_index=True)

    # This will check if any of the group users has not been suggested the particular movie
    # TODO: Uncomment
    if not suggestion_not_exists.empty:
        print('========= Movie ', movies_data[movies_data['movieId'] == movie].title.values[0],
              ' has not been suggested to user(s) ', suggestion_not_exists.user.tolist(), ' of the group.')

        # This should go through the user level why-not question

    # TODO: Uncomment
    if suggestion_not_exists.empty:
        aggregated_results = average_aggregation(recommendations_list)
        lowest_score = aggregated_results.score.min()

        for existing_rating_user in existing_in_suggestion.user:
            if existing_in_suggestion[existing_in_suggestion['user'] == existing_rating_user].score.values[0] < lowest_score:
                print('User ', existing_rating_user, ' suggestion score is lower than lowest score...')


def user_why_not_movie(user_id, movie):
    # Getting 10 matching users set
    matching_users = matching_users_dataframe(user_id)

    user_x_rating_on_movie = pd.DataFrame()
    for matched_user in matching_users.userId:
        user_x_rating_on_movie = user_x_rating_on_movie.append(ratings_data[(ratings_data['userId'] == matched_user) & (ratings_data['movieId'] == movie)])

    if user_x_rating_on_movie.empty:
        print('Any other similar user has not rated this movie.')
    elif user_x_rating_on_movie.size < (matching_users.size/2):
        print('Less than half of the similar users have rated this movie. ')
    else:
        if user_x_rating_on_movie[user_x_rating_on_movie['rating'] < 3].size < (matching_users.size/2):
            print('More than 50% of the similar users have given low ratings for the movie.')


# why_not_movie([2,10,22], 21)

def why_not_genre(user_group, genre):
    recommendations_list = user_wise_recommendations(user_group, False)
    merged_recommendation = pd.merge(recommendations_list, movies_data, left_on='movie', right_on='movieId', how='inner')

    existing_in_suggestion = pd.DataFrame()

    for movie_genres in merged_recommendation[['genres','user','movieId']]:
        if genre in movie_genres.genres:
            existing_in_suggestion = existing_in_suggestion.append(movie_genres)

    print(existing_in_suggestion)
    suggestion_not_exists = pd.DataFrame(columns=['user'])
    for group_user in user_group:
        if group_user not in existing_in_suggestion.user.tolist():
            suggestion_not_exists = suggestion_not_exists.append({'user': group_user}, ignore_index=True)

    # This will check if any of the group users has not been suggested the particular movie
    # TODO: Uncomment
    # if not suggestion_not_exists.empty:
    #     print('========= Movie ', movies_data[movies_data['movieId'] == movie].title.values[0],
    #           ' has not been suggested to user(s) ', suggestion_not_exists.user.tolist(), ' of the group.')

        # This should go through the user level why-not question

    # TODO: Uncomment
    # if suggestion_not_exists.empty:
    aggregated_results = average_aggregation(recommendations_list)
    lowest_score = aggregated_results.score.min()

    for existing_rating_user in existing_in_suggestion.user:
        if existing_in_suggestion[existing_in_suggestion['user'] == existing_rating_user].score.values[0] < lowest_score:
            print('User ', existing_rating_user, ' suggestion score is lower than lowest score...')


def user_why_not_genre(user_id, movie):
    # Getting 10 matching users set
    matching_users = matching_users_dataframe(user_id)

    user_x_rating_on_movie = pd.DataFrame()
    for matched_user in matching_users.userId:
        user_x_rating_on_movie = user_x_rating_on_movie.append(ratings_data[(ratings_data['userId'] == matched_user) & (ratings_data['movieId'] == movie)])

    if user_x_rating_on_movie.empty:
        print('Any other similar user has not rated this movie.')
    elif user_x_rating_on_movie.size < (matching_users.size/2):
        print('Less than half of the similar users have rated this movie. ')
    else:
        if user_x_rating_on_movie[user_x_rating_on_movie['rating'] < 3].size < (matching_users.size/2):
            print('More than 50% of the similar users have given low ratings for the movie.')

why_not_genre([2,10,22], 'Comedy')