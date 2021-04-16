import numpy as np
from lightfm import LightFM
from lightfm.data import Dataset
import sqlite3
from lightfm.evaluation import precision_at_k
from lightfm.evaluation import auc_score
from lightfm.cross_validation import random_train_test_split
from lightfm.datasets import fetch_movielens

def dict_factory(cursor, row):
    d = {}
    d[row[0]] = row[1:]
    return d

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

    for row in cur.execute('SELECT userId, movieId, rating FROM RecoFramework_ratings WHERE rating = 5;'):
        data.append(row)

    # Be sure to close the connection
    con.close()

    dataset = Dataset()
    print("Loading dataset...")

    dataset.fit(users, movies)
    interactions, ratings = dataset.build_interactions(data)

    train = interactions.tocsr()[:, :1682]
    # train, test = random_train_test_split(interactions)

    test = fetch_movielens()['test']

    model = LightFM(loss='warp')

    # train lightFM model using fit method
    print("Starting training the model...")
    model.fit(train, epochs=30, num_threads=2)

    user_dict = dataset._user_id_mapping
    movie_dict = dataset._item_id_mapping

    return model, ratings, user_dict, movie_dict, train, test

def recommend_by_userid(userid):

    # fetch data movie data and trained model from our database
    model, _, user_dict, movie_dict, train, test = fetch_data()
    movie_indices = list(movie_dict.keys())
    movie_ids = list(movie_dict.values())

    known_movies = []
    recommended_movies = []

    # number of movies and users in our dataset
    n_users, n_items = train.shape

    user_index = user_dict[userid]
    # list of movie indices that user likes
    known = train.tocsr()[user_index].indices
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

    con = sqlite3.connect("db.sqlite3")
    con.row_factory = dict_factory
    cur = con.cursor()
    result = []

    for mid in recommended_movies[:10]:
        cur.execute("SELECT * FROM RecoFramework_movies WHERE movieId=?", (mid, ))
        r = cur.fetchone()
        result.append(r)

    con.close()

    evaluation(model, train, test)

    return result

def evaluation(model, train, test):
    print("\nStarting evaluation our model...")
    train_precision = precision_at_k(model, train, k=10).mean()
    test_precision = precision_at_k(model, test, k=10).mean()

    train_auc = auc_score(model, train).mean()
    test_auc = auc_score(model, test).mean()

    print('Precision: train %.2f, test %.2f.' % (train_precision, test_precision))
    print('AUC: train %.2f, test %.2f.' % (train_auc, test_auc))

if __name__ == '__main__':
    # predicting top 10 movies for the user 23
    recommended_movies = recommend_by_userid(4)
