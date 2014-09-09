from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.shortcuts import render

from utils.decorators import render_to
from apps.main.models import *
# from apps.main.models import Organization, SystemUser, UserType
from django.http import HttpResponse
import json

def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
    return HttpResponseRedirect('/')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def register_user(request):
    if not request.POST['username']  or not request.POST['password'] or (0 < len(User.objects.filter(username=str(request.POST['username'])))):
        return HttpResponse(json.dumps({ 'error': 'Not full information, or user already exist' }), content_type="application/json", status=400)
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username, username+'@'+username+'.ff', password)
        user.save()
        return HttpResponseRedirect('/')
