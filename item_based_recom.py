"""
Recommender systems assignment 1
Group members: Janaka Nawagamuwa & Oloruntobiloba Kolawole
"""

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

ratings_data = pd.read_csv('ml-latest-small/ratings.csv')


movies_data = pd.read_csv('ml-latest-small/movies.csv')

# displaying the count of ratings
ratings_data.count()
# merging the two datasets together
ratings_data = pd.merge(movies_data, ratings_data)
ratings_data.head()
# .drop removes irrelevant columns
ratings_data = pd.merge(movies_data, ratings_data).drop(['genres', 'timestamp'], axis=1)
ratings_data.head()
ratings_for_users = ratings_data.pivot_table(index=['userId'], columns=['title'], values='rating')
ratings_for_users.head()
# select movies with 10 users or more
ratings_for_users = ratings_for_users.dropna(thresh=10, axis=1).fillna(0)
ratings_for_users.head()


def standardization(row):
    current_row = (row - row.mean()) / (row.max() - row.min())
    return current_row


# Making Recommendations
def movies_similarity(movie_name, rating):
    ratings_std = ratings_for_users.apply(standardization)

    # Calculating the similarity between items using the cosine similarity method
    # We are taking the transpose of the matrix because we want to cac
    item_similarity = cosine_similarity(ratings_std.T)
    # similarity matrix
    item_similarity_df = pd.DataFrame(item_similarity, index=ratings_for_users.columns,
                                      columns=ratings_for_users.columns)
    close_movie_references = (item_similarity_df[movie_name] * (rating - 2.5))
    # sort the list in descending order
    close_movie_references = close_movie_references.sort_values(ascending=False)

    return close_movie_references


like_movies = pd.DataFrame()


def like_movies_for_user(id):
    global like_movies
    test = ratings_for_users[(ratings_for_users.index.isin([id]))]
    top_rated = (test.loc[id].sort_values(ascending=False).nlargest(5))
    for a, b in top_rated.items():
        like_movies = like_movies.append(movies_similarity(a, b), ignore_index=True)
    return like_movies


def recommendations():
    user_ = int(input("Type in your user id: "))
    like_movies_for_user(user_)
    # Sum all the values(ratings) row-wise'
    print("These are the movies recommended for you...")
    print(like_movies.sum().sort_values(ascending=False).head(20))

recommendations()
