from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'apps.api.views.index'),
    url(r'active$', 'apps.api.views.active'),
    url(r'archive$', 'apps.api.views.archive'),
    url(r'voting$', 'apps.api.views.voting'),

)
