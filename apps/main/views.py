from django.shortcuts import render
from datetime import datetime, timedelta

from models import *

def index(request):
	return render(request, 'index.html', {})

def topic(request, topic_id):
	return render(request, 'topic.html', {})

def state(request):
	return render(request, 'state.html', {})