from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.shortcuts import render

from apps.main.models import *
# from apps.main.models import Organization, SystemUser, UserType
from django.http import HttpResponse
import json


def index(request):
    return HttpResponseRedirect('/')

def login(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'login.html', c)

def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login/')
    return HttpResponseRedirect('/login/')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')

def register_user(request):
    if request.method == 'POST':
        if not request.POST['username']  or not request.POST['password'] or (0 < len(User.objects.filter(username=str(request.POST['username'])))):
            pass
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.create_user(username, username+'@'+username+'.ff', password)
            user.save()
            return HttpResponseRedirect('/login/')
    args={}
    args.update(csrf(request))
    return render(request, 'register.html', args)