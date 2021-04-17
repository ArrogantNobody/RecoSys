from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
#from django.db import models
import numpy as np
from lightfm import LightFM
from lightfm.data import Dataset
import sqlite3
from lightfm.evaluation import precision_at_k
from lightfm.evaluation import auc_score
from lightfm.cross_validation import random_train_test_split
from RecoFramework.models import UserInfo
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







def login_map(request):
    return render(request, 'adminPage.html')

def login_success(request):
    return render(request, 'sessionTest.html')


@csrf_exempt
def ccid_verify(request):
    # try:
    #     UserInfo.objects.create(username='BQ', password='456', age=27)
    #     print('successful')
    # except:
    #     print('failed')
    # try:
    #     for i in range(941):
    #         UserInfo.objects.create(username='admin', password='123', age=18)
    #     print('successful')
    # except:
    #     print('failed')
    user_list_obj = UserInfo.objects.values()
    ccid_list = []
    for item in user_list_obj:
        username = item['username']
        ccid_list.append(username)
    #print(ccid_list)

    if request.method == "POST":
        username = request.POST['username']
        userid = UserInfo.objects.filter(username=username)
        if username in ccid_list:
            request.session['userid'] = userid # also cookie
            userid = userid.values()[0]['id']
            print(userid)
            movieids = recommend_by_userid(userid)
            mvidList = mvid_l(movieids)
            print(movieids)
            url_lis = json.dumps(get_ImgURL_from_ID_lst(mvidList))

            #url_lis = json.dumps([(1,'bs'),(3,'shit'),(5,'fuck'),(7,'basu'),(9,'ma4')])
            return render(request, '802project.html', {'urllist': url_lis})
        else:
            return render(request, 'adminPage.html',{'script': "alert", 'wrong': 'You have input wrong ccid, please re-input'})

