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

def full_topic_to_json(topic_id):
	t = Topic.objects.filter(id=topic_id)
	if len(t):
		t=t[0]
		comments = []
		cs = Comment.objects.filter(topic_id=t.id)
		for c in cs:
			comments.append({
				'id': c.id,
				'user': c.user.username,
				'q_comment_id': c.q_comment.id,
				'text': c.text,
				'date_add': str(t.date_add.isoformat())
				})
		t = {
			'id': t.id,
			'owner': {
					'id': t.owner.id,
					'username': t.owner.username
				},
			'title': t.title,
			'date_add': str(t.date_add.isoformat())
			}
	else:
		t = { 'title': 'None' }
	return t

def index(request):
	topics_on_main_page = 3
	data = {
		'active': topic_to_json(Topic.objects.filter(  date_add__gt=datetime.datetime.now() - timedelta(days=1),
				                                date_add__lt=datetime.datetime.now()
				                                ).order_by('id')[:topics_on_main_page]),

		'voting': topic_to_json(Topic.objects.filter(	date_add__gt=datetime.datetime.now() - timedelta(days=2),
				                            	date_add__lt=datetime.datetime.now() - timedelta(days=1)
				                            	).order_by('id')[:topics_on_main_page]),

		'archive': topic_to_json(Topic.objects.filter( date_add__lt=datetime.datetime.now() - timedelta(days=2)
				                            	).order_by('id')[:topics_on_main_page])
	}
	return HttpResponse(json.dumps(data), content_type="application/json")

def active(request):
	data = topic_to_json(Topic.objects.filter(  date_add__gt=datetime.datetime.now() - timedelta(days=1),
				                                date_add__lt=datetime.datetime.now() ).order_by('id'))
	return HttpResponse(json.dumps(data), content_type="application/json")

def archive(request):
	data = topic_to_json(Topic.objects.filter( date_add__lt=datetime.datetime.now() - timedelta(days=2)
				                            	).order_by('id'))
	return HttpResponse(json.dumps(data), content_type="application/json")

def voting(request):
	data = topic_to_json(Topic.objects.filter(	date_add__gt=datetime.datetime.now() - timedelta(days=2),
				                            	date_add__lt=datetime.datetime.now() - timedelta(days=1)
				                            	).order_by('id'))
	return HttpResponse(json.dumps(data), content_type="application/json")

def topic(request, topic_id):
	t = full_topic_to_json(topic_id)
	return HttpResponse(json.dumps(t), content_type="application/json")