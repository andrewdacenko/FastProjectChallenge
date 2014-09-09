from django.contrib import admin
from models import *

admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(TopicUserLike)
admin.site.register(CommentUserLike)
admin.site.register(Vote)
