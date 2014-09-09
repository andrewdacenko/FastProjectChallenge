from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.api.views.index'),
    url(r'^active$', 'apps.api.views.active'),
    url(r'^archive$', 'apps.api.views.archive'),
    url(r'^voting$', 'apps.api.views.voting'),
    url(r'^topics$', 'apps.api.views.topics'),
    url(r'^topic/(?P<topic_id>\d+)$', 'apps.api.views.topic'),


    url(r'^topic/(?P<topic_id>\d+)/like$', 'apps.api.views.topic_like'),
    url(r'^topic/(?P<topic_id>\d+)/dislike$', 'apps.api.views.topic_dislike'),

    url(r'^comment/(?P<comment_id>\d+)/like$', 'apps.api.views.comment_like'),
    url(r'^comment/(?P<comment_id>\d+)/dislike$', 'apps.api.views.comment_dislike'),

)
