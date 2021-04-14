import numpy as np
from lightfm import LightFM
from lightfm.data import Dataset
import sqlite3

def fetch_data():
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    # The result of a "cursor.execute" can be iterated over by row
    data = []
    users = []
    movies = []
    for row in cur.execute('SELECT id FROM RecoFramework_userinfo;'):
        users.append(row[0])

    for row in cur.execute('SELECT movieId FROM RecoFramework_movies;'):
        movies.append(row[0])

    for row in cur.execute('SELECT userId, movieId, rating FROM RecoFramework_ratings WHERE rating > 4;'):
        data.append(row)

    dataset = Dataset()
    print("Loading dataset...")
    dataset.fit(users, movies)
    interactions, ratings = dataset.build_interactions(data)

    # Be sure to close the connection
    con.close()

    model = LightFM(loss='warp')

    # train lightFM model using fit method
    print("Starting training the model...")
    model.fit(ratings, epochs=30, num_threads=2)

    user_dict = dataset._user_id_mapping
    movie_dict = dataset._item_id_mapping

    return model, ratings, user_dict, movie_dict

def recommend_by_userid(userid):

    # fetch data movie data and trained model from our database
    model, ratings, user_dict, movie_dict = fetch_data()
    movie_indices = list(movie_dict.keys())
    movie_ids = list(movie_dict.values())

    known_movies = []
    recommended_movies = []

    # number of movies and users in our dataset
    n_users, n_items = ratings.shape

    user_index = user_dict[userid]
    # list of movie indices that user likes
    known = ratings.tocsr()[user_index].indices
    for i, movie in enumerate(known):
        known_movies.append(movie_indices[movie_ids.index(movie)])
    # predicting the scores
    print('Predicting the scores')
    scores = model.predict(user_index, np.arange(n_items))

    # ranking them in non increasing order
    top = np.argsort(-scores)
    for i, movie in enumerate(top):
        recommended_movies.append(movie_indices[movie_ids.index(movie)])
    # display results
    print("User %s" % str(userid))
    print("------Known Choices:")
    for x in known_movies[:20]:
        print("%s" % x)
    print("------Recomended:")
    for x in recommended_movies[:10]:
        print("%s" % x)

    return recommended_movies[:10]

def evaluation():
    print("Starting evaluation our model...")

if __name__ == '__main__':
    # predicting top 10 movies for the user 23
    recommended_movies = recommend_by_userid(23)
