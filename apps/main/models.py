from django.db import models
import datetime

class Topic(models.Model):
	owner = models.ForeignKey('auth.User', related_name='tu')
	title = models.CharField(max_length=255)
	date_add = models.DateTimeField(default = datetime.datetime.now())

class Comment(models.Model):
	user = models.ForeignKey('auth.User', related_name='cu')
	topic = models.ForeignKey('main.Topic', related_name='ct')
	q_comment = models.ForeignKey(Topic, related_name='cc', null=True, on_delete=models.SET_NULL, blank=True)
	text = models.CharField(max_length=255)
	date_add = models.DateTimeField(default = datetime.datetime.now())

class TopicUserLike(models.Model):
	user = models.ForeignKey('auth.User', related_name='tulu')
	topic = models.ForeignKey(Topic, related_name='tult')
	value = models.IntegerField(default = 0)

class CommentUserLike(models.Model):
	user = models.ForeignKey('auth.User', related_name='culu')
	comment = models.ForeignKey(Comment, related_name='culc')
	value = models.IntegerField(default = 0)

class Vote(models.Model):
	user_from = models.ForeignKey('auth.User', related_name='vuf')
	user_to = models.ForeignKey('auth.User', related_name='vut')
	topic = models.ForeignKey(Topic, related_name='vt')