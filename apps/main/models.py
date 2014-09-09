from django.db import models
import datetime

# class Topic(models.Model):
# 	owner = models.ForeignKey('auth.User', relation_name='user_topics')
# 	title = models.CharField(max_length=255)
# 	date_add = models.DateTimeField(default = datetime.datetime.now())

# class Comment(models.Model):
# 	user = models.ForeignKey('auth.User', relation_name='user_topics')
# 	topic = models.ForeignKey(Topic, relation_name='topic_comment')
# 	q_comment = models.ForeignKey(Topic, relation_name='topic_comment')
# 	text = models.CharField(max_length=255)
# 	date_add = models.DateTimeField(default = datetime.datetime.now())