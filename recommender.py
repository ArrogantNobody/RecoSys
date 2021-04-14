import numpy as np
from lightfm import LightFM
from lightfm.data import Dataset
import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

# The result of a "cursor.execute" can be iterated over by row
data = []

for row in cur.execute('SELECT userId, movieId, rating FROM RecoFramework_ratings;'):
    data.append(row)

dataset = Dataset()
dataset.fit((i[0] for i in data), (m[1] for m in data))
interactions, ratings = dataset.build_interactions(data)

# Be sure to close the connection
con.close()

model = LightFM(loss='warp')

# train lightFM model using fit method
model.fit(ratings, epochs=30, num_threads=2)

def Recomender(model, ratings, userid):
    # number of movies and users in our dataset
    n_users, n_items = ratings.shape

    # list of movie indices that user likes
    known = ratings.tocsr()[userid].indices

    # predicting the scores
    scores = model.predict(userid, np.arange(n_items))

    # ranking them in non increasing order
    top = np.argsort(-scores)

    # display results
    print("User %s" % userid)
    print("------Known Choices:")
    for x in known[:5]:
        print("%s" % x)
    print("------Recomended:")
    for x in top[:5]:
        print("%s" % x)

# predicting top 5 movies for the user 23
Recomender(model, ratings, 23)
