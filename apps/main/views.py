from django.shortcuts import render
from datetime import datetime, timedelta

from models import *

# Create your views here.
def index(request):
	# topics_on_main_page = 3
	# data = {
	# 	'active_topics': Topic.objects.filter(  date_add__gt=datetime.datetime.now() - timedelta(days=1),
	# 			                                date_add__lt=datetime.datetime.now()
	# 			                                ).order_by('id')[:topics_on_main_page],

	# 	'vote_topics': Topic.objects.filter(	date_add__gt=datetime.datetime.now() - timedelta(days=2),
	# 			                            	date_add__lt=datetime.datetime.now() - timedelta(days=1)
	# 			                            	).order_by('id')[:topics_on_main_page],

	# 	'archive_topics': Topic.objects.filter( date_add__gt=datetime.datetime.now() - timedelta(days=2)
	# 			                            	).order_by('id')[:topics_on_main_page]
	# }
	return render(request, 'index.html', {})