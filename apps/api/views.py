from django.shortcuts import render
from datetime import datetime, timedelta
from dateutil.tz import tzutc
from django.contrib.auth.models import User
import json

from apps.main.models import *
from django.http import HttpResponse, HttpResponseRedirect

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
			'sum': TopicUserLike().likes(t.id)['value__sum'],
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
			qcl = c.q_comment
			if c.q_comment:
				qcl = {
					'id': c.q_comment.id,
					'username': c.q_comment.username
				}
			comments.append({
				'id': c.id,
				'user':{
					'id': c.user.id,
					'username': c.user.username
				},
				'q_comment_id': qcl,
				'sum': CommentUserLike().likes(t.id)['value__sum'],
				'text': c.text,
				'date_add': str(c.date_add.isoformat())
				})
		t = {
			'id': t.id,
			'owner': {
					'id': t.owner.id,
					'username': t.owner.username
				},
			'title': t.title,
			'sum': TopicUserLike().likes(t.id)['value__sum'],
			'comments': comments,
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
	if request.method == 'POST':
		try:
			t = Topic.objects.get(id=topic_id)
			if not t.is_active():
				return HttpResponse(json.dumps({ 'error': 'comment error' }), content_type="application/json", status=403)
			c = Comment(user=request.user, topic_id=topic_id, text=request.POST.get('text', ''), date_add=datetime.datetime.now())
			if request.POST.get('q_comment'):
				c.q_comment_id = request.POST.get('q_comment', 1)
			c.save()
		except:
			return HttpResponse(json.dumps({ 'error': 'auth error' }), content_type="application/json", status=401)
	t = full_topic_to_json(topic_id)
	return HttpResponse(json.dumps(t), content_type="application/json")

def topics(request):
	if request.method != 'POST':
		return HttpResponseRedirect('/')
	try:
		t = Topic(owner = request.user, title = request.POST.get('title', ''))
		t.save()
		t = full_topic_to_json(t.id)
		return HttpResponse(json.dumps(t), content_type="application/json")
	except:	
		return HttpResponse(json.dumps({ 'error': 'auth error' }), content_type="application/json", status=401)

def topic_like(request, topic_id):
	try:
		tul = TopicUserLike.objects.filter(user_id=request.user.id, topic_id=topic_id)
		if len(tul):
			return HttpResponse(json.dumps({ 'error': 'already liked' }), content_type="application/json", status=403)
		TopicUserLike(user_id=request.user.id, topic_id=topic_id, value=1).save()
		return HttpResponse(json.dumps({ 'result': 'ok' }), content_type="application/json")
	except:	
		return HttpResponse(json.dumps({ 'error': 'auth error' }), content_type="application/json", status=401)

def topic_dislike(request, topic_id):
	try:
		tul = TopicUserLike.objects.filter(user_id=request.user.id, topic_id=topic_id)
		if len(tul):
			return HttpResponse(json.dumps({ 'error': 'already liked' }), content_type="application/json", status=403)
		TopicUserLike(user_id=request.user.id, topic_id=topic_id, value=-1).save()
		return HttpResponse(json.dumps({ 'result': 'ok' }), content_type="application/json")
	except:	
		return HttpResponse(json.dumps({ 'error': 'auth error' }), content_type="application/json", status=401)

def comment_like(request, comment_id):
	try:
		cul = CommentUserLike.objects.filter(user_id=request.user.id, comment_id=comment_id)
		if len(cul):
			return HttpResponse(json.dumps({ 'error': 'already liked' }), content_type="application/json", status=403)
		CommentUserLike(user_id=request.user.id, comment_id=comment_id, value=1).save()
		return HttpResponse(json.dumps({ 'result': 'ok' }), content_type="application/json")
	except:	
		return HttpResponse(json.dumps({ 'error': 'auth error' }), content_type="application/json", status=401)

def comment_dislike(request, comment_id):
	try:
		cul = CommentUserLike.objects.filter(user_id=request.user.id, comment_id=comment_id)
		if len(cul):
			return HttpResponse(json.dumps({ 'error': 'already liked' }), content_type="application/json", status=403)
		CommentUserLike(user_id=request.user.id, comment_id=comment_id, value=-1).save()
		return HttpResponse(json.dumps({ 'result': 'ok' }), content_type="application/json")
	except:	
		return HttpResponse(json.dumps({ 'error': 'auth error' }), content_type="application/json", status=401)
