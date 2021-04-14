from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
#from django.db import models
from RecoFramework.models import UserInfo

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
            return render(request, '802project.html', {'userid': request.session['userid']})
        else:
            return render(request, 'adminPage.html',{'script': "alert", 'wrong': 'You have input wrong ccid, please re-input'})

