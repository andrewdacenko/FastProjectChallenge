from django.shortcuts import render
from datetime import datetime, timedelta
from django.core.context_processors import csrf

from models import *

def index(request):
	return render(request, 'index.html', {})

def topic(request, topic_id):
	c = {}
    c.update(csrf(request))
	return render(request, 'topic.html', c)

def state(request):
	return render(request, 'state.html', {})