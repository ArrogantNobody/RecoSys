import numpy as np
from lightfm.datasets import fetch_movielens
from lightfm import LightFM

# fetch movie data having a minimum rating of five
data = fetch_movielens(min_rating=5.0)
model = LightFM(loss='warp')

# train lightFM model using fit method
model.fit(data['train'], epochs=30, num_threads=2)

def Recomender(model, data, userid):
    # number of movies and users in our dataset
    n_users, n_items = data['train'].shape

    # list of movie indices that user likes
    known = data['item_labels'][data['train'].tocsr()[userid].indices]

    # predicting the scores
    scores = model.predict(userid, np.arange(n_items))

    # ranking them in non increasing order
    top = data['item_labels'][np.argsort(-scores)]

    # display results
    print("User %s" % userid)
    print("------Known Choices:")
    for x in known[:5]:
        print("%s" % x)
    print("------Recomended:")
    for x in top[:5]:
        print("%s" % x)

# predicting top 5 movies for the user 23
Recomender(model, data, 23)
