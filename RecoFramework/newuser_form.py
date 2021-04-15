from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from RecoFramework.models import UserInfo,Ratings
import sqlite3

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
        print(mv_value)
        userid = request.session.get('userid')
        userid = userid.values()[0]['id']
        ratedmv = rated_movie_list()
        print(ratedmv)

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

        return HttpResponse('ok')

        

