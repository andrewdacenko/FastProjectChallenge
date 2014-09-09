from django.shortcuts import render
from datetime import datetime, timedelta

from models import *

def index(request):
	return render(request, 'index.html', {})

def topic(request, topic_id):
	# if request.method == 'POST':
		# t = Topic.objects.get
		# return ''
	return render(request, 'topic.html', {})

def state(request):
	return render(request, 'state.html', {})