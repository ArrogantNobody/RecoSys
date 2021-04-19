from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from RecoFramework.models import UserInfo,Ratings
import sqlite3
import numpy as np
from lightfm import LightFM
from lightfm.data import Dataset
import sqlite3
from lightfm.evaluation import precision_at_k
from lightfm.evaluation import auc_score
from lightfm.cross_validation import random_train_test_split
import imdb
import json
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

    dataset = Dataset()
    #print("Loading dataset...")
    dataset.fit(users, movies)
    interactions, ratings = dataset.build_interactions(data)

    # Be sure to close the connection
    con.close()

    train, test = random_train_test_split(interactions)

    model = LightFM(loss='warp')

    # train lightFM model using fit method
    #print("Starting training the model...")
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
    #print('Predicting the scores')
    scores = model.predict(user_index, np.arange(n_items))

    # ranking them in non increasing order
    top = np.argsort(-scores)
    for i, movie in enumerate(top):
        recommended_movies.append(movie_indices[movie_ids.index(movie)])
    # display results
    #print("User %s" % str(userid))
    #print("------Known Choices:")
    # for x in known_movies[:20]:
    #     print("%s" % x)
    # print("------Recomended:")
    # for x in recommended_movies[:10]:
    #     print("%s" % x)

    con = sqlite3.connect("db.sqlite3")
    con.row_factory = dict_factory
    cur = con.cursor()
    result = []

    for mid in recommended_movies[:10]:
        cur.execute("SELECT * FROM RecoFramework_movies WHERE movieId=?", (mid, ))
        r = cur.fetchone()
        result.append(r)

    con.close()

    #evaluation(model, train, test)

    return result

def mvid_l(recommended_movies):
    imbdid_li = []
    for item in recommended_movies:
        imbdid_li.append(list(item.values())[0][0])
    return imbdid_li


def get_ImgURL_from_ID_lst(id_lst):
    d = []
    access = imdb.IMDb()
    for id in id_lst:
        movie = access.get_movie(id)
        d.append((movie['title'], movie['cover url']))
    return d





def rated_movie_list():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    rating = []

    rated = list(cur.execute('SELECT movieId, rating FROM RecoFramework_ratings where userId = 1'))
    rated_mv = [a[0] for a in rated]
    return rated_mv

def update_data(rate_value, userid, i):
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    cur.execute('update RecoFramework_ratings set rating = %d where userId = %d and movieId = %d' % (rate_value, userid, i))
    #cur.execute('update RecoFramework_ratings set rating = 5 where userId = 1 and movieId = 1')
    con.commit()

def insert_data(userid, i, rate_value):
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    cur.execute('insert into RecoFramework_ratings(userId, movieId, rating) VALUES (%d, %d, %d)'% (userid, i, rate_value))
    con.commit()


def pop(request):
    return render(request, 'newuser_form.html')

@csrf_exempt
def form_process(request):
    if request.method == "POST":
        mv_list = ["mv1", "mv2", "mv3", "mv4", "mv5", "mv6", "mv7", "mv8", "mv9", "mv10"]
        mv_value = {}
        for item in mv_list:
            mv_value[item] = request.POST[item]
        #print(mv_value)
        userid = request.session.get('userid')
        userid = userid.values()[0]['id']
        print(userid)
        ratedmv = rated_movie_list()
        #print(ratedmv)
        for i in range(1,11):
            rate_value = int(mv_value[mv_list[i - 1]])
            #print(rate_value)
            if i in ratedmv:#the movie is in that database, we need to update
                #update_data(rate_value, userid, i)
                try:
                    update_data(rate_value, userid, i)
                    # Ratings.objects.filter(userId=userid, movieId=i).update(rating=rate_value)
                except:
                    print('update failed')

            else:#the movie is not in database, we need to create
                try:
                    insert_data(userid, i, rate_value)
                    #cur.execute('insert into RecoFramework_ratings(userId, movieId, rating) VALUES (%d, %d, %d)'% (userid, i, rate_value))
                    # Ratings.objects.create(userId=userid, movieId=i, rating=rate_value)
                except:
                    print('insert failed')
        movieids = recommend_by_userid(userid)
        mvidList = mvid_l(movieids)
        print(movieids)
        url_lis = json.dumps(get_ImgURL_from_ID_lst(mvidList))

        return render(request, '802project.html', {'urllist': url_lis})

        

