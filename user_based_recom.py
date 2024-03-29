import pandas as pd
import numpy as np

ratings_data = pd.read_csv('ml-latest-small/ratings.csv')
movies_data = pd.read_csv('ml-latest-small/movies.csv')


def set_ratings_data(ratings_data_input):
    global ratings_data
    ratings_data = ratings_data_input

# Pearson correlation function
def pearson_correlation(a, b, rated_intersection):
    # Averages for the pearson function
    average_a = float(sum(a['rating'])/len(a['rating']))
    average_b = float(sum(b['rating'])/len(b['rating']))
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    sim_a_b = 0

    # applying the pearson correlation function iteratively on every common movie
    for common_movie_id in rated_intersection['movieId']:
        a_rating_for_movie = float(a[a['movieId'] == common_movie_id].rating)
        b_rating_for_movie = float(b[b['movieId'] == common_movie_id].rating)

        numerator += (a_rating_for_movie - average_a) * (b_rating_for_movie - average_b)

        denominator1 += (a_rating_for_movie - average_a) * (a_rating_for_movie - average_a)
        denominator2 += (b_rating_for_movie - average_b) * (b_rating_for_movie - average_b)

        # Calling the function and identifying similarities of the users
        if (denominator1 > 0 and denominator2 > 0):
            sim_a_b = numerator / ((np.sqrt(denominator1)) * (np.sqrt(denominator2)))

    return sim_a_b

def matching_users_dataframe(input_user):
    # Taking the unique users lists
    rated_all_users = ratings_data['userId'].unique()

    # ratings added by the input user
    input_user_ratings = ratings_data[ratings_data['userId']==input_user]

    correlations_list = list()
    similar_users = list()

    for iterative_user_id in rated_all_users:
        if iterative_user_id != input_user:
            # merge input user movies and current iteration users ratings on same movie
            iterative_user_ratings = ratings_data[ratings_data['userId'] == iterative_user_id]
            rated_intersection = pd.merge(input_user_ratings, iterative_user_ratings, on=['movieId', 'movieId'], how='inner')

            #if there are any common movies, then calculate pearson correlation
            if not rated_intersection.empty:
                similarity_a_b = pearson_correlation(input_user_ratings, iterative_user_ratings, rated_intersection)
                correlations_list.append(similarity_a_b)
                similar_users.append(iterative_user_id)

    # new dataframe build based on similarity matrix
    dataframe_with_similar_data = pd.DataFrame(list(zip(similar_users, correlations_list)), columns = ['userId', 'correlation'])

    return dataframe_with_similar_data


def movie_predictions(user):
    global top_similar_users

    # Identifying the movie ids of the user that we are looking for
    user_movie_ids = ratings_data[ratings_data['userId']==user].movieId

    # Creating a dataframe with similar user's movie ratings only
    top_similar_rated_movies = pd.DataFrame()
    for similar_user in top_similar_users.userId:
        top_similar_rated_movies = top_similar_rated_movies.append(ratings_data[ratings_data['userId'] == similar_user])

    # making a list of movies that contains similar users movies, but not containing users rated movies
    suggestable_movies = list()
    for movie_id in top_similar_rated_movies.movieId.unique():
        if movie_id not in user_movie_ids:
            suggestable_movies.append(movie_id)

    avg_of_user = float(np.mean(ratings_data[ratings_data.userId == user].rating))
    denominator = float(sum(top_similar_users.correlation))
    numerator = 0
    recommendations = list()
    top_movies = list()
    for movie in suggestable_movies:
        similar_movie = top_similar_rated_movies[top_similar_rated_movies['movieId']==movie]
        for similar_movie_user in similar_movie['userId']:
            avg_of_user_this_user = float(np.mean(ratings_data[ratings_data.userId == similar_movie_user].rating))
            rbp = float(similar_movie[similar_movie['userId']==similar_movie_user].rating.values.tolist()[0])
            correlation = float(top_similar_users[top_similar_users['userId'] == similar_user].correlation)
            numerator += (correlation)*(rbp - avg_of_user_this_user)
        prediction = avg_of_user + (numerator/denominator)
        recommendations.append(prediction)
        top_movies.append(movie)

    movie_recommendations = pd.DataFrame(list(zip(top_movies, recommendations)), columns=['movie', 'score'])
    return movie_recommendations


def set_similar_users(user_id_input):
    global top_similar_users

    similar_user_results_count = 10

    matching_users_movies_data = matching_users_dataframe(user_id_input)
    top_similar_users = matching_users_movies_data.nlargest(similar_user_results_count, 'correlation')

    # print("====== " + str(similar_user_results_count) + " most similar users ======")
    # print(top_similar_users['userId'].values)


def get_movie_recommendations(user_id_input, limit):
    set_similar_users(user_id_input)

    movies_recommendation = movie_predictions(user_id_input)
    if limit > 0:
        top_predictions = movies_recommendation.nlargest(limit, 'score')
    else:
        top_predictions = movies_recommendation

    return top_predictions


def user_based_recommendation():
    global top_similar_users

    print("====== First 10 ratings data items ======")
    print(ratings_data.head(10))

    print("====== Length of data ======")
    print(len(ratings_data))

    user_id_input = int(input("Type in your user id: "))

    top_predictions = get_movie_recommendations(user_id_input, 20)

    for predicted_movie in top_predictions.movie:
        print(movies_data[movies_data['movieId']==predicted_movie].title.values[0])








