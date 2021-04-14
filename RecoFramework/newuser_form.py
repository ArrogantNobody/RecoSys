from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from RecoFramework.models import UserInfo,Ratings

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
        print(userid.values()[0]['id'])
        for i in range(1,11):
            Ratings.objects.create(userId=userid, movieId=i, rating = mv_value[mv_list[i-1]])
    return render(request, '802project.html', {'userid': userid})
        

