from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
import datetime

class Topic(models.Model):
	owner = models.ForeignKey('auth.User', related_name='tu')
	title = models.CharField(max_length=255)
	date_add = models.DateTimeField(default = datetime.datetime.now())

	def is_active(self):
		return self.date_add >= timezone.now() - datetime.timedelta(days=1)

class Comment(models.Model):
	user = models.ForeignKey('auth.User', related_name='cu')
	topic = models.ForeignKey('main.Topic', related_name='ct')
	q_comment = models.ForeignKey('auth.User', related_name='cc', null=True, on_delete=models.SET_NULL, blank=True)
	text = models.CharField(max_length=255)
	date_add = models.DateTimeField(default = datetime.datetime.now())

class TopicUserLike(models.Model):
	user = models.ForeignKey('auth.User', related_name='tulu')
	topic = models.ForeignKey(Topic, related_name='tult')
	value = models.IntegerField(default = 0)

	def likes(self, topic_id):
		return TopicUserLike.objects.filter(topic_id=topic_id).aggregate(models.Sum('value'))

	def get_top_users(self, topic_id):
		tuls = TopicUserLike.objects.filter(topic_id=topic_id)
		users = []
		for tul in tuls:
			if tul.user not in users:
				users.append(tul.user)
		res = []
		for u in users:
			res.append({
				'id': u.id,
				'username': u.username,
				'sum': TopicUserLike.objects.filter(user_id=u.id, topic_id=topic_id).aggregate(models.Sum('value'))['value__sum']
			})
		return res

class CommentUserLike(models.Model):
	user = models.ForeignKey('auth.User', related_name='culu')
	comment = models.ForeignKey(Comment, related_name='culc')
	value = models.IntegerField(default = 0)

	def likes(self, comment_id):
		print CommentUserLike.objects.filter(comment_id=comment_id)
		return CommentUserLike.objects.filter(comment_id=comment_id).aggregate(models.Sum('value'))

class Vote(models.Model):
	user_from = models.ForeignKey('auth.User', related_name='vuf')
	user_to = models.ForeignKey('auth.User', related_name='vut')
	topic = models.ForeignKey(Topic, related_name='vt')

	def choice(self,topic_id, user_to_id):
		v = Vote().objects.filter(user_to_id=user_to_id, topic_id=topic_id)
		if len(v):
			return v[0].user_from.id
		return None