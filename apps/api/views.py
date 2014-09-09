from django.shortcuts import render
from datetime import datetime, timedelta
from dateutil.tz import tzutc
import json

from apps.main.models import *
from django.http import HttpResponse

UTC = tzutc()

def topic_to_json(topic_list):
	res = []
	for t in topic_list:
		res.append({
			'id': t.id,
			'owner': {
					'id': t.owner.id,
					'username': t.owner.username
				},
			'title': t.title,
			'date_add': str(t.date_add.isoformat())
			})
	return res

def index(request):
	topics_on_main_page = 3
	data = {
		'active_topics': topic_to_json(Topic.objects.filter(  date_add__gt=datetime.datetime.now() - timedelta(days=1),
				                                date_add__lt=datetime.datetime.now()
				                                ).order_by('id')[:topics_on_main_page]),

		'vote_topics': topic_to_json(Topic.objects.filter(	date_add__gt=datetime.datetime.now() - timedelta(days=2),
				                            	date_add__lt=datetime.datetime.now() - timedelta(days=1)
				                            	).order_by('id')[:topics_on_main_page]),

		'archive_topics': topic_to_json(Topic.objects.filter( date_add__gt=datetime.datetime.now() - timedelta(days=2)
				                            	).order_by('id')[:topics_on_main_page])
	}
	return HttpResponse(json.dumps(data), content_type="application/json", status=400)